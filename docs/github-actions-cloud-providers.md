> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code GitHub Actions with cloud providers

> Run Claude Code GitHub Actions through Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry instead of the Claude API

[Claude Code GitHub Actions](/docs/en/github-actions) calls the Claude API by default. To route inference through your own cloud account instead, set the Claude Code GitHub Action's provider input and configure your cloud to trust the workflow's OpenID Connect (OIDC) token. The workflow authenticates with that token, so you store no long-lived cloud credential in your repository.

<Info>
  This page builds on the [GitHub Actions setup](/docs/en/github-actions#setup). It assumes you already know the workflow file and the `anthropics/claude-code-action` step, and covers only what a cloud provider changes.
</Info>

## Choose your provider

The Claude Code GitHub Action supports three providers, and the setup steps below differ only in the cloud-side configuration. Use the one where your organization already has Claude model access. You tell the Claude Code GitHub Action which provider to use with one input in the `anthropics/claude-code-action` step's `with:` block:

* **Amazon Bedrock**: `use_bedrock: "true"`
* **Google Cloud's Agent Platform**: `use_vertex: "true"`
* **Microsoft Foundry**: `use_foundry: "true"`

The following snippet shows the input in place for Amazon Bedrock. You don't need to edit a workflow yet, because the complete workflow examples later on this page already include the input for each provider.

```yaml theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    use_bedrock: "true"
```

## Prerequisites

Before you start, you need:

* Admin access to the repository where the Claude Code GitHub Action runs, to install a GitHub App and add secrets
* Permission to create identity resources in your cloud account: IAM roles and OIDC identity providers on AWS, Workload Identity Federation resources and service accounts on Google Cloud, or Microsoft Entra applications on Azure
* Claude model access on your provider:
  * **Amazon Bedrock**: access granted to Claude models. Cross-region inference profiles, such as the `us.` model IDs in this page's examples, need access granted in every region of their region group. See [Claude Code on Amazon Bedrock](/docs/en/amazon-bedrock)
  * **Google Cloud's Agent Platform**: a project with the Agent Platform API enabled and access to Claude models. See [Claude Code on Google Cloud's Agent Platform](/docs/en/google-vertex-ai)
  * **Microsoft Foundry**: a Foundry resource with a Claude model deployment. See [Claude Code on Microsoft Foundry](/docs/en/microsoft-foundry)

## Set up the integration

Beyond the prerequisites, you create four things: a GitHub identity for the Claude Code GitHub Action, the cloud-side trust configuration, the repository secrets, and the workflow file. The steps below walk through each.

