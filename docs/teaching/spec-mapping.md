# Exam-spec mapping

This document maps the 12 barebear lessons to commonly-taught Computer
Science specifications: UK **AQA A-level**, UK **OCR A-level**, UK **OCR
GCSE** (J277), US **AP Computer Science Principles**, US **AP Computer
Science A**, and **IB Computer Science** (HL/SL).

It exists so a head of department can answer the *"how does this fit our
scheme of work?"* question in under a minute.

## How to use this document

Each lesson is described first in **concept terms** — what it actually
teaches, independent of any spec. Then for each major spec, the lesson is
labelled:

- **Direct** — teaches a concept the spec explicitly examines
- **Adjacent** — teaches a concept the spec touches but doesn't
  centrally examine
- **Enrichment** — broadens understanding without a one-to-one spec point

Specifications change. Section numbers below were checked at the time of
writing but you should always cross-reference your current spec document.
Cells marked `[verify]` are areas where the mapping is plausible but I
have not personally confirmed the current section number — please check
and, if you teach this, [open a comment on the pinned thread](https://github.com/richey-malhotra/barebear/issues/1)
so the mapping improves.

---

## Concept summary per lesson

| # | Concept | What students actually learn |
|---|---|---|
| 1 | What an LLM is | Direct API call to an LLM. Tokens, system/user/assistant roles, request-response cycle. |
| 2 | The agent loop | Wrapping the LLM call in a loop that can act. Perceive → think → act → observe. |
| 3 | Tool design | Function calling. Schemas as part of the prompt. Naming and description matter. |
| 4 | State and memory | Short-term (message list) vs long-term (`State` dict). Persistence between runs. |
| 5 | Budgets | Resource limits on autonomous systems. Step / token / cost caps as safety. |
| 6 | Policy and guardrails | Pre-execution checks. Risk classification. Side-effect categorisation. |
| 7 | Checkpoints | Human-in-the-loop. Pausing autonomous execution for approval. |
| 8 | Planning | Plan-then-execute vs act-and-react. When each is appropriate. |
| 9 | Reflection | Self-critique. Iterative refinement. The asymmetry between generating and evaluating. |
| 10 | Multi-agent | Composition: a system from cooperating components. Separation of concerns. |
| 11 | Evaluation | Testing non-deterministic systems. Behavioural assertions over `Report` traces. |
| 12 | Honest uncertainty | Distinguishing what is known from what is assumed. Surfacing this to downstream code. |

---

## UK A-level — AQA (7517)

The current AQA A-level Computer Science specification examines, among
other things, **moral, social, legal and ethical issues** (section 4.9 in
the published spec at time of writing), **theory of computation**,
**fundamentals of programming and OOP**, and **algorithms**. The mapping
below focuses on areas where barebear lessons can be cited as direct or
adjacent material.

| Lesson | Mapping | Spec area |
|---|---|---|
| 1 | Direct | Programming fundamentals; communication with external services |
| 2 | Direct | Iteration and selection; subroutines (`Bear.run`, tools as functions) |
| 3 | Direct | Subroutine design; parameter passing; data types and structures |
| 4 | Direct | Variables, persistence, file/dict-based storage |
| 5 | Adjacent | Computational efficiency; trade-offs in resource use |
| 6 | **Direct** | **Section 4.9 — Moral, social, legal, cultural and ethical issues. Specifically: software safety, privacy, automation responsibility.** `[verify current section number]` |
| 7 | Direct | Human-computer interaction; system design with mandatory human steps |
| 8 | Adjacent | Algorithm design; pseudocode and step decomposition |
| 9 | Enrichment | Software testing concepts; iterative development |
| 10 | Direct | Object-oriented design; composition; modular system architecture |
| 11 | **Direct** | **Software testing; verification and validation; documentation** |
| 12 | **Direct** | **Section 4.9 — Risks of overconfident automation; AI ethics** |

**Strongest fit:** sections 4.9 (ethics), programming/OOP fundamentals,
and software testing.

---

## UK A-level — OCR (H446)

The OCR A-level specification examines **algorithms** (component 02),
**software development** (1.2), **legal, moral, cultural and ethical
issues** (1.5), and **programming techniques** (2.2). Particularly well-
matched to barebear's framework-as-textbook approach.

| Lesson | Mapping | Spec area |
|---|---|---|
| 1 | Direct | 2.2 Programming techniques — function definition, parameter passing |
| 2 | Direct | 2.2 — control flow, iteration, function calls; 2.3 — design |
| 3 | Direct | 2.2 — modular code; subroutines and parameters |
| 4 | Direct | 2.2 — data structures; persistence |
| 5 | Direct | 2.3 Software development — testing for edge cases; defensive programming |
| 6 | **Direct** | **1.5 Legal, moral, cultural and ethical issues — software ethics, automation safety** |
| 7 | Direct | 2.3 Software development methodologies — human checkpoints in workflow |
| 8 | Direct | 2.1 Algorithms — algorithm design before implementation |
| 9 | Adjacent | 2.3 — iterative development, debugging |
| 10 | Direct | 2.2 — OOP concepts: composition, encapsulation; modular design |
| 11 | **Direct** | **2.3 — testing strategies, validation, behavioural specification** |
| 12 | **Direct** | **1.5 — risks of AI; epistemic responsibility in autonomous systems** |

**Strongest fit:** OCR's 1.5 ethics topic and the 2.x programming /
software development topics. The full lesson sequence forms a coherent
software-engineering case study.

---

## UK GCSE — OCR Computer Science (J277)

For GCSE classes, barebear is best used as **enrichment** — students
generally need stronger Python fundamentals than the GCSE assumes. That
said, lessons 1–4 work as a Year-11 enrichment unit if students have
covered iteration, selection, and functions.

| Lesson | Use as | Spec area |
|---|---|---|
| 1–2 | GCSE-appropriate | 2.1 Algorithms; 2.2 Programming fundamentals |
| 3–4 | GCSE-appropriate | 2.2 Programming fundamentals |
| 5–6 | Enrichment | 1.5 Legal, ethical, environmental impact |
| 7+ | Post-GCSE / Year-12 bridge | — |

---

## US — AP Computer Science Principles

AP CSP examines five Big Ideas. barebear maps strongly onto **Big Idea 3
(Algorithms and Programming)** and **Big Idea 5 (Impact of Computing)**.

| Lesson | Big Idea | Specific topics |
|---|---|---|
| 1 | BI 3 | Variables, expressions; algorithms as sequences of steps |
| 2 | BI 3 | Iteration; abstraction; procedures with parameters |
| 3 | BI 3 | Procedures and parameters; libraries |
| 4 | BI 3 | Lists / data structures; managing complexity |
| 5 | **BI 5** | **Computing systems and networks; impacts on resources, scale** |
| 6 | **BI 5** | **Beneficial and harmful effects; safe computing** |
| 7 | BI 3 + BI 5 | Procedural abstraction; human oversight of automation |
| 8 | BI 3 | Algorithm development; problem decomposition |
| 9 | BI 3 | Iterative refinement |
| 10 | BI 3 | Procedural abstraction; modular design |
| 11 | BI 3 | Testing and debugging |
| 12 | **BI 5** | **Computing bias; trustworthiness of automated systems** |

**Performance Task fit:** lessons 8, 10, 11, 12 give students concrete
experience producing and evaluating an autonomous system, which transfers
directly to the AP CSP Create Performance Task.

---

## US — AP Computer Science A

AP CS A is more rigorous on Java OOP. barebear is in Python, so it can't
substitute for AP CS A teaching, but it can be used as an **end-of-year
enrichment block** (after the exam, May–June) that demonstrates practical
applications of OOP and software engineering students have already learnt.

| Lesson | Use as | Topic |
|---|---|---|
| 1–4 | Enrichment | Practical OOP: classes (Bear, Tool, Policy), methods, composition |
| 5–7 | Enrichment | Exception handling parallels; defensive programming |
| 8–11 | Enrichment | Software design; algorithm development; testing |
| 12 | Enrichment | Reflective software engineering practice |

---

## IB Computer Science (HL / SL)

The IB CS curriculum spans **Topic 1 (System fundamentals)**, **Topic 4
(Computational thinking)**, **Topic 5 (Abstract data structures, HL)**,
the **Internal Assessment** (programmed solution), and the **Case Study**
(annually rotating, recently AI-themed in 2026 cycles).

| Lesson | Mapping | IB area |
|---|---|---|
| 1 | Direct | Topic 4 — programming fundamentals; communication |
| 2 | Direct | Topic 4 — control structures; abstraction |
| 3 | Direct | Topic 4 — methods/functions; parameter design |
| 4 | Direct | Topic 4 — state, persistence; HL: data structure design |
| 5 | Adjacent | Topic 1 — software–hardware interaction; resource constraints |
| 6 | **Direct** | **Topic 1 — social and ethical issues; system design** |
| 7 | Direct | Topic 1 — system design with human factors |
| 8 | Direct | Topic 4 — algorithm design; thinking before coding |
| 9 | Adjacent | Internal Assessment — iterative development with testing |
| 10 | Direct | Topic 5 (HL) — abstract data structures and composition |
| 11 | **Direct** | **Internal Assessment — testing and evaluation** |
| 12 | **Direct** | **Case Study (2026 onward) — AI ethics, transparency, accountability** |

**Strongest fit:** the Case Study (especially when it's AI-themed) and the
Internal Assessment, where students must produce, document, and evaluate
a working program.

---

## A note on currency

Specifications are revised. AQA, OCR, the College Board, and the IB all
publish updated documents periodically. Section numbers in this file were
correct at time of writing (early 2026). Before relying on a specific
mapping for SLT or OFSTED-facing documents, check it against the current
published spec for your exam series and, ideally, [share a correction in
the pinned classroom thread](https://github.com/richey-malhotra/barebear/issues/1)
so other teachers benefit.

If you teach a spec not listed here (Edexcel A-level, Scottish Highers,
NCEA, Australian VCE / HSC, Indian CBSE, others) and you'd like a
mapping, please open a comment on the same thread — local additions are
welcomed.
