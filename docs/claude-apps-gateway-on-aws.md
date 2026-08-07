> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploy Claude apps gateway on AWS

> A worked example of running Claude apps gateway on AWS: ECS Fargate or EKS, Amazon RDS for PostgreSQL, AWS Secrets Manager, and IAM-role auth to Amazon Bedrock.

<Note>
  This page walks through one way to run Claude apps gateway on AWS. The configuration is a working example for customer-managed infrastructure rather than a supported production deployment; use it to see how the pieces fit together before adapting it to your own environment. For the platform-agnostic requirements, see the [deployment guide](/docs/en/claude-apps-gateway-deploy).
</Note>

This example provisions Claude apps gateway on AWS with Amazon Bedrock as the model upstream, using either [Amazon ECS](https://aws.amazon.com/ecs/) on [AWS Fargate](https://aws.amazon.com/fargate/) or [Amazon EKS](https://aws.amazon.com/eks/) for compute. [Okta](https://www.okta.com/) is the example identity provider (IdP), but any OpenID Connect (OIDC) compliant IdP works; see [Identity provider setup](/docs/en/claude-apps-gateway-deploy#identity-provider-setup) for per-IdP details.

<Note>
  Bedrock isn't the only Claude upstream on AWS. The gateway also supports Claude Platform on AWS, the Anthropic-operated Claude API with AWS authentication and AWS Marketplace billing, in place of Bedrock or alongside it. Its upstream entry, credentials, and IAM permissions differ from this page's Bedrock-scoped ones; the [Claude Platform on AWS upstream reference](/docs/en/claude-apps-gateway-config#claude-platform-on-aws) covers what changes, and the rest of this page applies unchanged.
</Note>

## Architecture

<Frame caption="The example architecture, with Amazon Bedrock as the model upstream. A Claude Platform on AWS upstream occupies the same position.">
  <img src="https://mintcdn.com/claude-code/PHweeRmDUYEKff49/images/claude-gateway-aws-architecture.svg?fit=max&auto=format&n=PHweeRmDUYEKff49&q=85&s=8599cc34aa28522cde208ee831439bb4" alt="Diagram of Claude apps gateway on AWS: Claude Code clients connect over HTTPS to an internal Application Load Balancer fronting the gateway (ECS Fargate or EKS), which runs in private subnets alongside an Amazon RDS for PostgreSQL instance for session state. The gateway signs users in via OIDC against the corporate IdP, reads secrets from AWS Secrets Manager, forwards model requests to Amazon Bedrock using its IAM role, and pulls its image from Amazon ECR at deploy." width="820" height="430" data-path="images/claude-gateway-aws-architecture.svg" />
</Frame>

The gateway runs as a private HTTPS endpoint on your network that developers sign in to through your IdP. Their Claude Code sessions reach Claude models on Amazon Bedrock through the gateway's IAM role, so no model credentials land on developer machines. The reference configuration provisions:

* **Amazon ECS on AWS Fargate** service or **Amazon EKS** Deployment running the gateway container
* **Amazon ECR** repository for the gateway image
* **Amazon RDS for PostgreSQL** instance in private subnets, not publicly accessible, for the gateway's [store](/docs/en/claude-apps-gateway-config#store)
* **AWS Secrets Manager** secrets for the JWT signing key, the OIDC client secret, and the Postgres URL
* **IAM role** with `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`, attached as the ECS task role or bound via IAM Roles for Service Accounts (IRSA) on EKS
* **Internal Application Load Balancer** for HTTPS

## Prerequisites

The walkthrough creates the gateway's own resources, but it builds on network and identity infrastructure you already have. Before you start, you need:

* An AWS account with permission to create the [resources above](#architecture)
* The [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and [authenticated](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-authentication.html), and [Docker](https://docs.docker.com/get-started/get-docker/) installed locally
* A [VPC](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) with at least two [private subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html) in different Availability Zones, with outbound internet access through a [NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html); the internal load balancer needs subnets in two AZs, and the gateway needs egress to Bedrock and your IdP
* An Okta OIDC web application with redirect URI `https://<gateway-host>/oauth/callback`; see [Identity provider setup](/docs/en/claude-apps-gateway-deploy#identity-provider-setup)
* A TLS hostname for the gateway, typically an internal DNS name in a [Route 53 private hosted zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-private.html) pointing at the load balancer, with an [ACM certificate](https://docs.aws.amazon.com/acm/latest/userguide/gs.html) for that name, imported or issued by [AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html)

### Set your environment variables

Every command on this page reads four values from your shell: `AWS_REGION`, `ACCOUNT_ID`, `VPC_ID`, and `PRIVATE_SUBNETS`.

Pick a US region where Bedrock serves the Claude models you need. The walkthrough relies on the gateway's built-in model catalog, which resolves to `us.anthropic.*` inference profiles, and the IAM policy grants those ARNs. In a non-US region, add a [`models:` block](/docs/en/claude-apps-gateway-config#models) with that geo's inference-profile IDs and change the IAM policy's ARN prefix to match.

If you don't have the VPC ID at hand, list your VPCs with `aws ec2 describe-vpcs`, then list that VPC's subnets to find two private ones in different Availability Zones:

```bash theme={null}
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<your-vpc-id>" \
  --query 'Subnets[].{ID:SubnetId,AZ:AvailabilityZone,CIDR:CidrBlock}' --output table
```

Export all four before continuing:

```bash theme={null}
export AWS_REGION=us-east-1   # a US region where Bedrock serves the Claude models you need
export ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export VPC_ID=<your-vpc-id>
export PRIVATE_SUBNETS="<subnet-id-a> <subnet-id-b>"
```

## Deploy the gateway

The steps below provision the full deployment with `aws` commands.

<Steps>
  <Step title="Create the security groups">
    Three security groups chain the traffic path: your corporate network reaches the load balancer on 443, the load balancer reaches the gateway on 8080, and the gateway reaches Postgres on 5432. Nothing else is reachable. How you attach them depends on the compute track:

    * On ECS Fargate, the deploy step attaches `$ALB_SG` to the load balancer and `$GW_SG` to the service.
    * On EKS, the AWS Load Balancer Controller creates its own frontend security group for the ALB, so `$ALB_SG` and `$GW_SG` go unused: the deploy step's `inbound-cidrs` annotation restricts the listener to your corporate network, and the database security group admits the cluster's security group instead.

    ```bash theme={null}
    ALB_SG="$(aws ec2 create-security-group --group-name claude-gateway-alb \
      --description "Claude gateway ALB" --vpc-id "$VPC_ID" \
      --query GroupId --output text)"
    GW_SG="$(aws ec2 create-security-group --group-name claude-gateway-svc \
      --description "Claude gateway service" --vpc-id "$VPC_ID" \
      --query GroupId --output text)"
    DB_SG="$(aws ec2 create-security-group --group-name claude-gateway-db \
      --description "Claude gateway Postgres" --vpc-id "$VPC_ID" \
      --query GroupId --output text)"

    aws ec2 authorize-security-group-ingress --group-id "$ALB_SG" \
      --protocol tcp --port 443 --cidr <your-corporate-cidr>
    aws ec2 authorize-security-group-ingress --group-id "$GW_SG" \
      --protocol tcp --port 8080 --source-group "$ALB_SG"
    aws ec2 authorize-security-group-ingress --group-id "$DB_SG" \
      --protocol tcp --port 5432 --source-group "$GW_SG"
    ```
  </Step>

  <Step title="Create the IAM roles and submit the use case form">
    The gateway runs with a dedicated task role whose only permission is invoking Claude models on Bedrock. Per the [Bedrock upstream reference](/docs/en/claude-apps-gateway-config#amazon-bedrock), the policy must cover both the cross-region inference-profile ARNs and the underlying foundation-model ARNs:

    ```bash theme={null}
    cat > bedrock-invoke.json <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
        "Resource": [
          "arn:aws:bedrock:${AWS_REGION}:${ACCOUNT_ID}:inference-profile/us.anthropic.*",
          "arn:aws:bedrock:*::foundation-model/anthropic.*"
        ]
      }]
    }
    EOF
    cat > ecs-trust.json <<'EOF'
    {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Principal": { "Service": "ecs-tasks.amazonaws.com" },
        "Action": "sts:AssumeRole"
      }]
    }
    EOF

    aws iam create-role --role-name claude-gateway-task \
      --assume-role-policy-document file://ecs-trust.json
    aws iam put-role-policy --role-name claude-gateway-task \
      --policy-name bedrock-invoke --policy-document file://bedrock-invoke.json
    ```

    ECS also needs an execution role, which the ECS agent itself uses to pull the image from ECR and inject the Secrets Manager values created later. It is separate from the task role the gateway's AWS SDK uses at runtime:

    ```bash theme={null}
    aws iam create-role --role-name claude-gateway-execution \
      --assume-role-policy-document file://ecs-trust.json
    aws iam attach-role-policy --role-name claude-gateway-execution \
      --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
    cat > secrets-read.json <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
        "Resource": [
          "arn:aws:secretsmanager:${AWS_REGION}:${ACCOUNT_ID}:secret:gateway-jwt-secret-??????",
          "arn:aws:secretsmanager:${AWS_REGION}:${ACCOUNT_ID}:secret:gateway-oidc-client-secret-??????",
          "arn:aws:secretsmanager:${AWS_REGION}:${ACCOUNT_ID}:secret:gateway-postgres-url-??????"
        ]
      }]
    }
    EOF
    aws iam put-role-policy --role-name claude-gateway-execution \
      --policy-name read-gateway-secrets --policy-document file://secrets-read.json
    ```

    The policy names one ARN per secret rather than a bare `gateway-*` wildcard, which in a shared account would also match unrelated secrets; the trailing `-??????` matches exactly the random six-character suffix Secrets Manager appends to every secret's ARN. A trailing `-*` would be a plain prefix glob and would also match longer names such as `gateway-postgres-url-prod`.

    The IAM policy grants the gateway permission to call Bedrock, and Bedrock enables model access by default in commercial regions. The remaining account-level gate is Anthropic's one-time use case form: if no one in your account has submitted it, open the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/), select an Anthropic model from the Model catalog, and complete the form. Access is granted immediately after submission; see [Claude Code on Amazon Bedrock](/docs/en/amazon-bedrock#1-submit-use-case-details) for the AWS Organizations form and the IAM permissions the submitter needs.

    The EKS track reuses both policy documents on an IRSA role instead of the two ECS roles; see the deploy step.
  </Step>

  <Step title="Provision Amazon RDS for PostgreSQL">
    The instance runs in the private subnets with no public address and storage encryption on. The engine version is pinned to Postgres 16, which satisfies the gateway's supported floor of PostgreSQL 14 and guarantees the parameter-group family below matches the instance.

    First, create the subnet group that places the database in the private subnets, and a parameter group with `rds.force_ssl=1` so the server rejects plaintext connections. The engine version is pinned once because the parameter group's family must match the engine major version the instance runs:

    ```bash theme={null}
    aws rds create-db-subnet-group --db-subnet-group-name claude-gateway-db \
      --db-subnet-group-description "Claude gateway" --subnet-ids $PRIVATE_SUBNETS

    PG_VERSION=16
    PG_FAMILY="postgres${PG_VERSION}"
    aws rds create-db-parameter-group --db-parameter-group-name claude-gateway-db \
      --db-parameter-group-family "$PG_FAMILY" \
      --description "Claude gateway - require TLS on every connection"
    aws rds modify-db-parameter-group --db-parameter-group-name claude-gateway-db \
      --parameters "ParameterName=rds.force_ssl,ParameterValue=1,ApplyMethod=immediate"
    ```

    Then create the instance with a generated master password:

    ```bash theme={null}
    PGPASS="$(openssl rand -hex 24)"
    aws rds create-db-instance --db-instance-identifier claude-gateway-db \
      --engine postgres --engine-version "$PG_VERSION" \
      --db-instance-class db.t4g.micro \
      --allocated-storage 20 --db-name claude_gateway \
      --master-username gateway --master-user-password "$PGPASS" \
      --db-subnet-group-name claude-gateway-db \
      --db-parameter-group-name claude-gateway-db \
      --vpc-security-group-ids "$DB_SG" \
      --no-publicly-accessible --storage-encrypted
    ```

    The literal `--master-user-password` argument is visible in the process table and in audit/EDR logs while the command runs, the same exposure the secrets step's note covers. On a shared or monitored host, pass the password via `--cli-input-json` from a `0600` file instead, the way the bundle's `setup.sh` does.

    Wait for the instance to come up, which can take several minutes, then read its private endpoint and assemble the connection string the gateway will use:

    ```bash theme={null}
    aws rds wait db-instance-available --db-instance-identifier claude-gateway-db
    DB_HOST="$(aws rds describe-db-instances --db-instance-identifier claude-gateway-db \
      --query 'DBInstances[0].Endpoint.Address' --output text)"
    GATEWAY_POSTGRES_URL="postgres://gateway:${PGPASS}@${DB_HOST}:5432/claude_gateway?sslmode=verify-full"
    ```

    `sslmode=verify-full` makes the gateway verify the RDS server certificate's chain and hostname, not only encrypt. The trust anchor is the [AWS RDS certificate bundle](https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem), which the image build step below copies to `/etc/claude/rds-global-bundle.pem` and trusts via `NODE_EXTRA_CA_CERTS`. Don't append a libpq-style `sslrootcert=` parameter to the URL: the gateway's driver reads only `sslmode` from the query string and would forward `sslrootcert` to Postgres as a startup parameter, which the server rejects.

    The ECS service or EKS pods must run in this VPC so they can reach the instance's private endpoint, and the `claude-gateway-db` security group only admits the gateway's security group.
  </Step>

  <Step title="Write gateway.yaml">
    The `upstreams` block points at Bedrock with `auth: {}`, so the gateway authenticates via the AWS default credential chain from the task role on ECS or the IRSA role on EKS. See the [configuration reference](/docs/en/claude-apps-gateway-config) for every field.

    Two `listen` fields describe what fronts the gateway:

    * `public_url`: the external `https://` origin, required for any non-loopback bind; see the [`listen` reference](/docs/en/claude-apps-gateway-config#listen). The gateway builds the IdP `redirect_uri` and its discovery document only from this value, never from `X-Forwarded-*` headers.
    * `trusted_proxies`: the front end's source ranges. The gateway honors `X-Forwarded-For` only when the TCP peer is in this list, then walks the chain past trusted hops, so per-IP sign-in rate limits and audit events record developer IPs instead of the load balancer's.

    On both tracks the front end is an internal ALB, whether created directly or by the AWS Load Balancer Controller, and an ALB's nodes take addresses from the subnets it is attached to, so set `trusted_proxies` to those subnets' CIDRs. This trusts every host in those subnets as a proxy. Keep the ALB's ingress source, your corporate CIDR, from overlapping them, and don't share the subnets with untrusted workloads that could spoof client IPs via `X-Forwarded-For`.

    ```yaml gateway.yaml theme={null}
    listen:
      host: 0.0.0.0
      port: 8080
      public_url: https://claude-gateway.internal.example.com
      trusted_proxies: [<your-alb-subnet-cidrs>]

    oidc:
      issuer: https://example.okta.com
      client_id: 0oa1example2
      client_secret: ${OIDC_CLIENT_SECRET}           # EKS: ${file:/secrets/oidc-client-secret}
      allowed_email_domains: [example.com]
      # The Okta org authorization server returns a thin id_token that omits
      # email and groups; the gateway fills them from /userinfo.
      userinfo_fallback: true
      # Okta emits groups only when the `groups` scope is requested and the
      # app's groups claim filter allows them.
      scopes: [openid, profile, email, offline_access, groups]

    session:
      jwt_secret: ${GATEWAY_JWT_SECRET}              # EKS: ${file:/secrets/jwt-secret}
      ttl_hours: 8                                   # bounds deprovision latency; lower
                                                     # toward 1 for tighter revocation

    store:
      postgres_url: ${GATEWAY_POSTGRES_URL}          # EKS: ${file:/secrets/postgres-url}

    upstreams:
      - provider: bedrock
        region: <your-region>                        # match $AWS_REGION so the IAM
                                                     # policy's ARNs cover it
        auth: {}                                     # AWS default credential chain:
                                                     # ECS task role, or IRSA on EKS
    ```

    <Note>
      Only the `oidc` block is Okta-specific. To use Microsoft Entra ID instead, set `issuer` to `https://login.microsoftonline.com/<tenant-id>/v2.0`, drop `userinfo_fallback` and the `groups` scope, and note that Entra emits group Object IDs rather than names, so [`managed.policies`](/docs/en/claude-apps-gateway-config#managed) must match on the GUIDs, or on App Roles with `oidc.groups_claim: roles`. See [Identity provider setup](/docs/en/claude-apps-gateway-deploy#identity-provider-setup).
    </Note>
  </Step>

  <Step title="Store secrets in AWS Secrets Manager">
    Create three secrets; the execution role from the IAM step can already read them:

    ```bash theme={null}
    aws secretsmanager create-secret --name gateway-jwt-secret \
      --secret-string "$(openssl rand -base64 32)"
    aws secretsmanager create-secret --name gateway-oidc-client-secret \
      --secret-string '<your-okta-client-secret>'
    aws secretsmanager create-secret --name gateway-postgres-url \
      --secret-string "$GATEWAY_POSTGRES_URL"
    ```

    Note the ARN each call prints; the ECS task definition references secrets by ARN.

    <Note>
      Literal `--secret-string` arguments are visible in the process table and in audit/EDR logs while each command runs. On a shared or monitored host, put the value in a `0600` file and pass `--secret-string file://<path>` instead. The bundle's `setup.sh` keeps secret values off process argv the same way, passing `0600` temporary files to `--cli-input-json`.
    </Note>

    Unlike the secrets, `gateway.yaml` itself contains no secret values, because every credential resolves at boot through [`${VAR}` or `${file:...}` expansion](/docs/en/claude-apps-gateway-config#secret-expansion). How everything reaches the container differs by track:

    * On ECS, the next step's build copies `gateway.yaml` into the image at `/etc/claude/gateway.yaml`, and the task definition injects the three secrets as environment variables via its `secrets` field, so the YAML references `${GATEWAY_JWT_SECRET}`, `${OIDC_CLIENT_SECRET}`, and `${GATEWAY_POSTGRES_URL}`.
    * On EKS, mount `gateway.yaml` from a ConfigMap and the secrets as files at `/secrets`, referenced as `${file:/secrets/...}`. Source the Kubernetes Secrets from Secrets Manager with External Secrets Operator or the Secrets Store CSI driver's AWS provider, or create them directly with `kubectl`.
  </Step>

  <Step title="Build and push the image to Amazon ECR">
    Build the image per the [container image requirements](/docs/en/claude-apps-gateway-deploy#container-image), placing the `linux-x64` glibc binary at `./claude` in the build context. Write your own Dockerfile per those requirements or start from the bundle's [`Dockerfile`](https://github.com/anthropics/claude-code/blob/main/examples/gateway/aws/Dockerfile), which copies the filled-in `gateway.yaml` from the previous steps into the image at `/etc/claude/gateway.yaml`. On ECS that embedded copy is how the configuration reaches the container, which is why the build comes after the file is written. The EKS track instead mounts `gateway.yaml` from a ConfigMap at deploy, so the embedded copy is unused there.

    The image also carries the AWS RDS certificate bundle as the trust anchor for the connection string's `sslmode=verify-full`, so download it into the build context first. AWS rotates the bundle (new regional CAs get appended), so download it per build rather than pinning a checksum or committing it:

    ```bash theme={null}
    curl -fL --proto '=https' -o rds-global-bundle.pem \
      https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
    ```

    The container image requirements don't cover the bundle, so if you write your own Dockerfile, add the two lines that copy and trust it; the bundle's `Dockerfile` already includes both:

    ```dockerfile theme={null}
    COPY rds-global-bundle.pem /etc/claude/rds-global-bundle.pem
    ENV NODE_EXTRA_CA_CERTS=/etc/claude/rds-global-bundle.pem
    ```

    Create the ECR repository and sign Docker in to it. Immutable tags mean the `<version>` tag the deploy step pins cannot later be silently re-pointed at a different image:

    ```bash theme={null}
    aws ecr create-repository --repository-name claude-gateway \
      --image-tag-mutability IMMUTABLE \
      --image-scanning-configuration scanOnPush=true
    aws ecr get-login-password --region "$AWS_REGION" \
      | docker login --username AWS --password-stdin \
        "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    ```

    Build and push the image. The task definition below runs `linux/amd64`, so the platform must match here; for Fargate on ARM64 (Graviton), build `linux/arm64` with the `linux-arm64` binary and set `cpuArchitecture` to `ARM64` instead:

    ```bash theme={null}
    docker build --platform=linux/amd64 \
      -t "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/claude-gateway:<version>" .
    docker push "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/claude-gateway:<version>"
    ```
  </Step>

  <Step title="Deploy">
    <Tabs>
      <Tab title="ECS Fargate">
        Create the cluster and a log group for the gateway's stderr, which carries both its audit events and operational logs. Retention is a separate call, and without one CloudWatch keeps the logs forever; align the 90 days with your audit retention policy:

        ```bash theme={null}
        aws ecs create-cluster --cluster-name claude-gateway
        aws logs create-log-group --log-group-name /ecs/claude-gateway
        aws logs put-retention-policy --log-group-name /ecs/claude-gateway \
          --retention-in-days 90
        ```

        Write the task definition. The task role carries the Bedrock permission and the execution role injects the secrets; use the secret ARNs from the Secrets Manager step:

        ```json claude-gateway-task.json theme={null}
        {
          "family": "claude-gateway",
          "networkMode": "awsvpc",
          "requiresCompatibilities": ["FARGATE"],
          "cpu": "1024",
          "memory": "2048",
          "runtimePlatform": { "cpuArchitecture": "X86_64", "operatingSystemFamily": "LINUX" },
          "executionRoleArn": "arn:aws:iam::<account-id>:role/claude-gateway-execution",
          "taskRoleArn": "arn:aws:iam::<account-id>:role/claude-gateway-task",
          "containerDefinitions": [
            {
              "name": "gateway",
              "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/claude-gateway:<version>",
              "portMappings": [{ "containerPort": 8080 }],
              "secrets": [
                { "name": "GATEWAY_JWT_SECRET",   "valueFrom": "<gateway-jwt-secret ARN>" },
                { "name": "OIDC_CLIENT_SECRET",   "valueFrom": "<gateway-oidc-client-secret ARN>" },
                { "name": "GATEWAY_POSTGRES_URL", "valueFrom": "<gateway-postgres-url ARN>" }
              ],
              "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                  "awslogs-group": "/ecs/claude-gateway",
                  "awslogs-region": "<region>",
                  "awslogs-stream-prefix": "gateway"
                }
              }
            }
          ]
        }
        ```

        Register it:

        ```bash theme={null}
        aws ecs register-task-definition --cli-input-json file://claude-gateway-task.json
        ```

        Put an internal ALB in front with a target group that health-checks the gateway. `--ip-address-type ipv4` matters: an internal dual-stack ALB publishes public-range AAAA records, which the `/login` private-network check rejects:

        ```bash theme={null}
        ALB_ARN="$(aws elbv2 create-load-balancer --name claude-gateway \
          --scheme internal --type application --ip-address-type ipv4 \
          --subnets $PRIVATE_SUBNETS --security-groups "$ALB_SG" \
          --query 'LoadBalancers[0].LoadBalancerArn' --output text)"

        TG_ARN="$(aws elbv2 create-target-group --name claude-gateway \
          --protocol HTTP --port 8080 --vpc-id "$VPC_ID" --target-type ip \
          --health-check-path /readyz \
          --query 'TargetGroups[0].TargetGroupArn' --output text)"
        ```

        Add the HTTPS listener and raise the idle timeout. `--ssl-policy` pins a modern TLS floor, since omitting it falls back to the legacy `ELBSecurityPolicy-2016-08` default, which still accepts TLS 1.0/1.1. The idle timeout matters for streaming: the ALB closes a connection after 60 seconds with no data by default, which cuts off streams during quiet periods, such as long prompt processing before the first token:

        ```bash theme={null}
        aws elbv2 create-listener --load-balancer-arn "$ALB_ARN" \
          --protocol HTTPS --port 443 \
          --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06 \
          --certificates CertificateArn=<your-acm-certificate-arn> \
          --default-actions Type=forward,TargetGroupArn="$TG_ARN"

        aws elbv2 modify-load-balancer-attributes --load-balancer-arn "$ALB_ARN" \
          --attributes Key=idle_timeout.timeout_seconds,Value=3600
        ```

        Create the service. The deployment circuit breaker rolls a deployment whose tasks keep failing, from a bad image or an unbootable config, back to the last steady state instead of relaunching failing tasks forever:

        ```bash theme={null}
        aws ecs create-service --cluster claude-gateway --service-name claude-gateway \
          --task-definition claude-gateway --desired-count 1 --launch-type FARGATE \
          --deployment-configuration "deploymentCircuitBreaker={enable=true,rollback=true}" \
          --health-check-grace-period-seconds 60 \
          --network-configuration "awsvpcConfiguration={subnets=[$(echo $PRIVATE_SUBNETS | tr ' ' ',')],securityGroups=[$GW_SG],assignPublicIp=DISABLED}" \
          --load-balancers "targetGroupArn=$TG_ARN,containerName=gateway,containerPort=8080"
        ```

        The 60-second grace period gives a cold task time to pull the image, connect to the store, and answer its first health check before ECS starts counting failures against the deployment. The target group's health check on `GET /readyz` verifies the store is reachable, so a task that can't reach Postgres never enters rotation; see [Outage behavior](/docs/en/claude-apps-gateway-deploy#outage-behavior) for the tradeoff and the `/healthz` alternative.

        The tasks run in private subnets with no public IP, so all egress (to Bedrock, your IdP, Secrets Manager, ECR, and CloudWatch Logs) goes through the NAT gateway. To keep Bedrock traffic off the public path, create a `bedrock-runtime` interface VPC endpoint and point the upstream's `base_url` at it, as shown in the [Bedrock upstream reference](/docs/en/claude-apps-gateway-config#amazon-bedrock); the IdP still needs internet egress.

        Finish by giving developers a privately resolvable hostname: in a Route 53 private hosted zone, alias the gateway's internal DNS name to the ALB, and set `listen.public_url` to that hostname. The ALB's own `*.elb.amazonaws.com` name resolves to private addresses on an internal ALB, but it can't carry your ACM certificate, so use your own name.

        Update the OAuth client's authorized redirect URI to `<public_url>/oauth/callback` before the first sign-in. After changing `public_url`, rebuild and push the image under a new tag, register a new task definition revision, and redeploy. On ECS the setting lives in the image's embedded `gateway.yaml`, and the gateway builds its public origin only from that setting, ignoring `X-Forwarded-Host` and `X-Forwarded-Proto`. `X-Forwarded-For` is honored for client IPs only when `listen.trusted_proxies` is set.
      </Tab>

      <Tab title="EKS">
        This track needs `kubectl` and `eksctl` installed locally, and an existing EKS cluster with an IAM OIDC provider and the AWS Load Balancer Controller installed. The cluster must be on `$VPC_ID` so pods can reach the RDS private endpoint, and the `claude-gateway-db` security group must admit the cluster's pod or node security group in place of `$GW_SG`.

        On EKS the gateway gets its Bedrock credentials through IRSA rather than the ECS roles. The `ecs-tasks.amazonaws.com` trust policy from the IAM step does not apply here; IRSA needs a role whose trust policy federates on the cluster's OIDC provider, scoped to `system:serviceaccount:claude-gateway:gateway`. `eksctl create iamserviceaccount` creates that role, attaches the policies, and annotates the Kubernetes service account with the role ARN in one step. Turn the two policy documents from the IAM step into managed policies it can attach:

        ```bash theme={null}
        BEDROCK_POLICY_ARN="$(aws iam create-policy --policy-name claude-gateway-bedrock-invoke \
          --policy-document file://bedrock-invoke.json --query Policy.Arn --output text)"
        SECRETS_POLICY_ARN="$(aws iam create-policy --policy-name claude-gateway-secrets-read \
          --policy-document file://secrets-read.json --query Policy.Arn --output text)"

        kubectl create namespace claude-gateway
        eksctl create iamserviceaccount --cluster <your-cluster> --region "$AWS_REGION" \
          --namespace claude-gateway --name gateway --role-name claude-gateway \
          --attach-policy-arn "$BEDROCK_POLICY_ARN" \
          --attach-policy-arn "$SECRETS_POLICY_ARN" \
          --approve
        ```

        The secrets policy is needed only when the pods read Secrets Manager themselves, as the Secrets Store CSI driver's AWS provider does using the mounting pod's service account; drop it if you create the Kubernetes Secrets another way. The provider needs both of the policy's actions: it calls `DescribeSecret` when it reconciles rotated secrets, so a `GetSecretValue`-only grant mounts on the first deploy but stops picking up rotations.

        Deploy the gateway as a standard Deployment plus a Service and an Ingress, as described in [Kubernetes deployment](/docs/en/claude-apps-gateway-deploy#kubernetes), with:

        * `serviceAccountName: gateway`
        * `gateway.yaml` mounted from a ConfigMap and the secrets mounted at `/secrets`
        * the readiness probe pointed at `GET /readyz`

        For the front end, an Ingress managed by the AWS Load Balancer Controller provisions the internal ALB. Annotate it with:

        * `alb.ingress.kubernetes.io/scheme: internal` and `alb.ingress.kubernetes.io/target-type: ip`
        * `alb.ingress.kubernetes.io/ip-address-type: ipv4`, so no public-range AAAA records are published for the `/login` [private-network check](/docs/en/claude-apps-gateway#prerequisites) to reject
        * `alb.ingress.kubernetes.io/inbound-cidrs: <your-corporate-cidr>`, so the controller-managed frontend security group admits only your corporate network in place of its `0.0.0.0/0` default
        * `alb.ingress.kubernetes.io/certificate-arn` with the ACM certificate
        * `alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS13-1-2-2021-06`, so the listener doesn't fall back to the legacy default policy that accepts TLS 1.0 and 1.1
        * `alb.ingress.kubernetes.io/load-balancer-attributes: idle_timeout.timeout_seconds=3600`, so a 60-second data gap in a stream doesn't close the connection

        With IRSA, the AWS SDK reads a projected service-account token and exchanges it with AWS STS, so the pod never needs the EC2 instance metadata service; an egress NetworkPolicy may block `169.254.169.254` for gateway pods. The node hop-limit problem in [Troubleshooting](#troubleshooting) below applies only to clusters that skip IRSA and rely on node instance roles.
      </Tab>
    </Tabs>
  </Step>

  <Step title="Push the gateway URL to developer machines">
    The gateway is now running, but developers can't reach it from `/login` until the gateway URL is on their machines. Set `forceLoginMethod` and `forceLoginGatewayUrl` in the [managed settings file](/docs/en/claude-apps-gateway#set-the-gateway-url) you deploy to each device via MDM. There is no gateway option in the login picker for a developer to select manually.
  </Step>
</Steps>

## Terraform reference

The companion bundle at [`examples/gateway/aws`](https://github.com/anthropics/claude-code/tree/main/examples/gateway/aws) packages this page as code:

* **`setup.sh`** scripts the provisioning walkthrough above with the same `aws` commands, on the ECS Fargate track. It is idempotent: existing resources are detected and skipped, so re-running it is safe, and any default can be overridden via environment variable. You still create the Okta OIDC client secret and the ACM certificate yourself: a run without them skips the ECS/ALB deploy, names the missing inputs, and prints the `create-secret` command; create both and re-run. The Bedrock use case form and the Route 53 alias print as next steps rather than running automatically, and the client MDM push stays a manual step from this page.
* **`gateway.yaml.example`** is the configuration template from the gateway.yaml step, with the optional keys included commented out. Copy it to `gateway.yaml` and replace every `REPLACE_ME` before building.
* **`Dockerfile`** builds the runtime image from the prebuilt `linux-x64` binary and copies in your filled-in `gateway.yaml` at `/etc/claude/gateway.yaml`, plus the AWS RDS certificate bundle that anchors the store's `sslmode=verify-full`. `setup.sh` downloads the bundle only when it isn't already in the build context; delete the file and rebuild under a new tag to pick up an AWS CA rotation. The config file holds no secret values, since every credential resolves at boot through `${VAR}` expansion. A config edit therefore means a rebuild under a new tag; `setup.sh` automates this by tagging images with a hash of the file.
* **`terraform/`** provisions the same ECS Fargate scope declaratively: the security groups, IAM roles, ECR repository, RDS instance, Secrets Manager secrets, and the ECS service behind the internal ALB. The VPC and private subnets stay prerequisites, passed in as variables. Terraform creates the ECR repository but doesn't build the image, and the service definition references the image, so the apply is two passes: a targeted apply for the repository, then the build and push, then the full apply. The bundle's `terraform/README.md` covers the variables, remote state, and teardown.

Like this page, the bundle is a working example for customer-managed infrastructure rather than a supported production deployment; review and adapt it to your own environment before relying on it.

## Troubleshooting

For gateway boot and login errors, see the platform-agnostic [troubleshooting table](/docs/en/claude-apps-gateway-deploy#troubleshooting). The entries below are specific to AWS.

| Symptom                                                                                                                                    | Cause                                                                                                                                                                                                                                                                                                                  | Fix                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CLI `/login`: `Gateway hosts must be on your organization's private network; <host> resolves to the public (or unrecognized) address <ip>` | The gateway name resolves to at least one public address. A dual-stack internal ALB publishes public-range AAAA records, and the [private-network check](/docs/en/claude-apps-gateway#prerequisites) requires every resolved address to be private                                                                          | Create the ALB with `--ip-address-type ipv4`, or serve a separate internal-only DNS name with no public AAAA record                                                                                                                                                                                            |
| Every Bedrock request returns 502; log shows `Could not load credentials from any providers`                                               | The task runs on the ECS EC2 launch type without a task role, or the pod runs on an EKS node without IRSA, so credentials come from instance metadata, which IMDSv2's default hop limit of 1 stops inside a container. Neither track on this page is affected: Fargate task roles and IRSA don't use instance metadata | Prefer task roles and IRSA. Where instance credentials are unavoidable, raise the hop limit with `aws ec2 modify-instance-metadata-options --instance-id <id> --http-put-response-hop-limit 2`; the [platform-agnostic table](/docs/en/claude-apps-gateway-deploy#troubleshooting) covers the tradeoffs             |
| Bedrock requests return `403 AccessDeniedException`                                                                                        | The account hasn't submitted Anthropic's one-time use case form, the automatic AWS Marketplace subscription that starts on the account's first invoke hasn't finished yet, or the task role's policy is missing the inference-profile or foundation-model ARNs                                                         | Submit the use case form from the Bedrock console's Model catalog; if it was just submitted or this is the account's first invoke, retry after a few minutes. Grant `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on both ARN families.                                                    |
| Bedrock returns a `ValidationException` saying on-demand throughput isn't supported                                                        | A custom `models:` entry maps to a bare foundation-model ID that the region serves only through inference profiles                                                                                                                                                                                                     | Map the model to its cross-region inference profile ID (`us.anthropic.*`) instead; the built-in catalog already does this                                                                                                                                                                                      |
| ECS task stops with `ResourceInitializationError` before the gateway logs anything                                                         | The execution role can't read the Secrets Manager secrets, or the private subnets have no path to Secrets Manager or ECR                                                                                                                                                                                               | Grant `secretsmanager:GetSecretValue` on the three `gateway-` secrets' ARNs to the execution role, and provide egress via the NAT gateway, or, without one, interface endpoints for Secrets Manager, ECR, and CloudWatch Logs, which the `awslogs` driver needs at the same stage, plus an S3 gateway endpoint |
| Gateway boot exits with a Postgres connection-timeout error                                                                                | The database security group doesn't admit the gateway's security group on 5432, or the service runs outside the database's VPC; the store stops waiting after 5 seconds                                                                                                                                                | Allow 5432 from the gateway's security group on the database's, and run the service in the same VPC as the DB subnet group                                                                                                                                                                                     |
| Gateway boot exits with a Postgres TLS certificate verification error                                                                      | The connection string sets `sslmode=verify-full` but the image doesn't trust the RDS CA bundle: the bundle wasn't copied into the image, or `NODE_EXTRA_CA_CERTS` doesn't point at it                                                                                                                                  | Add the build step's two Dockerfile lines that copy the bundle and set `NODE_EXTRA_CA_CERTS`, then rebuild, push under a new tag, and redeploy                                                                                                                                                                 |
| Streaming responses drop mid-stream after a quiet period                                                                                   | The ALB idle timeout closes the connection after 60 seconds with no data by default. A stream that is actively emitting tokens isn't affected; one that goes quiet, during long prompt processing before the first token or extended thinking with no streamed output, is cut at the gap                               | Set the `idle_timeout.timeout_seconds` attribute to `3600`, via `modify-load-balancer-attributes` or the `load-balancer-attributes` Ingress annotation on EKS                                                                                                                                                  |

## Telemetry

The gateway gives you per-developer usage metrics without any per-machine OTEL configuration. Claude Code emits OpenTelemetry (OTLP) metrics, logs, and opt-in traces; [Monitoring usage](/docs/en/monitoring-usage) covers everything the CLI reports. On gateway sessions the CLI stamps each export with the authenticated IdP identity attributes `user.id`, `user.email`, and `user.groups`, so usage rolls up per developer with no `OTEL_RESOURCE_ATTRIBUTES` plumbing.

The gateway itself is an authenticated OTLP relay. Set [`telemetry.forward_to`](/docs/en/claude-apps-gateway-config#telemetry) together with `listen.public_url`, and it pushes the OTEL exporter settings to every connected client and forwards their OTLP traffic verbatim to each destination you list. Each destination opts into metrics, logs, and traces independently, and the default is metrics only; see the [`telemetry` reference](/docs/en/claude-apps-gateway-config#telemetry) for the per-signal fields and their sensitivity tradeoffs. The gateway doesn't buffer, aggregate, or store telemetry, so where the data lands is entirely the collector's exporter configuration.

Client telemetry is off by default; configuring `telemetry.forward_to` is what turns it on for connected developers, and each interactive client shows a one-time security approval dialog for the pushed settings, as described in the [configuration reference](/docs/en/claude-apps-gateway-config#telemetry). On AWS, each signal maps to a destination as follows.

### Client metrics, logs, and traces

Point `telemetry.forward_to` at an OpenTelemetry collector, such as the [AWS Distro for OpenTelemetry (ADOT) collector](https://aws-otel.github.io/), and export from there to Amazon CloudWatch, Amazon Managed Service for Prometheus, or any OTLP backend.

Run the collector as its own internal service reachable over `https://`: the gateway accepts plaintext `http://` only for loopback URLs, and even then its [SSRF guard](/docs/en/claude-apps-gateway-deploy#threat-model-summary) blocks loopback connections by default. Unless `CLAUDE_GATEWAY_ALLOW_LOOPBACK=1` is set in the gateway's environment, a sidecar collector on `http://localhost:4318` passes config validation but receives no traffic, with exports failing as `ECONNREFUSED_SSRF` in the gateway logs, and the gateway rejects an IP-literal URL such as `http://127.0.0.1:4318` at boot. That variable relaxes the loopback block for every operator-configured URL, not only telemetry, so prefer the internal-service pattern and reserve the sidecar-plus-flag setup for tasks whose network is otherwise locked down.

### Gateway logs

On ECS Fargate, no extra setup: the `awslogs` driver delivers the gateway's stderr, which carries its audit events and operational logs, to the `/ecs/claude-gateway` log group created above. On EKS, pod logs don't reach CloudWatch by default, so the audit trail is lost until you install log collection: the Amazon CloudWatch Observability add-on with container log capture enabled, or a Fluent Bit DaemonSet. On either track, query the logs with CloudWatch Logs Insights and drive alarms from metric filters.

### Container metrics

Enable Container Insights on the cluster with `aws ecs update-cluster-settings --cluster claude-gateway --settings name=containerInsights,value=enabled` for per-task CPU, memory, and network. On EKS, install the Amazon CloudWatch Observability add-on.

### Spend

Telemetry shows usage after the fact; [spend limits](/docs/en/claude-apps-gateway-spend-limits) are the gateway's live per-developer view and enforcement on top of the shared upstream credential.

## Next steps

* [Configuration reference](/docs/en/claude-apps-gateway-config): every `gateway.yaml` option, including `managed.policies` and `telemetry`
* [Deployment and operations](/docs/en/claude-apps-gateway-deploy): IdP setup, health checks, JWT secret rotation, upgrades, and the security model
* [Claude apps gateway overview](/docs/en/claude-apps-gateway): quickstart and connecting developers
* [AWS samples for Claude apps gateway](https://github.com/aws-samples/anthropic-on-aws/tree/main/claude-apps-gateway): AWS-maintained deployment samples covering a range of customer environments
