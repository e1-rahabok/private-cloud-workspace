# Open questions

Questions only the author can answer: names, field knowledge, lab facts, and the licence. Everything else from the interview is decided; the records are [round 1](spec/interview-round-1.md) and [round 2](spec/interview-round-2.md). Write an answer under each question, or `Agree` to take the recommendation. IDs are explained in the [glossary](spec/glossary.md).

## Q-60 The product's name

You called PCM "a website called Private Cloud Manager" (2026-11-26) and changed its heading in the intent to "private-cloud-manager"; the repository is [private-cloud-management](https://github.com/e1-rahabok/private-cloud-management), and PCM's D-001 says "Private Cloud Management".

- **Recommendation:** "Private Cloud Manager" for the product, since it names the tool and the books keep "Private Cloud Management" as the discipline. PCM stays the short name. The repository is renamed to match, the way PCM-Adapter was.

**Answer:**

## Q-88 Guest OS run queue: per vCPU, or total

The adapter's part is "Guest CPU Run Queue per vCPU"; Agent E2's catalog calls it "Peak vCPU run queue length", with the same limits (0, 2, 4, 8, 16). One of the two is wrong.

- **Needs your field knowledge:** were the limits set per vCPU or for the whole Guest OS? If per vCPU, the catalog row is renamed; if total, the adapter changes.

**Answer:**

## Q-120 Where the nested ESXi hosts run

The lab build creates two small nested ESXi hosts with memory tiering ([lab-build requirements](spec/requirements/lab-build.md)).

- **Needs you:** the physical cluster, datastore and network to use, and how much CPU, memory and NVMe space you can spare.

**Answer:**

## Q-122 Licences for the nested hosts

- **Needs you:** do the lab licences cover two more ESXi hosts?

**Answer:**

## Q-130 Events for birds-of-a-feather sessions

Contributions on isvara.io can include a request for a session on a topic ([isvara.io plan](spec/design/isvara-revamp.md), section Contributions).

- **Needs you:** which events to list, for example VMware Explore, VMUG meetings, or online.

**Answer:**

## Q-132 A GitHub organization for the product

Customers copy all the product's repositories together (W-025). An organization gives the product one name on GitHub and shared defaults for every repository. The repositories are under your personal account today.

- **Recommendation:** move the product repositories and this workspace into an organization named after the product, after Q-60 settles the name. isvara stays where it is.

**Answer:**

## Q-133 The licence

Customers will copy the knowledge and the code, and the vCommunity will contribute (W-024). Both need a licence that says what is allowed. Some repositories have their own today, and they differ.

- **Recommendation:** one licence for the code (an open-source licence such as Apache 2.0, which allows private copies and changes) and one for the knowledge (a Creative Commons licence that requires credit). This is your decision, and worth a lawyer's reading before contributions grow.

**Answer:**
