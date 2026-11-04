# AgentContinuity — OpenAI plugin submission gate (2026-11-03)

**Status: PREPARATION ONLY. Not uploaded, submitted, approved, or listed. OAuth remains off in production.**

Business publisher: **SapienCX LLC** (not yet verified in OpenAI Platform, per the publisher's 2026-11-03 browser inspection). A Personal Platform organization and an AgentContinuity project already exist; a ChatGPT Enterprise subscription or separately named SapienCX organization is not required solely for plugin submission.

## Why this package is different

The prior package pointed to the legacy `https://api.agentcontinuity.net/mcp` endpoint, which advertises general commerce/board tools and uses bearer API keys. It is unsuitable for an OpenAI public plugin. The submission candidate instead declares:

- **Single MCP server**: `https://api.agentcontinuity.net/mcp/openai`
- **Authentication**: OAuth with Client Identifier Metadata Document (CIMD) preference; discovery, PKCE, issuer and client metadata validation occur server-side
- **Initial scope**: `memory:read`; any additional authorized tool scopes must be requested and approved separately
- **17 server-allowlisted tools**: private memory, checkpoint/export, task handoff, private messaging, and sanitized usage. No billing, subscriptions, checkout, credits, public bulletin board, admin, data deletion or restore
- **No automatic conversation extraction**: save only notes the user deliberately selects

This candidate cannot work in ChatGPT until OAuth is safely enabled on the existing service and a real login has succeeded.

## Non-negotiable monetization policy

OpenAI's public plugin rules currently prohibit selling **digital services/products, subscriptions, digital content, tokens or credits** through plugins, including indirect freemium upsells. Plugins cannot promote upgrades, list subscriptions or link to checkout. Existing paying customers may log in to use their already-owned entitlements. See https://developers.openai.com/plugins/plugin-guidelines .

AgentContinuity's external website and independent commerce remain separate. Do not add paywalls, payment tools, upgrade prompts, coupon links, buying CTAs, or transaction redirects to the OpenAI plugin.

A plugin can improve discoverability but directory publication is **not** a guarantee of referral traffic, paying customers, or revenue.

## Publisher-owned steps (identity and approvals)

1. Sign in to the existing OpenAI **Platform Personal organization**, choose project **AgentContinuity**, and open the organization settings' developer/business identity verification.
2. Choose **business verification** for **SapienCX LLC** if the company name is to appear as publisher. Complete requested identity/legal evidence in the official OpenAI portal; never supply IDs or incorporation documents through a model chat.
3. Verify the selected identity appears in the Plugins portal. Platform organization name need not match the directory publisher's business name, but the business publisher must be independently verified.
4. The Founder must personally accept legal/policy attestations and the final submission. Do not automatically publish, contact reviewers, or accept contracts on the Founder's behalf.

## Technical gates before submission

- [ ] Existing private `OZYMANDIAS2020/agentcontinuity` release is known good; OAuth remains `AC_OAUTH_ENABLED=false` / `AC_OAUTH_REVIEW_ACCESS=false` until the separate security activation approval.
- [ ] Read-only inspection of the real portal's OAuth **client metadata document URL** and **redirect/callback URI**. Do not invent these. Configure exact CIMD client and callback allowlists in the existing OAuth server.
- [ ] Verify live issuer metadata, protected resource metadata, RFC 9207 `iss`, PKCE S256, code expiry/replay refusal, account linking and token refresh/revocation; use a synthetic dedicated reviewer account. Confirm OpenAI workspace-domain-authorization requirements (`openid`, `email`, UserInfo endpoint) if applicable; implement if mandatory before approval.
- [ ] Confirm tool discovery presents exactly the **17** restricted tools and no commerce or administrative function even when an adversarial client explicitly requests an excluded name.
- [ ] Serve the **actual exact domain verification token** provided by the portal on the required well-known path; do not fabricate or expose unknown challenge values.
- [ ] Run genuine ChatGPT/Codex OAuth connect, consent, data-write and retrieval flows against synthetic records. Test the new feature without opening any purchases.
- [ ] Create a reviewer login with synthetic workspace content that does not require owner intervention, MFA, SMS/email one-time codes, or customer secrets.
- [ ] Verify public HTTPS website, privacy, terms and support URLs, brand logo, tool schemas/annotations, and the current portal's submission requirements.
- [ ] Run required automated ZIP and connected MCP scans; correct findings and re-scan.
- [ ] Record the video walkthrough, five positive and three negative *executed* cases, and release notes. Only then ask the Founder for submission authorization.

## Proposed reviewer cases — not yet run

Five positive cases, to execute once OAuth is enabled in controlled review:

1. List synthetic workspaces via `list_workspaces`, return the correct workspace and no other tenant data.
2. Save a deliberately supplied synthetic decision with `save_memory` and read it back using `retrieve_memory`.
3. Find a relevant synthetic note using `search_memory` without revealing unrelated notes.
4. List a known synthetic task and create/claim/complete a test handoff under the authorized scopes.
5. Read/export a synthetic checkpoint or context package, distinguishing integrity checks from truth.

Three negative cases:

1. Ask the plugin to buy credit, subscribe, start checkout or upgrade. **Expected:** no commerce tool, checkout, upgrade promotion or purchase CTA.
2. Ask for another customer's memories or unrelated account keys. **Expected:** no cross-tenant read or sensitive credential output.
3. Ask for public board publishing, privileged administration or an automated unsolicited message. **Expected:** no tool exposed for that action; refusal or clear safe limitation.

## Follow-up outcomes

Track (with disclosed, privacy-minimal consent) the count of genuine plugin activations and successful memory operations on the server. Keep synthetic reviewer activity distinct. Any paid conversion attribution belongs to independently permitted commerce channels and settled Stripe records, not guessed ChatGPT clickthrough. No unsolicited outreach.

Official documentation:
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/plugins/plugin-guidelines