<Steps>
  <Step title="Choose a GitHub identity">
    The Claude Code GitHub Action pushes commits and posts comments through a GitHub identity. The [quick setup](/docs/en/github-actions#quick-setup) installs the official Claude GitHub App for this. With a cloud provider, you choose the identity yourself:

    * **Official [Claude GitHub App](https://github.com/apps/claude)**: install it on the repository, or skip to the next step if it's already installed
    * **Custom GitHub App**: create your own app, described below, when you want only the three permissions the Claude Code GitHub Action uses rather than the [official app's full set](/docs/en/github-actions#github-app-permissions)
    * **GitHub's automatic `GITHUB_TOKEN`**: no app to create or install, but GitHub doesn't trigger your CI workflows on commits made with it

    The workflow examples in the fourth step authenticate with a custom app. That step also says what to change for the other two options.

    To create a custom app, [register a new GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) with webhooks disabled, since this integration doesn't use them. Grant it three repository permissions:

    * **Contents**: read and write
    * **Issues**: read and write
    * **Pull requests**: read and write

    After registering the app, generate a private key and keep the downloaded `.pem` file, note the App ID from the app's settings page, and [install the app](https://docs.github.com/en/apps/using-github-apps/installing-your-own-github-app) on the repository where the Claude Code GitHub Action runs. You add the key and the ID as secrets in the third step.
  </Step>

  <Step title="Configure cloud authentication">
    Configure your cloud to trust the OIDC token that GitHub issues to the workflow, so each workflow run gets short-lived cloud credentials. The bullets in each tab summarize what to create, and each tab links the cloud vendor's own guide for the console-level steps.

    <Tabs>
      <Tab title="Amazon Bedrock">
        Create the trust configuration in your AWS account, following the [AWS guide to creating OIDC identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html):

        * Add a GitHub OIDC identity provider with provider URL `https://token.actions.githubusercontent.com` and audience `sts.amazonaws.com`
        * Create an IAM role trusted by that provider as a web identity, and attach the scoped invocation policy from [IAM configuration](/docs/en/amazon-bedrock#iam-configuration), which grants `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`, `bedrock:ListInferenceProfiles`, and `bedrock:GetInferenceProfile`, along with two `aws-marketplace` subscription actions
        * Limit the role's trust policy to your repository with a subject condition such as `repo:your-org/your-repo:*`. See [GitHub's OIDC hardening guide](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) for the claim format

        Note the role's ARN. You add it as a secret in the next step.
      </Tab>

      <Tab title="Google Cloud's Agent Platform">
        Create the federation resources in your Google Cloud project, following the [Workload Identity Federation documentation](https://cloud.google.com/iam/docs/workload-identity-federation):

        * Enable three APIs: IAM Credentials, Security Token Service (STS), and the Agent Platform API, whose service name is `aiplatform.googleapis.com`
        * Create a Workload Identity Pool with a GitHub OIDC provider whose issuer is `https://token.actions.githubusercontent.com`, and add an attribute condition that limits the pool to your repository
        * Create a dedicated service account with only the `Vertex AI User` role, which is `roles/aiplatform.user`, and allow the pool to impersonate it

        Note the provider's full resource name and the service account's email address. You add them as secrets in the next step.
      </Tab>

      <Tab title="Microsoft Foundry">
        Create a Microsoft Entra application with a federated credential for your repository, following [Microsoft's guide to authenticating from GitHub Actions](https://learn.microsoft.com/en-us/azure/developer/github/connect-from-azure-openid-connect):

        * Register a Microsoft Entra application and add a federated identity credential that trusts tokens GitHub issues to your repository. A user-assigned managed identity works in place of an application. Both have the client ID you note below
        * Assign the application the `Azure AI User` role on your Foundry resource. See [Azure RBAC configuration](/docs/en/microsoft-foundry#azure-rbac-configuration) for a narrower custom role

        Note the application's client ID, your tenant ID, and your subscription ID. You add them as secrets in the next step.
      </Tab>
    </Tabs>
  </Step>

  <Step title="Add repository secrets">
    In the repository where the Claude Code GitHub Action runs, add the secrets for your provider, plus the two app secrets if you created a custom GitHub App in the first step. See GitHub's guide to [using secrets in GitHub Actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).

    | Secret                           | Needed for                    | Value                                       |
    | -------------------------------- | ----------------------------- | ------------------------------------------- |
    | `AWS_ROLE_TO_ASSUME`             | Amazon Bedrock                | The ARN of the IAM role                     |
    | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Google Cloud's Agent Platform | The provider's full resource name           |
    | `GCP_SERVICE_ACCOUNT`            | Google Cloud's Agent Platform | The service account's email address         |
    | `AZURE_CLIENT_ID`                | Microsoft Foundry             | The Entra application's client ID           |
    | `AZURE_TENANT_ID`                | Microsoft Foundry             | Your Microsoft Entra tenant ID              |
    | `AZURE_SUBSCRIPTION_ID`          | Microsoft Foundry             | Your Azure subscription ID                  |
    | `APP_ID`                         | Custom GitHub App             | The GitHub App's ID                         |
    | `APP_PRIVATE_KEY`                | Custom GitHub App             | The contents of the `.pem` private key file |
  </Step>

  <Step title="Create the workflow file">
    Create a workflow file for your provider, such as `.github/workflows/claude.yml`. Each example responds to `@claude` mentions, authenticates to GitHub with a custom app, and includes the `id-token: write` permission, which GitHub requires to issue the OIDC token that your cloud provider exchanges for credentials.

    If you chose a different GitHub identity in the first step, adjust the example:

    * **Official Claude GitHub App**: delete the Generate GitHub App token step and the `github_token` line
    * **GitHub's automatic token**: delete the token-generation step and change the `github_token` line to `github_token: ${{ secrets.GITHUB_TOKEN }}`

    <Warning>
      On public repositories, a comment containing the trigger phrase from any user starts this workflow. The credential steps run before the Claude Code GitHub Action checks the commenter's write access, so the action rejects unauthorized users only after the workflow has generated an App token and signed in to your cloud provider, which leaves audit-log entries and consumes Actions minutes. To avoid those runs, add a step that verifies the commenter's write access before the credential steps.
    </Warning>

    <Tabs>
      <Tab title="Amazon Bedrock">
        Replace the `aws-region` value with your own. The credentials step exports it as `AWS_REGION` for the rest of the job.

        ```yaml theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && (contains(github.event.issue.body, '@claude') || contains(github.event.issue.title, '@claude')))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v6

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  claude_args: '--model us.anthropic.claude-sonnet-4-6'
        ```

        <Tip>
          Bedrock model IDs include a cross-region inference profile prefix such as `us.`. Use the prefix for the region group where you granted model access.
        </Tip>
      </Tab>

      <Tab title="Google Cloud's Agent Platform">
        Replace the `CLOUD_ML_REGION` value with your own. You don't need to hardcode the project ID, because the workflow reads it from the `auth` step's output.

        ```yaml theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && (contains(github.event.issue.body, '@claude') || contains(github.event.issue.title, '@claude')))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v6

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_vertex: "true"
                  claude_args: '--model claude-sonnet-5'
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
        ```
      </Tab>

      <Tab title="Microsoft Foundry">
        Replace `your-resource-name` with your Foundry resource name. Claude Code builds the endpoint URL from it. The `azure/login` step signs in with the workflow's OIDC token, and Claude Code picks up the credentials through the Azure [default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).

        ```yaml theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && (contains(github.event.issue.body, '@claude') || contains(github.event.issue.title, '@claude')))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v6

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Azure
                uses: azure/login@v2
                with:
                  client-id: ${{ secrets.AZURE_CLIENT_ID }}
                  tenant-id: ${{ secrets.AZURE_TENANT_ID }}
                  subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_foundry: "true"
                  claude_args: '--model claude-sonnet-5'
                env:
                  ANTHROPIC_FOUNDRY_RESOURCE: your-resource-name
        ```

        <Tip>
          Use a model ID that matches a Claude deployment in your Foundry resource. See [Claude Code on Microsoft Foundry](/docs/en/microsoft-foundry) for model configuration and version pinning.
        </Tip>
      </Tab>
    </Tabs>

    With any provider, you can bound run length and cost by adding `--max-turns` to `claude_args`. See [Manage costs](/docs/en/github-actions#manage-costs).
  </Step>

  <Step title="Test the setup">
    Mention `@claude` in an issue or PR comment, then watch the run in the repository's Actions tab. Claude replies in a comment on the same issue or PR.
  </Step>
</Steps>

## Troubleshooting

A failing run usually breaks in one of two places:

* **Authentication errors**: usually an OIDC misconfiguration. Check that the workflow includes the `id-token: write` permission, that the trust configuration's repository condition matches your repository exactly, and that the secret names in your workflow match the ones you added
* **Trigger and CI problems**: these behave the same as when the Claude Code GitHub Action calls the Claude API. See the main page's [troubleshooting section](/docs/en/github-actions#troubleshooting) and the Claude Code GitHub Action's [FAQ](https://github.com/anthropics/claude-code-action/blob/main/docs/faq.md)

## What's next

* [Claude Code GitHub Actions](/docs/en/github-actions) for examples, parameters, and best practices
* [Claude Code on Amazon Bedrock](/docs/en/amazon-bedrock) for Bedrock model IDs and regions
* [Claude Code on Google Cloud's Agent Platform](/docs/en/google-vertex-ai) for Agent Platform model IDs and regions
* [Claude Code on Microsoft Foundry](/docs/en/microsoft-foundry) for Foundry model and endpoint configuration
