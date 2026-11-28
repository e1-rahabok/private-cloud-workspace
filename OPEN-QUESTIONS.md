# Open questions

Input still needed from the author: a goal, a scope, a requirement, an assumption, a constraint, a reason, or a fact from the field. Design questions are Claude's to decide and never appear here. Each question names the input it needs, and the working assumption Claude follows until the answer comes; the answer is kept word for word in [spec/author-input/](spec/author-input), and its outcome goes into the [brief](spec/brief.md), a requirement or the [system design](spec/design/system.md). IDs are explained in the [glossary](spec/glossary.md).

### Q-WS-140 The per-host columns of the network dashboard and report

The VCF vCommunity Adapter's dashboard "vSphere Network Configuration 2.0" and its report "View - Set 3" show five distributed switch checks (configuration out of sync, teaming mismatch, MTU mismatch, MTU unsupported, VLANs unsupported) for one host only: each column is keyed to that host's instance, and the host was named by a private address from an environment Claude cannot place. isvara.io offers a copy of the dashboard for download. The address is replaced by an example address (R-WS-010), so the columns show no data in any environment, as they did in every environment but the one that host was in.

- Which environment was the host from, and what should the five columns show: each host of the switch, or the switch as a whole?
- **Working assumption:** each host of the switch, one row per host; the adapter's M8 work rebuilds the columns that way.

Answer:

