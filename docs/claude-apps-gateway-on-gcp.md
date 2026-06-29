> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploy Claude apps gateway on Google Cloud

> A worked example of running Claude apps gateway on Google Cloud: Cloud Run or GKE, Cloud SQL for PostgreSQL, Secret Manager, and service-account auth to Agent Platform.

<Note>
  This page walks through one way to run Claude apps gateway on Google Cloud. The configuration is a working example for customer-managed infrastructure rather than a supported production deployment; use it to see how the pieces fit together before adapting it to your own environment. For the platform-agnostic requirements, see the [deployment guide](/en/claude-apps-gateway-deploy).
</Note>

This example provisions Claude apps gateway on Google Cloud with Google Cloud's Agent Platform as the model upstream, using either Cloud Run or GKE for compute. Google Workspace is the example identity provider (IdP), but any OpenID Connect (OIDC) compliant IdP works; only the `oidc` block changes. See [Identity provider setup](/en/claude-apps-gateway-deploy#identity-provider-setup) for per-IdP details.

## What you'll build

<Frame>
  <img src="https://mintcdn.com/claude-code/-uq-4JE0W_JO5Er5/images/claude-gateway-gcp-architecture.svg?fit=max&auto=format&n=-uq-4JE0W_JO5Er5&q=85&s=cb705151c69128ac0da235852d5600ab" alt="Diagram of Claude apps gateway on Google Cloud: Claude Code clients connect over HTTPS to the gateway (Cloud Run or GKE), which runs inside a VPC alongside a private-IP Cloud SQL database for session state. The gateway signs users in via OIDC against Google Workspace, reads config and secrets from Secret Manager, forwards model requests to Agent Platform, and pulls its image from Artifact Registry at deploy." width="760" height="400" data-path="images/claude-gateway-gcp-architecture.svg" />
</Frame>

The reference configuration provisions:

* **Cloud Run** service or **GKE** Deployment running the gateway container
* **Artifact Registry** repository for the gateway image
* **Cloud SQL for PostgreSQL** instance, private IP only, for the gateway's [store](/en/claude-apps-gateway-config#store)
* **Secret Manager** secrets for `gateway.yaml`, the JWT signing key, the OIDC client secret, and the Postgres URL
* **Service account** with `roles/aiplatform.user`, attached directly on Cloud Run or bound via Workload Identity on GKE
* **Internal Application Load Balancer** on Cloud Run, or an internal **GKE Ingress** of class `gce-internal` on GKE, for HTTPS

## Prerequisites

