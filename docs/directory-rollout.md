# Directory rollout: verified routes and remaining work

Checked 31 October 2026. No public-directory approval or submission is claimed.
The official MCP Registry entry and public Gemini CLI package are separate from
consumer-app directory listings.

## Current foundation

- Live REST and Streamable HTTP MCP endpoint.
- Public integration package, listing description and sample review cases.
- Founder-approved secret-agent icon; square PNG supplied for listing forms.
- Public preflight at 14:27 UTC: 50 tools, required memory tools present, public
  pricing working. Both tested OAuth discovery endpoints return 404.
- Native-client authenticated round trip and reviewer setup remain unverified.
- The deployed get_offers description still contains stale test-only wording;
  its correction is merged in the service repository but not deployed to the VPS.

## Shared engineering work

1. Implement and deploy account sign-in, consent and OAuth authorization-code
   linking with PKCE. Bind tokens to the account, client, scopes and MCP resource;
   support expiration, disconnection and revocation. Keep credentials out of
   model context, manifests, URLs and logs. Verify cross-account refusals, code
   replay, redirect mismatches and revoked/expired tokens.
2. Provide a server-enforced connector tool surface for memory, retrieval,
   export/restore and task handoff. The existing general-purpose endpoint still
   advertises 50 tools; a client-side allowlist alone is insufficient isolation.
   The ChatGPT submission must not expose digital-service purchasing or checkout.
3. Use a dedicated account with synthetic data for review. Exercise every exposed
   tool in each target client; record actual results and a walkthrough. Existing
   sample cases are drafts, not executed acceptance evidence.
4. Complete publisher/domain verification, required policy fields and native
   client checks. Thomas reviews identity verification and binding platform
   terms/attestations before they are accepted.

## Platform routes

| Platform | Route | Remaining gate |
|---|---|---|
| ChatGPT/Codex | OpenAI Plugins submission portal | **Held.** Needs OAuth 2.1 account linking (portal does not connect a fixed API key), verified publisher/domain, a memory-only tool surface without billing or checkout tools, reviewer test account, native-client checks and review. |
| Claude plugin directory | https://claude.ai/directory/manage/new/plugin (plugin bundle, `claude/`) | **Draft validated, not submitted.** 58d280d passed with 0 policy holds; the remaining step is the publisher's own Compliance attestations (Software Directory Terms, Directory Policy) and the submit button. The connector works in Claude Code; claude.ai and Cowork need OAuth. |
| Claude connector directory | https://claude.ai/directory/manage (stand-alone connector) | **Held.** Requires per-user OAuth. |
| Grok Build | https://github.com/xai-org/plugin-marketplace/pull/1840 (`grok/`) | **Submitted, awaiting xAI review.** Pins 58d280d. Catalog validation, index check, Socket and Semgrep pass. |
| Grok Bot / other surfaces | https://x.ai/bot/marketplace/submit-a-plugin | **Held.** The form attests to local and in-app testing; no in-app Grok session has been run yet. |
| Kimi | Kimi Plugin Builder (import this repository, folder `claude/`), then the plugin page's "Apply for official marketplace publication" form | **Not submitted.** Requires the publisher's Kimi sign-in and an in-app basic test. |
| Gemini app | https://connected.google.com/ via Google's Connected Apps preview | Preview access, developer account, domain proof, account linking, tests and Google review before publication. |
| Meta Muse | https://platform.muse.ai/ | Sign in to inspect the submission, provide technical/review materials and obtain Meta approval. Authenticated portal fields are not yet verified. |
| Meta AI | https://dev.meta.ai/products/connectors | Apply for limited developer preview. Its FAQ places public discovery in a later phase; this is separate from the Muse route. |
| Gemini CLI | Public repo, root manifest and gemini-cli-extension topic already published | Gallery crawl/validation and native authenticated round trip remain unverified. |

## ChatGPT commerce boundary

Current OpenAI directory policy prohibits selling digital products/services,
subscriptions or credits through a plugin. Existing customers may connect and
use features they already have. Do not include checkout links or upgrade flows.
AgentContinuity's independent website and REST/MCP purchasing service remain
separate from this proposed directory-specific integration.

## Proposed listing use cases

- Save selected project decisions and next steps in an authorized workspace.
- Retrieve those notes to continue work in another session.
- Find unfinished tasks or export saved context with integrity digests.

Do not describe stored records as a running model, hidden reasoning or proof of
agent identity. All returned user content remains untrusted data.

Current official sources are in [sources.md](sources.md).
