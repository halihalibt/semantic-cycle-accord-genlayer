# SCA-3 V1 State Machine

Time is the GenVM transaction clock. At `now >= expires_at` an OPEN or RESERVED
Intent is effectively EXPIRED. At `now >= confirmation_deadline` a PENDING
Cycle is effectively EXPIRED. Reads show both effective and stored status; they
do not mutate storage. CONSUMED, CANCELLED and terminal Cycles keep their status
after their old timestamps pass.

| Entity / from | Trigger | To / effect |
| --- | --- | --- |
| New Intent | Valid create by actual caller | OPEN, version 1 |
| OPEN Intent | Valid owner update with expected version | OPEN, version +1 |
| OPEN Intent | Valid owner cancellation | CANCELLED |
| OPEN Intent | Future accepted assessment invokes deterministic seam | RESERVED, linked to new PENDING Cycle |
| RESERVED Intent | Third independent valid confirmation | CONSUMED, linked to ACTIVE Cycle |
| RESERVED Intent | Eligible cycle decline/cancellation | OPEN if valid; cancelled target becomes CANCELLED |
| RESERVED Intent | Expiration cleanup | OPEN if still valid; otherwise EXPIRED |
| PENDING Cycle | Owner's first/second valid confirmation | PENDING, one flag added |
| PENDING Cycle | Third valid owner confirmation | ACTIVE and all three Intents consumed |
| PENDING Cycle | Eligible owner decline | ABORTED; release own reservations; record declined identity |
| PENDING Cycle | Valid cancellation of its reserved Intent | ABORTED; release own reservations; cancel target |
| PENDING Cycle | Cleanup at or after deadline | EXPIRED; release own reservations |
| ACTIVE / ABORTED Cycle | Any confirm, decline or expiration | Reject; terminal |
| EXPIRED Cycle | Repeated expiration cleanup | False, no changes |

RESERVED and CONSUMED content cannot be edited. A reserved cancellation first
checks the actual owner, current version, deadline and authoritative snapshot.
An overdue reserved cancellation rejects until permissionless `expire_cycle`
cleans up the Cycle; then a still-valid OPEN Intent may be cancelled normally.
Expired Intents cannot be confirmed, matched, or edited.

Activation is a commitment state, not a delivery or settlement state. Cleanup
never reopens cancelled, expired, consumed, or another Cycle's reservations.
History and frozen terms remain readable after terminal transitions.
