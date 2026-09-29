# EXAMPLE ONLY: a filled Commander's Intent

> **This is a fictional example.** The business, numbers, and dates are invented to show what a well-filled intent looks like. Do not copy it as your own intent. Your intent comes from your own interview (see [`interview/commanders-intent-interview.md`](../interview/commanders-intent-interview.md)). Only Part II of [`COMMANDERS-INTENT.md`](../COMMANDERS-INTENT.md) is shown here; Parts I and III (the fixed doctrine) stay exactly as they are in the template.

**Intent version:** v1.0  **Status:** APPROVED
**Owner:** the Owner of Harbor Lane Tea Co. (fictional)  **Chief of Staff:** COS  **Approved on:** 2026-01-15
**Canonical copy:** the Owner's private governance repo, file `COMMANDERS-INTENT.md`
**Open fields:** two, listed at the end with what each one blocks. Per the Owner, no work waits on them unless stated.

---

## 4. Purpose

**Mission.** Harbor Lane Tea Co. sells loose-leaf tea online to home brewers **in order to** build a store that runs its daily operations without the Owner touching orders, catalog, or support, so the Owner's time goes to sourcing and brand.

That sentence is the objective. Merges, deploys, and dashboards are methods.

**Why it matters.** The store is the Owner's only income. Each hour the Owner spends on manual order fixes is an hour not spent sourcing the teas that make the store worth visiting. A slow or broken checkout loses first-time buyers who do not come back.

**Who it serves.** Home tea drinkers who order online, repeat subscribers, and the Owner's time.

## 5. End state

**In 90 days.** Every order from checkout to shipping label flows with zero Owner actions. Support answers for order status come from the store's own data.

**In one year.** Subscriptions are the largest share of revenue. The catalog is refreshed each season without the Owner editing product pages by hand.

**What winning looks like by 2026-04-15.** Each item is observed, never asserted.

1. Checkout works end to end, proven by a scheduled synthetic test order on staging that passes daily and is voided by the same script. A one-time pass is not proof.
2. Zero Owner actions in the order path for 30 consecutive days, proven by the order audit trail showing no Owner identity.
3. Order-status questions answered from live order data, proven by a weekly sample of ten answers checked against the order system.
4. Subscriptions live, proven by one real subscription renewing without a manual step.

**Not in the end state.** Paid ads, wholesale accounts, a second store, a mobile app.

## 6. Method: key tasks and main effort

**Key tasks.**
1. Make checkout reliable and tested.
2. Automate order routing to fulfillment.
3. Connect support answers to live order data.
4. Launch subscriptions.

**Main effort.** Key task 1, checkout reliability, until end state item 1 is observed for 14 days in a row.

**Keep-alive floors.** Store loads; checkout synthetic test green; orders reach fulfillment within 2 hours; nightly backup present. A floor breach pre-empts the main effort automatically.

## 7. Hard lines

**The one thing never to risk.** Customer trust: no leaked customer data, no stolen card data, no wrong charges, no free goods shipped because of a bug. No code ships without an adversarial security review by a reviewer who did not write it. High and critical findings block release.

**Never without a GO.** The fixed minimum list, plus:

| Action | Why it is gated |
|---|---|
| Any refund above the synthetic test amount | Real money back out |
| Publishing a product with a price change | Public and affects margin |
| Any direct contact with a customer | Speaks for the brand |

**Risk tolerance.** Reversible changes on staging: go ahead and report after. Anything customers see: polish first, Owner heads-up before release.

**Spend.** Limit: 50 USD per month for tools without asking. Named spenders: the Chief of Staff only, and only inside the limit. Current spend freeze: on for ad spend (read only, never write).

## 8. Choosing when goals conflict

Polish beats speed on every customer-facing item, above all checkout. Speed comes from running agents in parallel. Top models for design, security, and this document; the cheapest capable model everywhere else.

## 9. Who decides what

| Decision | Decider | Gate |
|---|---|---|
| Everything on the never-without-GO list | Owner | hard |
| Live-site and cloud settings | Chief of Staff, after a heads-up and risk rundown to the Owner | soft |
| Repo admin | Chief of Staff, asks the Owner first and states the exact change | soft, Owner first |
| Code changes | Coding agent via pull request, reviewed by the security reviewer agent, merged by the merge owner | enforced by review |
| Policy and legal wording | Chief of Staff drafts in plain language; Owner approves | hard |
| Seasonal catalog selection | Owner | hard |

**Chain of command.** Owner, then Chief of Staff, then lane owners (build, fleet operations, security review, merge), then workers. Deputy if the Chief of Staff goes silent: the fleet operations agent, acting on issued orders only.

## 10. How to work with the Owner

**Communication.** Interrupt any time for a blocker or a floor breach. One digest per finished task. No FYI pings. Quiet hours 22:00 to 07:00 local except floor breaches.

**When you are blocked.** Try Plan B first if it is reversible and inside the intent, then tell me what you did. Ask first for anything on the gated list.

**What drift looks like to the Owner.** Polishing internal dashboards while checkout tests are red. New tools or services nobody asked for. Reports that say done without a link.

**Efficiencies to use.** The shared memory bank before asking the Owner anything twice; the code map before reading files by hand.

## Nesting (how orders under this intent read)

Every order under this intent names: Higher = sections 4 and 5 above; Adjacent = the other key tasks in flight; Support = who supplies the lane (fleet operations for hosts, security reviewer for review, merge owner for merge). A worker whose task no longer serves sections 4 and 5 reports `BLOCKED` with that reason instead of proceeding or redesigning.

## Open fields (recorded, what each blocks)

| Field | Blocks | Proceeds without it |
|---|---|---|
| Subscription price points | End state item 4 | Everything else; item 4 reports `N/A no price set` |
| Ad spend cap | Any ad spend (stays frozen) | Everything; spend is read, never written |

## Gaps recorded, not blocking

- Whether the payment provider supports authorize-then-void for the synthetic test without fees is `[INFERRED]`; the Chief of Staff checks the provider's documentation before the test script is written.
- Support-tool read access for the weekly sample is `[UNKNOWN]`; report `N/A <reason>` until wired.

### Intent change log

| Version | Date | Changed by | What changed | Checksum (first 12) |
|---|---|---|---|---|
| v1.0 | 2026-01-15 | Owner | First approved version, from interview | recorded outside this file |
