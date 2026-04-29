# School IT brief

A one-page summary you can email to your school's IT department to get
barebear approved for classroom use. Below is a plain-text version
suitable for pasting into an email.

---

## What it is

barebear is an open-source Python framework for teaching agentic AI to
sixth-form / A-level Computer Science students. It is freely available
under the MIT licence, maintained on GitHub, and distributed via PyPI
(the standard Python package repository). It is not a service — it is
a small Python library (~1,500 lines of source code) that runs on a
student's laptop or, more commonly, in Google Colab in a browser.

- **Source / homepage:** <https://github.com/richey-malhotra/barebear>
- **Package on PyPI:** <https://pypi.org/project/barebear/>
- **Licence:** MIT (permissive open-source, commercial-use friendly)

## How students will use it

For most lessons, students click a "Open in Colab" link, sign in to
Google, and run code in their browser. **No software needs to be
installed on school machines.**

For lessons where students want to use barebear locally, they would
install Python (3.9+) and run `pip install barebear` from a normal
user account — no admin / root access required. This is the same model
as installing any standard scientific Python library (numpy, pandas,
matplotlib).

## Network endpoints used

When students run a lesson, the only outbound traffic is to one of two
endpoints:

| Endpoint | Purpose | Required? |
|---|---|---|
| `openrouter.ai` | Hosted free-tier AI model service | Required for default lessons |
| `colab.research.google.com` | Browser-based Python notebook host | Required for the no-install path |
| `pypi.org` | Standard Python package repository | Required only if students install locally |
| `github.com` | Raw lesson notebook contents | Required only if students install locally |

If your school already permits Google Workspace / Google Colab and
PyPI for STEM teaching, no additional firewall changes are needed.

If students wish to run **without internet**, they can install
[Ollama](https://ollama.com) — a free, open-source local AI runtime —
on their machine and run lessons entirely offline. This is the
recommended path for schools where AI-domain whitelisting is
restricted.

## Data sent to OpenRouter

When students run a lesson cell, the request to `openrouter.ai`
contains:

- The student's prompt text (e.g. "Greet a user named Alice").
- The system prompt the lesson defines (publicly visible in the
  lesson source).
- The OpenRouter API key the student or teacher generated.

What is **not** sent: any local files, any browser history, any
school-system data, any other student information.

OpenRouter operates under standard internet-service privacy practices.
Their privacy policy is at <https://openrouter.ai/privacy>.

## Data we (barebear) collect

**None.** barebear is a library, not a service. It runs on the
student's machine or in their Colab session. There is no telemetry,
no analytics, no phone-home. The only network traffic is to
OpenRouter (or Ollama, locally) for the AI model itself.

## Suitability for under-18 students

The lessons themselves are written for ages roughly 16+ and contain no
inappropriate content. Students will, of course, send their own
prompts to AI models, and AI models can produce unexpected outputs —
this is true of any AI service, including school-issued tools like
Microsoft Copilot for Education.

OpenRouter free-tier models are general-purpose. Schools concerned
about model output may prefer the **Ollama (offline)** path, where the
specific model (e.g. `qwen2.5:3b`) is small, vendor-controlled, and
known. The lessons run identically against either backend.

## Cost to the school

**Zero.** Barebear is open-source. OpenRouter has a free tier
sufficient for classroom use. Google Colab has a free tier sufficient
for lesson notebooks. Ollama is free.

## Summary for whitelisting

If your school's IT policy requires a single line of justification for
allowing classroom access to:

- `openrouter.ai`  — used for free AI-model API calls in CS lessons
- `colab.research.google.com` — used for in-browser Python notebooks

— that is the entire request. There is no installer, no agent on the
network, no inbound traffic, no PII.

## Verifying

If your IT department wishes to verify any claim above:

1. The full source is at <https://github.com/richey-malhotra/barebear>
   — they can read every line.
2. Network calls can be inspected by running a lesson and using the
   browser's developer tools (Network tab).
3. The MIT licence is at <https://github.com/richey-malhotra/barebear/blob/main/LICENSE>.

---

## Email template

> **Subject:** Approval request — barebear (open-source Python library
> for sixth-form CS lessons)
>
> Hi [IT contact],
>
> I'd like to use barebear in my A-level Computer Science classes
> next term. It's a small open-source Python library (~1,500 lines,
> MIT licence) that lets students run lessons on AI agents in a
> browser via Google Colab — no installation on school machines
> required.
>
> The only network endpoint students will use is `openrouter.ai`
> (free-tier AI model API) alongside the existing `colab.research.google.com`
> we already use for STEM. No data is sent beyond the prompts students
> type. There's an offline-only option (Ollama) available for any
> students whose home setup blocks AI domains.
>
> The full source, licence, and a more detailed IT brief are at:
>
> <https://github.com/richey-malhotra/barebear/blob/main/docs/teaching/it-brief.md>
>
> Could you confirm whether `openrouter.ai` is reachable from the
> classroom network, or whether it needs to be added to the
> whitelist? Happy to come and walk you through it whenever suits.
>
> Thanks,
> [your name]

---

If your IT department needs additional information not covered here,
please [open a comment on the pinned classroom thread](https://github.com/richey-malhotra/barebear/issues/1)
— the question and the answer will help other teachers in the same
situation.
