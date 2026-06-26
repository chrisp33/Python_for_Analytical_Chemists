---
description: Build the full PFAC video package for a lesson (brief + five-beat structure + publish draft)
argument-hint: <lesson-ID> [brief|structure|publish]  e.g. "2.6" or "2.6 structure"
---

You are producing the **video package** for PFAC lesson `$ARGUMENTS`.

PFAC = "Python for Analytical Chemists." The brand is *use Python to become a more
capable scientist* — measurement judgment is the moat, code is the easy part. Every
lesson is briefed and built scientist-to-scientist, never as a Python tutorial.

## Step 1 — Parse the request

`$ARGUMENTS` is a lesson ID (e.g. `2.6`) optionally followed by a stage word:
- no stage word, or `all` → produce **all three** artifacts below
- `brief` → only the content brief
- `structure` → only the five-beat lesson structure
- `publish` → only the YouTube publish draft

## Step 2 — Ground yourself in the real lesson (do this before writing anything)

1. Find the lesson directory under `notebooks/` (the folder whose name starts with
   the ID, e.g. `notebooks/02_scientific_computing/2.6_*/`). If no match, stop and
   say so — never invent a lesson.
2. Read its `README.md` and the `.ipynb` (dump the markdown + code cells). The brief
   and structure must cite **real cells, outputs, and figures** — the hero figure,
   the specific functions, the actual numbers. No generic claims.
3. Skim `private/strategy/content_strategy.md` (pillars, audience) and
   `private/strategy/Domain.md` (the measurement-judgment clusters) for positioning.

## Step 3 — Read the templates and an exemplar

- Brief template: `private/content/templates/content_brief_v3.md`
- Structure template: `private/content/templates/lesson_structure_v1.md`
- Exemplar publish package (match this format): `private/content/2.5_plotting_that_reveals_chemistry/youtube_package_v1.md`
- Exemplar filled brief + structure: `private/content/2.6_missing_values_and_detector_dropouts/`

Follow the templates' own drift checks and tests (deadline test, moat test). The
**moat test is non-negotiable**: if a generic Python educator with no measurement
background could have written a section, the domain layer is too thin — rewrite it.

## Step 4 — Write the artifacts

Output directory: `private/content/<lesson-dir-name>/` (create if missing). **Never
overwrite an existing file without flagging it first** — if a target already exists,
read it, tell the user, and ask before replacing.

1. **`content_brief_v3.md`** — fill every section of the v3 template, spine first
   (Part 1: trigger → job → scenario → decision → consequence → Python's role →
   domain layer → transferable lesson), grounded in the notebook's cells.

2. **`lesson_structure.md`** — pour the brief into the five-beat arc:
   **Problem → Evidence → Judgment → Code → Rule.** Order is non-negotiable.
   - Beat 1 opens on a measurement problem/failure mode, never on Python.
   - Beat 2 shows real data (name the hero figure/cell) before any code.
   - Beat 3 (Scientific Judgment) is the **heart** — give it the most runtime and
     the most care; it must pass the moat test.
   - Beat 4 (Code) shows only the judgment-bearing lines; boilerplate stays
     off-screen. If the code beat would be the longest, that is tutorial drift.
   - Beat 5 lands **one** concise, applicable rule (not the notebook's full
     takeaways list).
   Include a runtime budget keyed to the README's stated length, and the
   template's drift checklist.

3. **`youtube_package_v1.md`** — match the 2.5 exemplar's structure (ranked titles,
   thumbnail concept, description with above-the-fold + "what you'll learn",
   chapters, tags, end screen/cards, pre-publish checklist). **Timecode-dependent
   parts (chapters/timestamps, runtime) can only be finalized from the recorded
   cut** — fill them with clearly-marked placeholders and say so, unless the lesson
   is already filmed and timecodes exist.

## Step 5 — Report

Summarize what you wrote with clickable links, call out the **moat** for this lesson
in one line, and name the single biggest drift risk in the eventual cut (usually:
which beat is at risk of running long). If you only produced one stage, say which
stages remain.
