# Teacher quickstart

Start here if you're a CS teacher considering using barebear in your
classroom and you haven't necessarily installed a Python framework
before, or you don't think of yourself as a "technical" teacher.

You do not need to be a software engineer to teach this course. You need
to be a CS teacher willing to learn alongside your students for the first
two lessons. That is enough.

## What you actually need to do (the short version)

1. Click the **Try Lesson 1 in Colab** badge on the [main README](../../README.md).
2. Sign in to Google so the notebook can run.
3. Copy a free OpenRouter key (steps below) and paste it when the notebook asks.
4. Click **Run all** in the menu bar.

If you can do that, you can teach Lesson 1 from a projector tomorrow.
Everything else in this document is to help with the other 11 lessons,
the questions you'll get from students, and the conversations you'll
have with your IT department.

## You do not need to

- Install Python on your laptop.
- Use the command line / terminal.
- Use git.
- Read the framework source.
- Understand exactly how an LLM works internally.

You *can* do any of these and it'll deepen your teaching. But you can
teach the whole 12-week course with **just a browser, a Google account,
and a free OpenRouter key**. Every lesson runs in Google Colab — a free
in-browser code editor — with no install required.

## Step-by-step setup (about 10 minutes, one-time)

### Step 1 — Get a Google account ready

Most teachers already have one (school-issued Google Workspace counts).
If your school uses Microsoft 365, you'll need a personal Google account
or Gmail to use Colab. School policies vary — check with your IT
department before sharing screen shots that include your account name.

### Step 2 — Get a free OpenRouter API key (no card needed)

OpenRouter is the service that lets students "talk to" a real AI model.
The free tier is genuinely free — no payment method required.

