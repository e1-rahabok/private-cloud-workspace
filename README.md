# Private Cloud Workspace

Overview of the 4-repo app.

The app is 4 GitHub repos that form one product.

## The four repos

| Repo | Role | Notes |
|---|---|---|
| `private-cloud-management` | Web app | Runs on-premise, not on the Internet. Customers deploy it privately. |
| `agent-e2` | The "brain" | Used by the LLM. |
| `VCF-vCommunity-Adapter` | Metrics | A VCF Operations adapter. |
| `isvara` (https://isvara.io) | Public site | Helps readers learn the domain. Not part of the on-premise product. |

## How the pieces fit

- The 4 repos form one product.
- A change can span more than one repo.
- `isvara` is separate. It is a public site, not part of the on-premise deployment.

## Deployment

- Customers deploy the product privately, on-premise.
- The product is not hosted on the Internet.
- TODO: Confirm how `agent-e2` and `VCF-vCommunity-Adapter` are deployed with `private-cloud-management`.
- TODO: Confirm the deployment steps and requirements.

## Build and test

- See the "Build and test" section in each repo.
- TODO: Fill in per repo.

## Working rules

- See [CLAUDE.md](CLAUDE.md).
