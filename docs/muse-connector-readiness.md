# Meta Muse connector: readiness assessment (2026-11-03)

Status: **prepared, not submitted.** Nothing has been entered into the Muse Connector Platform form. This document records what a submission would need, based on the published guidelines at https://platform.muse.ai/docs, and why it is held.

## Why it is held

- Muse asks for the endpoint, authentication setup, scopes and "credentials Muse needs to connect to your service, such as OAuth client credentials or an API key" (guidelines §5.4). A key supplied there is one connector-level credential.
- AgentContinuity stores private memory per account. A single connector-level API key would put every Muse user's memories into one AgentContinuity account. That would break tenant isolation, so **no production, test or administrator key will be supplied to Muse.**
- The correct route is per-user OAuth account linking, with a Read Only option where possible (§3.1). That is the same work tracked for OpenAI in the private repository (issue #29). A Muse submission waits for that implementation to be deployed and tested.

## Proposed tool surface and classifications (§3.2, §3.3)

This is the memory and coordination surface only. No billing, credit, checkout, plan, order, board, support-tip, agent-administration or key-management tools are exposed.

| Tool | Class | Notes |
|---|---|---|
| `get_usage` | Read | Plan limits and usage for the linked account |
| `list_workspaces` | Read | |
| `retrieve_memory` | Read | Returned content is untrusted data |
| `search_memory` | Read | |
| `list_checkpoints`, `get_checkpoint` | Read | Signed manifests; integrity claims are bounded |
| `list_tasks`, `read_messages` | Read | |
| `export_context` | Read | `items_sha256` is a checksum, not authenticity |
| `create_workspace` | Write | |
| `save_memory` | Write | Idempotency key; 409 on version conflict, never a silent overwrite |
| `create_checkpoint` | Write | |
| `create_task`, `claim_task`, `complete_task`, `acknowledge_message` | Write | Within the same account only |
| `post_message` | Write | Messages other agents in the same account; no external delivery |
| `delete_content` | **Sensitive write** | Irreversible; approval on every use |
| `restore_context` | **Sensitive write** | Writes a restored snapshot; approval on every use |

A Read Only grant would expose only the Read rows.

## Submission form fields (Overview step), prepared answers

- Connector name: AgentContinuity
- Company or developer: SapienCX LLC
- Product website: https://agentcontinuity.net
- Example prompts:
  - "Save today's decisions and next steps for this project."
  - "What did I save about this project last week?"
  - "Create a checkpoint of my workspace."
- Icon: `claude/assets/icon-512.png` (512×512 PNG)
- Payments: "My connector does not accept payments". Purchases stay on AgentContinuity's own website and API, outside the connector.
- Support: https://agentcontinuity.net/contact/ (tom@phase3ai.com)
- Privacy policy: https://agentcontinuity.net/privacy/ (v1.2)
- Terms: https://agentcontinuity.net/terms/ (v1.3)
- Name and work email: the publisher's representative enters these.

## Remaining requirements and owners

1. Per-user OAuth with a Read Only scope, deployed and tested in production (engineering; private issue #29).
2. Company verification and evidence of authority to submit; acceptance of the Connector Platform Terms (publisher).
3. A dedicated review test account with synthetic data, kept available for the whole review (§5.5). It must be a separate account, never a production customer or administrator account. Credentials go only into the portal's secure credential field.
4. Tool documentation covering inputs, outputs, side effects, errors and rate limits (§5.4). It can be generated from the API's OpenAPI document for the tools listed above.
5. Security incident notice to Meta within 48 hours (§4.8). This must be added to the incident runbook before submission.