* A GCP project with billing enabled, and permission to create the resources above
* The `gcloud` CLI, authenticated with `gcloud auth login`, and Docker installed locally
* For the GKE track: `kubectl`, and a GKE cluster on the VPC created in the walkthrough below
* Access to the Claude models you need in Model Garden, in a region that publishes them
* A Google Workspace OAuth 2.0 web-application client with redirect URI `https://<gateway-host>/oauth/callback`; see [Identity provider setup](/en/claude-apps-gateway-deploy#identity-provider-setup)
* A TLS hostname for the gateway, typically an internal DNS name pointing at the load balancer

Set the project and region once:

```bash theme={null}
export PROJECT_ID=<your-project>
export REGION=us-east5   # a region where the Claude models you need are published in Model Garden
gcloud config set project "$PROJECT_ID"
```

## Deploy the gateway

The steps below provision the full deployment with `gcloud` commands.

<Steps>
  <Step title="Enable APIs">
    Enable the service APIs the walkthrough uses:

    ```bash theme={null}
    gcloud services enable \
      aiplatform.googleapis.com \
      artifactregistry.googleapis.com \
      sqladmin.googleapis.com \
      secretmanager.googleapis.com \
      iamcredentials.googleapis.com \
      iam.googleapis.com \
      compute.googleapis.com \
      servicenetworking.googleapis.com \
      run.googleapis.com \
      container.googleapis.com
    ```

    The APIs you need depend on the deployment path:

    * `compute` and `servicenetworking`: needed for the private-IP Cloud SQL path
    * `run`: Cloud Run only
    * `container`: GKE only
  </Step>

  <Step title="Create the service account and grant IAM">
    The gateway runs as a dedicated service account with permission to call Agent Platform. It reaches Cloud SQL over the VPC with a password user, so no Cloud SQL IAM role is required:

    ```bash theme={null}
    gcloud iam service-accounts create claude-gateway --display-name="Claude apps gateway"
    SA="claude-gateway@${PROJECT_ID}.iam.gserviceaccount.com"

    gcloud projects add-iam-policy-binding "$PROJECT_ID" \
      --member="serviceAccount:${SA}" --role="roles/aiplatform.user" --condition=None
    ```

    Then enable the Claude models for the project in Model Garden; models publish to specific regions, so check each model card.
  </Step>

  <Step title="Build and push the image to Artifact Registry">
    Build the image per the [container image requirements](/en/claude-apps-gateway-deploy#container-image), using the `linux-x64` glibc binary, and push it:

    ```bash theme={null}
    gcloud artifacts repositories create claude-gateway \
      --repository-format=docker --location="$REGION"
    gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

    # Cloud Run requires linux/amd64. --provenance=false avoids a buildx OCI
    # image index that Cloud Run rejects.
    docker build --platform=linux/amd64 --provenance=false \
      -t "${REGION}-docker.pkg.dev/${PROJECT_ID}/claude-gateway/gateway:<version>" .
    docker push "${REGION}-docker.pkg.dev/${PROJECT_ID}/claude-gateway/gateway:<version>"
    ```
  </Step>

  <Step title="Provision Cloud SQL for PostgreSQL">
    Create the instance on a VPC via Private Services Access so it has no public IP; this also satisfies projects where `constraints/sql.restrictPublicIp` is enforced:

    ```bash theme={null}
    VPC=cc-gateway-vpc
    gcloud compute networks create "$VPC" --subnet-mode=custom
    gcloud compute networks subnets create cc-gateway-subnet \
      --network="$VPC" --region="$REGION" --range=10.0.0.0/24

    # Private Services Access: one-time per VPC
    gcloud compute addresses create "google-managed-services-${VPC}" \
      --global --purpose=VPC_PEERING --prefix-length=16 --network="$VPC"
    gcloud services vpc-peerings connect \
      --service=servicenetworking.googleapis.com \
      --ranges="google-managed-services-${VPC}" --network="$VPC"

    gcloud sql instances create claude-gateway-db \
      --database-version=POSTGRES_16 --tier=db-g1-small --region="$REGION" \
      --network="projects/${PROJECT_ID}/global/networks/${VPC}" --no-assign-ip
    gcloud sql databases create claude_gateway --instance=claude-gateway-db
    PGPASS="$(openssl rand -hex 24)"
    gcloud sql users create gateway --instance=claude-gateway-db --password="$PGPASS"

    PRIVATE_IP="$(gcloud sql instances describe claude-gateway-db \
      --format='value(ipAddresses[0].ipAddress)')"
    GATEWAY_POSTGRES_URL="postgres://gateway:${PGPASS}@${PRIVATE_IP}:5432/claude_gateway?sslmode=require"
    ```

    The Cloud Run or GKE runtime must be on, or routed into, this VPC.
  </Step>

  <Step title="Write gateway.yaml">
    The `upstreams` block points at Agent Platform with `auth: {}`, so the gateway authenticates via Application Default Credentials from the runtime service account. See the [configuration reference](/en/claude-apps-gateway-config) for every field.

    Two `listen` fields depend on what fronts the gateway:

    * `public_url`: required behind Cloud Run or a GKE Ingress. The gateway builds the IdP `redirect_uri` and its discovery document only from this value, never from `X-Forwarded-*` headers.
    * `trusted_proxies`: the front end's source ranges. The gateway honors `X-Forwarded-For` only when the TCP peer is in this list, then walks the chain past trusted hops, so per-IP sign-in rate limits and audit events record developer IPs instead of the load balancer's.

    Set `trusted_proxies` to match your front end. An external GKE Ingress of class `gce` isn't listed: it provisions a public forwarding-rule address, which the `/login` [private-network check](/en/claude-apps-gateway#prerequisites) rejects.

    | Front end                                                | `trusted_proxies`                                   |
    | -------------------------------------------------------- | --------------------------------------------------- |
    | Cloud Run reached directly, no load balancer             | `[169.254.0.0/16]`                                  |
    | Internal Application Load Balancer in front of Cloud Run | `169.254.0.0/16` plus your proxy-only subnet's CIDR |
    | GKE internal Ingress, class `gce-internal`               | Your proxy-only subnet's CIDR                       |

    The example below uses the internal-load-balancer-in-front-of-Cloud-Run values.

    ```yaml gateway.yaml theme={null}
    listen:
      host: 0.0.0.0
      port: 8080
      public_url: https://claude-gateway.internal.example.com
      trusted_proxies: [169.254.0.0/16, <your-proxy-only-subnet-cidr>]

    oidc:
      issuer: https://accounts.google.com
      client_id: <your-oauth-client-id>
      client_secret: ${OIDC_CLIENT_SECRET}           # GKE: ${file:/secrets/oidc-client-secret}
      allowed_email_domains: [example.com]
      # Google ignores offline_access; these yield refresh tokens:
      scopes: [openid, profile, email]
      extra_auth_params: { access_type: offline, prompt: consent }

    session:
      jwt_secret: ${GATEWAY_JWT_SECRET}              # GKE: ${file:/secrets/jwt-secret}

    store:
      postgres_url: ${GATEWAY_POSTGRES_URL}          # GKE: ${file:/secrets/postgres-url}

    upstreams:
      - provider: vertex
        region: <your-region>                        # must match $REGION
        project_id: <your-project>
        auth: {}                                     # ADC via the runtime service account
    ```

    <Note>
      Google id\_tokens carry no `groups` claim. To use group-based policies in [`managed.policies`](/en/claude-apps-gateway-config#managed) with Google Workspace as the IdP, configure [`oidc.google_groups`](/en/claude-apps-gateway-config#oidc), which looks up each user's groups through the Admin SDK Directory API using a service account with domain-wide delegation. Without it, match on `email_domain` instead.
    </Note>
  </Step>

  <Step title="Store secrets in Secret Manager">
    Create four secrets and grant `roles/secretmanager.secretAccessor` to the `claude-gateway` service account:

    | Secret                       | Source                                          |
    | ---------------------------- | ----------------------------------------------- |
    | `gateway-jwt-secret`         | `openssl rand -base64 32`                       |
    | `gateway-oidc-client-secret` | Google Cloud Console → OAuth client             |
    | `gateway-postgres-url`       | `$GATEWAY_POSTGRES_URL` from the Cloud SQL step |
    | `gateway-config`             | the full `gateway.yaml` from the previous step  |

    How the secrets reach the container differs by track:

    * On GKE they mount as files via the Secret Manager CSI driver, and `gateway.yaml` references `${file:/secrets/...}`.
    * On Cloud Run, which can't mount multiple secrets into one directory, `gateway.yaml` mounts as a file and the other three inject as environment variables, so `gateway.yaml` references `${GATEWAY_JWT_SECRET}`, `${OIDC_CLIENT_SECRET}`, and `${GATEWAY_POSTGRES_URL}` instead.
  </Step>

  <Step title="Deploy">
    <Tabs>
      <Tab title="Cloud Run">
        The command below deploys for production behind an internal load balancer.

        ```bash theme={null}
        gcloud run deploy claude-gateway \
          --image="${REGION}-docker.pkg.dev/${PROJECT_ID}/claude-gateway/gateway:<version>" \
          --region="$REGION" \
          --service-account="claude-gateway@${PROJECT_ID}.iam.gserviceaccount.com" \
          --min-instances=1 \
          --timeout=3600 \
          --ingress=internal-and-cloud-load-balancing \
          --network="$VPC" --subnet=cc-gateway-subnet --vpc-egress=private-ranges-only \
          --set-secrets=/etc/claude/gateway.yaml=gateway-config:latest,GATEWAY_JWT_SECRET=gateway-jwt-secret:latest,OIDC_CLIENT_SECRET=gateway-oidc-client-secret:latest,GATEWAY_POSTGRES_URL=gateway-postgres-url:latest \
          --no-invoker-iam-check
        ```

        Direct VPC egress, via `--network`, `--subnet`, and `--vpc-egress=private-ranges-only`, lets the service reach the Cloud SQL private IP directly. Public egress to the Agent Platform endpoints and `accounts.google.com` goes directly to the internet rather than through the VPC, so no Cloud NAT is needed.

        The invoker IAM check must be open or disabled. The gateway runs its own OIDC and its clients carry no GCP token, so Cloud Run's invoker check has to admit unauthenticated requests. The gateway's OIDC sign-in authenticates the request once it reaches the container, with `allowed_email_domains` gating which domains may sign in.

        Two flags admit unauthenticated requests:

        * `--no-invoker-iam-check`: disables the check with no `allUsers` binding to manage, and works under Domain Restricted Sharing
        * `--allow-unauthenticated`: grants `allUsers` the `run.invoker` role; use it if your organization doesn't allow `--no-invoker-iam-check`

        Ingress restriction via `--ingress` is a separate, independent layer from the invoker check; keep it set to limit the service to your corporate network.

        By default the Cloud Run `*.run.app` URL resolves to a public address, which the `/login` [private-network check](/en/claude-apps-gateway#prerequisites) rejects. Two topologies give developers a privately resolvable hostname, and Cloud Run provisions neither for you:

        * **Internal Application Load Balancer**, the topology the deploy command above assumes: deploy with `--ingress=internal-and-cloud-load-balancing`, provision an internal Application Load Balancer in front of the service with an internal DNS name and certificate, and set `listen.public_url` to that hostname.
        * **Internal-only ingress with no load balancer**: deploy with `--ingress=internal` and leave `listen.public_url` as the `*.run.app` URL, the default in the [reference assets](#terraform-reference) below. For `*.run.app` to resolve privately, your network team must already operate a Private Service Connect endpoint for Google APIs, a Cloud DNS private zone resolving `*.run.app` to it, and on-premises routing to that endpoint.

        Google's [private networking guide for Cloud Run](https://cloud.google.com/run/docs/securing/private-networking) covers the infrastructure both options need. Verify sign-in once the gateway is serving on a private hostname; until then, confirm the container booted from its logs in Cloud Run.

        Update the OAuth client's authorized redirect URI to `<public_url>/oauth/callback` before the first sign-in. Redeploy after changing `public_url`, because the gateway builds its public origin only from that setting and ignores `X-Forwarded-Host` and `X-Forwarded-Proto`. `X-Forwarded-For` is honored for client IPs only when `listen.trusted_proxies` is set.
      </Tab>

      <Tab title="GKE">
        The cluster must be on the `$VPC` created in the Cloud SQL step so pods can reach the database's private IP; VPC peering alone doesn't work, because Cloud SQL private IP is itself a peered network and peering is non-transitive. To create a new cluster on that VPC, pass `--network="$VPC" --subnetwork=cc-gateway-subnet` to `gcloud container clusters create`.

        Enable Workload Identity on the cluster and its node pools, then bind the Google service account to the Kubernetes service account so pods inherit its credentials:

        ```bash theme={null}
        gcloud container clusters update <cluster> --region="$REGION" \
          --workload-pool="${PROJECT_ID}.svc.id.goog"
        # On a Standard cluster, existing node pools also need GKE_METADATA;
        # Autopilot enables this by default.
        gcloud container node-pools update <pool> --cluster=<cluster> \
          --region="$REGION" --workload-metadata=GKE_METADATA

        kubectl create namespace claude-gateway
        kubectl create serviceaccount gateway -n claude-gateway

        gcloud iam service-accounts add-iam-policy-binding \
          "claude-gateway@${PROJECT_ID}.iam.gserviceaccount.com" \
          --role roles/iam.workloadIdentityUser \
          --member "serviceAccount:${PROJECT_ID}.svc.id.goog[claude-gateway/gateway]"

        kubectl annotate serviceaccount gateway -n claude-gateway \
          iam.gke.io/gcp-service-account="claude-gateway@${PROJECT_ID}.iam.gserviceaccount.com"
        ```

        Deploy the gateway as a standard Deployment plus a Service and an internal Ingress, class `gce-internal`, as described in [Kubernetes deployment](/en/claude-apps-gateway-deploy#kubernetes), with:

        * `serviceAccountName: gateway`
        * the Secret Manager CSI driver mounting secrets at `/secrets`
        * the readiness probe pointed at `GET /readyz`

        Attach a BackendConfig with a raised `timeoutSec` to the gateway Service: the load balancer backend service behind GKE Ingress defaults to a 30-second timeout, which cuts off long streaming responses.

        Don't apply an egress NetworkPolicy that blocks `169.254.169.254` on a Workload Identity cluster; the pod must reach the metadata server for credentials. The gateway's built-in [SSRF guard](/en/claude-apps-gateway-deploy#threat-model-summary) is the defense there.

        The gateway logs a boot warning that the metadata endpoint is reachable and suggests applying an egress NetworkPolicy. Under Workload Identity that warning is expected, because the pod needs the endpoint.
      </Tab>
    </Tabs>
  </Step>

  <Step title="Push the gateway URL to developer machines">
    The gateway is now running, but developers can't reach it from `/login` until the gateway URL is on their machines. Set `forceLoginMethod` and `forceLoginGatewayUrl` in the [managed settings file](/en/claude-apps-gateway#set-the-gateway-url) you deploy to each device via MDM. There is no gateway option in the login picker for a developer to select manually.
  </Step>
</Steps>

## Terraform reference

The [reference deployment assets](https://github.com/anthropics/claude-code/tree/main/examples/gateway/gcp) automate the Cloud Run track on this page; the config and image assets apply to both tracks:

* `setup.sh`: an idempotent `gcloud` provisioner that walks the full Cloud Run path, from enabling APIs through the first deploy
* `terraform/`: the same deployment as infrastructure-as-code, for a greenfield deploy: a targeted apply to create the Artifact Registry repo, then build and push the image, then a full apply
* `gateway.yaml.example` and a `Dockerfile` for the distroless runtime image

The artifacts default Cloud Run ingress to `internal`, so no load balancer is required. To match this page's production-behind-an-ALB deployment, run `setup.sh` with `INGRESS=internal-and-cloud-load-balancing`, or set the Terraform variable `ingress` to `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER`. The artifacts also default the invoker layer to an `allUsers` `run.invoker` grant rather than `--no-invoker-iam-check`, the inverse of this page's walkthrough; either works, and the choice depends on your organization's policy constraints.

The assets are provided as working examples, not as a supported production artifact; review and adapt them to your environment.

## Troubleshooting

For gateway boot and login errors, see the platform-agnostic [troubleshooting table](/en/claude-apps-gateway-deploy#troubleshooting). The entries below are specific to Google Cloud.

| Symptom                                                                                  | Cause                                                                                                                               | Fix                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Cloud Run returns `403 Forbidden` before reaching the container                          | The invoker IAM check is still enabled                                                                                              | Deploy with `--no-invoker-iam-check`, or grant `allUsers` the `run.invoker` role with `--allow-unauthenticated`                                                                                                             |
| `--no-invoker-iam-check` rejected with `invoker_iam_disabled is not currently available` | Blocked by `constraints/run.managed.requireInvokerIam`                                                                              | Use `--allow-unauthenticated`. If Domain Restricted Sharing via `constraints/iam.allowedPolicyMemberDomains` blocks that too, use the GKE track, which exposes the gateway at the network layer with no `allUsers` binding. |
| `Container manifest type … must support amd64/linux` at deploy                           | Image was built on a non-amd64 host, or buildx emitted an OCI image index                                                           | Build with `--platform=linux/amd64 --provenance=false`                                                                                                                                                                      |
| Gateway boot exits with a Postgres connection-timeout error on Cloud Run                 | Service isn't attached to the VPC, or Cloud SQL has no private IP on that VPC; the store stops waiting after 5 seconds              | Deploy with `--network` and `--subnet` for Direct VPC egress, and create the Cloud SQL instance with `--no-assign-ip` and `--network` pointing at the same VPC                                                              |
| Agent Platform requests return `403 PERMISSION_DENIED`                                   | Runtime isn't using the `claude-gateway` service account, or the model isn't enabled in Model Garden for the project                | Set `--service-account` on Cloud Run or bind Workload Identity on GKE, and enable each Claude model in Model Garden for the target region                                                                                   |
| Streaming responses cut off after a fixed duration                                       | Front-end request timeout: the load balancer backend service behind GKE Ingress defaults to 30 seconds and Cloud Run to 300 seconds | Attach a BackendConfig with a raised `timeoutSec` on GKE, or deploy with `--timeout=3600` on Cloud Run                                                                                                                      |

## Next steps

* [Configuration reference](/en/claude-apps-gateway-config): every `gateway.yaml` option, including `managed.policies` and `telemetry`
* [Deployment and operations](/en/claude-apps-gateway-deploy): IdP setup, health checks, JWT secret rotation, upgrades, and the security model
* [Claude apps gateway overview](/en/claude-apps-gateway): quickstart and connecting developers