1. Open [openrouter.ai](https://openrouter.ai) in a new tab.
2. Click **Sign in**, choose Google or GitHub. Use a personal account if
   your school account blocks it.
3. Once signed in, click your avatar in the top right, then **Keys**.
4. Click **Create Key**. Give it a name (e.g. `school-classroom`).
   Copy the key it shows you — it starts with `sk-or-`.
5. Save the key somewhere private. **Treat it like a password.**

You will paste this key into the Colab notebook when prompted. The
notebook stores it for that session only — it's not saved to your Google
account or visible to students unless they look at your screen.

### Step 3 — Open Lesson 1 in Colab

1. Go to the [main README](../../README.md).
2. Click the **Open in Colab** badge near the top.
3. Colab opens in a new tab. You'll see a notebook with text and code
   cells.
4. Click **Runtime → Run all** in the menu.
5. The notebook will pause and ask you to paste your OpenRouter key.
   Paste it. Press Enter.
6. Watch the cells run. The final cell prints a real answer from a real
   AI model.

You've just done what your students will do in Lesson 1. The whole
course works the same way.

## A pre-lesson checklist (do this once before each class)

Run through this 5–10 minutes before the lesson:

- [ ] Open the lesson's Colab notebook in advance, in your browser.
- [ ] Paste your key. Run the first cell. Confirm a model response comes
      back. (If it doesn't, the free model may have rotated off — see the
      [troubleshooting](#troubleshooting) section.)
- [ ] Have the lesson's [`lesson.md`](../../lessons/README.md) open in a
      second tab — it has the discussion questions and exercise prompt.
- [ ] If you're projecting, sign out of any other tabs you don't want
      students to see (banking, personal email).
- [ ] Confirm the classroom internet is reaching `openrouter.ai`. Schools
      sometimes block AI domains as a precaution — see the
      [IT brief](it-brief.md) if you need a one-pager to send to IT.

## What you actually need to understand to teach this

The smallest set of mental models that makes you confident in front of
students. **You do not need to know the source code.**

### What an LLM is, in one sentence

A program that takes some text in and gives some text out, trained on a
very large amount of text. That is the whole interface.

### What an agent is, in one sentence

A program that calls an LLM in a loop and gives it tools (regular Python
functions) it can use, so the LLM can take actions, not just produce
text.

### What barebear actually is

A small framework — about 1,500 lines of Python — that runs the agent
loop, with explicit safety rails (policy, budget, checkpoints) so the
agent can't run forever or call dangerous tools without permission. The
size is deliberate: a confident GCSE student can read every line.

### The 7 names students will encounter

| Name | What it is, in plain English |
|---|---|
| **Bear** | The agent itself. The thing that runs. |
| **Task** | What you ask the agent to do. |
| **Tool** | A function the agent is allowed to call. |
| **Policy** | The rulebook. Which tools are allowed, what's the budget. |
| **State** | The agent's memory between runs (a dictionary). |
| **Checkpoint** | A pause point where a human approves before continuing. |
| **Report** | The full record of what happened — every step, every tool call. |

That's the whole vocabulary of the course. If you and your students get
fluent in those seven names, you're done.

## Troubleshooting

### "The notebook says 'model not available'"

Free-tier models on OpenRouter rotate. The lesson notebook lets you
override the model with one line. In the second code cell, set:

```python
os.environ["BAREBEAR_MODEL"] = "meta-llama/llama-3.2-3b-instruct:free"
```

Or any other model ending in `:free` from
[openrouter.ai/models](https://openrouter.ai/models). Re-run the cells.

### "I get an authentication error"

You probably copied the key with a leading or trailing space. Re-copy
the key from openrouter.ai (use the "Copy" button rather than selecting
manually) and paste again.

### "The free tier rate-limited me"

Free-tier requests are throttled. If a class of 30 students all run the
same cell at once, some may hit the limit. Two options:

1. Stagger student starts by 10–15 seconds.
2. Use the smallest free model — they're typically the most generously
   throttled.

### "Colab logged me out / lost the key"

Colab sessions reset after an hour or so of inactivity. Re-run the
"paste your key" cell — it'll prompt you again. Saving the key in your
school password manager makes this painless.

### "A student asked me a question I can't answer"

Read [`student-misconceptions.md`](student-misconceptions.md) — it has
plain-English answers to the most common ones. If a question isn't
covered there, the safest answer in front of a class is "good question,
let's investigate" — then run a quick experiment in the notebook
together. Modelling that genuine curiosity is more pedagogically
valuable than pretending you know.

## What to give yourself permission to skip

You can teach the entire course **without ever using the terminal,
without ever running `pip install`, and without ever opening the
framework source code.** Every lesson notebook is self-contained.

If a student asks "how does the framework actually work inside?" — that
is a fantastic prompt to point them at the source code on GitHub. They
can read it. So can you, if you want. Neither of you has to.

## Time commitment, honestly

- **Before you teach Lesson 1:** about 2 hours. Click through Lesson 1
  yourself, read [`lesson.md`](../../lessons/01-first-llm-call/lesson.md),
  read this document, skim the [syllabus](../../lessons/README.md). Try
  the exercise yourself.
- **Before each subsequent lesson:** 30–45 minutes. Open the notebook,
  run it end-to-end, read the lesson narrative, decide which optional
  bits to skip.
- **During the lesson:** the [pacing notes](instructor-guide.md#pacing-notes)
  estimate 50–70 minutes per lesson, fitting most double-period
  arrangements.

If you've got 6 spare evenings before next term, you can be ready.

## Where to ask for help

- **Pinned classroom thread:** [Issue #1](https://github.com/richey-malhotra/barebear/issues/1)
  is for sharing your classroom story and asking teaching-shaped
  questions.
- **Bug reports:** if something is genuinely broken, [open a normal
  issue](https://github.com/richey-malhotra/barebear/issues).
- **Curriculum questions:** comment on the pinned thread.

The repository is small and recent. Your question is likely useful for
the next teacher to land on it.

## What success looks like

By the end of the 12 weeks, your students should be able to look at any
agent-marketing claim ("our AI does X for you!") and ask the right
sceptical questions:

- *What tools does it actually have?*
- *What's its budget? Could it run away?*
- *Does it pause for human approval before sending the email / making
  the purchase?*
- *Does it tell you when it's not sure?*
- *Can I see a record of what it did?*

If a sixth-form student leaves your classroom thinking like that, this
course has done its job. So have you.
