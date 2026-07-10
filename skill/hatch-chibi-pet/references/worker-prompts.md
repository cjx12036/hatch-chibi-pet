# Worker prompts

Use one visual job per worker. Keep at most two generation workers active at once.

## Base

```text
Generate the hatch-chibi-pet base image.

Run dir: <absolute run dir>
Job id: base
Prompt file: <absolute base prompt>
Input images:
- <absolute person photo> — identity reference

Use $imagegen only. Read the prompt and attach every listed input image. Enforce a cute 2.5-head-tall Q-style sticker person: oversized head, compact rounded body, short limbs, large readable expression, clean outline, simplified clothing text/logos, and the photographed person's strongest identity anchors. Reject realistic adult proportions, pixel art, scenery, shadows, text, and detached effects.

Visually check one centered full-body character on a perfectly flat chroma background. Do not edit manifests, copy files, generate rows, package, or include image previews/base64.

Return exactly:
selected_source=/absolute/path/to/output.png
qa_note=<one sentence>
```

## Row

```text
Generate one hatch-chibi-pet row.

Run dir: <absolute run dir>
Row id: <row id>
Prompt file: <absolute prompt>
Retry prompt file: <absolute retry prompt>
Input images:
- <original photo> — identity reference
- <canonical base> — canonical Q-style identity
- <layout guide> — spacing only; never copy marks

Use $imagegen only. Attach every input. If the request returns Bad Request, retry once with the retry prompt. Preserve the same oversized-head Q proportions, face, hair, glasses/accessories, outfit, palette, outline, and simplified details. Check the exact frame count, generous clean gaps, flat chroma, complete separated full-body poses, and state semantics. No guide marks, text, new props, floor, shadows, or detached effects.

Keep the same camera zoom and head diameter as the canonical idle scale. For `jumping`, require the final upright settle to be within 5% of idle standing height. Move the unchanged-scale character vertically and use tucked/crouched poses for clearance; never zoom out or shrink the character to create the arc.

Do not edit manifests, copy files, mirror rows, run scripts, package, or include image previews/base64.

Return exactly:
selected_source=/absolute/path/to/output.png
qa_note=<one sentence>
```

## Final visual QA

```text
Visually QA a finalized hatch-chibi-pet.

Run dir: <absolute run dir>
Contact sheet: <run>/qa/contact-sheet.png
Transparent frames: <run>/frames-final
Preview dir: <run>/qa/previews
Review JSON: <run>/qa/review.json
Validation JSON: <run>/final/validation.json

Inspect the contact sheet, representative actual frames, and every GIF. The green/red rectangles in the contact sheet are intentional QA cell borders. Confirm clean transparent sprite edges, a consistent cute 2.3–2.7-head-tall identity, correct nine state motions, stable size/baseline, directional gait, and an airborne jump. Row `running` means focused task processing, not locomotion.

Do not edit files.

Return exactly:
visual_qa=pass|fail
qa_note=<one sentence>
repair_rows=<comma-separated ids or none>
repair_notes=<short notes or none>
```
