---
name: hatch-chibi-pet
description: Create, repair, validate, package, and install a cute Q-style animated Codex desktop pet from any uploaded single-person photo. Use when a user asks to turn a portrait or full-body person image into a chibi/Q版/卡通 Codex pet, generate the full 8x9 pet spritesheet with nine app states, remove the background cleanly, or install/share a reusable custom pet package.
---

# Hatch Chibi Pet

Turn one or more photos of a person into a consistent animated Codex pet. Default to a polished chibi sticker style, generate every required state with `$imagegen`, assemble geometry deterministically, remove chroma spill twice, validate, package, and install.

## Required resources

At the start of a run:

1. Read `${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/SKILL.md` completely.
2. Read `references/codex-pet-contract.md`, `references/animation-rows.md`, and `references/qa-rubric.md`.
3. Read `references/worker-prompts.md` before delegating visual jobs.
4. Use the scripts bundled in this skill. Resolve `SKILL_DIR` to this skill directory; do not depend on another installation of `hatch-pet`.

Use `$imagegen` as the only visual-generation layer. Use local scripts only for layout guides, copying, chroma cleanup, frame extraction, atlas assembly, validation, previews, and packaging.

## Default visual contract

Unless the user requests another style, enforce all of the following:

- Cute Q-version/chibi sticker character, approximately 2.3–2.7 heads tall.
- Head occupies about 40–46% of total character height.
- Compact rounded torso, short limbs, slightly oversized hands and shoes.
- Large readable eyes and expression; simplify tiny facial detail without changing identity.
- Preserve 3–6 strong identity anchors from the photo: hairstyle, glasses, braid, face shape, signature clothing colors, pose energy, or another obvious feature.
- Simplify or remove unreadable clothing text, badges, logos, and tiny patterns.
- Clean dark outline, flat color regions, minimal soft cel shading, no pixel-art texture.
- Full body, isolated silhouette, no scenery, floor, shadow, text, watermark, or detached effects.
- The same face, hair, accessories, outfit, palette, and proportions in every row.
- Keep the same camera zoom and head diameter across rows. In `jumping`, the upright settle frame must be within 5% of the idle standing height; create the airborne arc with vertical translation and tucked/crouched poses, never by zooming out or shrinking the character.

Reject realistic adult proportions, tiny heads, long limbs, dense photographic detail, pixelated output, or a generic anime character that loses the photographed person's identity.

## Visible progress

Keep this four-step checklist updated:

1. Prepare `<Pet>` from the photo.
2. Generate `<Pet>`'s Q-style main look.
3. Generate and repair nine animation rows.
4. Assemble, validate, install, and export `<Pet>`.

Invocation of this skill authorizes internal lightweight subagents for image jobs unless the user explicitly forbids them. Use no more than two generation workers concurrently. Keep one visual job per worker turn.

## 1. Inspect and prepare

Treat uploaded photos as identity references, not direct cutout targets. Inspect the image and infer:

- a short friendly display name and ASCII `pet_id` if omitted;
- a one-sentence description;
- 3–6 identity anchors;
- clothing details to preserve and logos/text to simplify;
- an appropriate chroma key selected by the preparation script.

Prepare a run:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/hatch-chibi-pet"
python3 "$SKILL_DIR/scripts/prepare_pet_run.py" \
  --pet-name "<Display Name>" \
  --pet-id "<ascii-id>" \
  --description "<one sentence>" \
  --reference /absolute/path/to/person.jpg \
  --output-dir /absolute/path/to/run \
  --pet-notes "<identity anchors; simplified clothing; warm personality>" \
  --style-preset chibi \
  --style-notes "2.5-head-tall cute Q-style sticker person; oversized head; compact rounded body; short limbs; large readable expression; preserve identity anchors; simplify clothing text and logos; no pixel art; no photoreal adult proportions" \
  --force
```

Use `python` only when `python3` is unavailable. Inspect `pet_request.json` and `imagegen-jobs.json` before generation.

## 2. Generate the base and rows

Generate `base` first. Copy the selected output to its `decoded/` path and also to `references/canonical-base.png`; then mark the job complete.

Generate row jobs with every input listed in `imagegen-jobs.json`. Always attach the original photo, canonical base, and row layout guide when listed. Start with `idle` and `running-right` to verify identity, Q proportions, and gait.

Generate `running-left` as a fresh row by default. Do not mirror a model-generated `running-right` strip unless its frame boundaries are exact and visual inspection proves that no body part crosses an inferred slot boundary. Fresh generation is safer for human characters.

Generate all nine required states:

`idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`.

The non-directional `running` state means focused task processing, not foot-running. Use eye, head, hand, or thinking motion without new props.

Workers return only:

```text
selected_source=/absolute/path/to/output.png
qa_note=<one sentence>
```

Delete a selected original under `${CODEX_HOME:-$HOME/.codex}/generated_images` only after its decoded copy exists.

## 3. Clean chroma and assemble

After every row is complete, clean each decoded strip before extraction. Read the selected key from `pet_request.json`:

```bash
RUN_DIR=/absolute/path/to/run
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/hatch-chibi-pet"
KEY=$(jq -r '.chroma_key.hex' "$RUN_DIR/pet_request.json")
mkdir -p "$RUN_DIR/decoded-clean"
for state in idle running-right running-left waving jumping failed waiting running review; do
  python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
    --input "$RUN_DIR/decoded/$state.png" \
    --out "$RUN_DIR/decoded-clean/$state.png" \
    --auto-key border --soft-matte \
    --transparent-threshold 12 --opaque-threshold 220 \
    --despill --force
done
```

Use stable slots to preserve jump height and row-level baseline:

```bash
python3 "$SKILL_DIR/scripts/extract_strip_frames.py" \
  --decoded-dir "$RUN_DIR/decoded-clean" \
  --output-dir "$RUN_DIR/frames" \
  --states all --method stable-slots \
  --chroma-key "$KEY" --key-threshold 96
```

Run a second chroma cleanup on extracted frames to remove low-alpha neon specks. This is required even when the first validation reports no errors:

```bash
mkdir -p "$RUN_DIR/frames-final"
for state_dir in "$RUN_DIR"/frames/{idle,running-right,running-left,waving,jumping,failed,waiting,running,review}; do
  state=$(basename "$state_dir")
  mkdir -p "$RUN_DIR/frames-final/$state"
  for frame in "$state_dir"/*.png; do
    python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/remove_chroma_key.py" \
      --input "$frame" \
      --out "$RUN_DIR/frames-final/$state/$(basename "$frame")" \
      --key-color "$KEY" --auto-key none --soft-matte \
      --transparent-threshold 160 --opaque-threshold 220 \
      --despill --force
  done
done
cp "$RUN_DIR/frames/frames-manifest.json" "$RUN_DIR/frames-final/frames-manifest.json"
```

Inspect, assemble, validate, and render QA artifacts:

```bash
mkdir -p "$RUN_DIR/final" "$RUN_DIR/qa"
python3 "$SKILL_DIR/scripts/inspect_frames.py" \
  --frames-root "$RUN_DIR/frames-final" \
  --json-out "$RUN_DIR/qa/review.json" \
  --require-components --allow-stable-slots
python3 "$SKILL_DIR/scripts/compose_atlas.py" \
  --frames-root "$RUN_DIR/frames-final" \
  --output "$RUN_DIR/final/spritesheet.png" \
  --webp-output "$RUN_DIR/final/spritesheet.webp"
python3 "$SKILL_DIR/scripts/validate_atlas.py" \
  "$RUN_DIR/final/spritesheet.webp" \
  --json-out "$RUN_DIR/final/validation.json"
python3 "$SKILL_DIR/scripts/make_contact_sheet.py" \
  "$RUN_DIR/final/spritesheet.webp" \
  --output "$RUN_DIR/qa/contact-sheet.png"
python3 "$SKILL_DIR/scripts/render_animation_previews.py" \
  --frames-root "$RUN_DIR/frames-final" \
  --output-dir "$RUN_DIR/qa/previews"
```

## 4. Visual QA and repair

Deterministic validation is necessary but not sufficient. Use one fresh visual-QA worker to inspect the contact sheet, actual transparent frames, and nine GIFs.

The green outlines around used cells and red outlines around unused cells in the contact sheet are QA borders, not chroma spill. Inspect the sprite pixels inside cells and actual frames.

Require:

- exact identity and Q proportions across rows;
- clean transparent edges with no neon key-colored fringe or speckles;
- visible but calm idle motion;
- alternating left/right gait with correct facing;
- a clearly airborne jumping frame preserved by stable slots;
- jumping at the established idle/waving camera scale: equal head diameter and an upright settle height within 5% of idle; airborne frames may have smaller bounding boxes only because the body is tucked;
- no clipping, slot fragments, detached effects, size popping, or new props;
- distinct failed, waiting, processing, and review semantics.

Repair the smallest failing row. Regenerate a row when its source imagery is wrong. Repeat chroma cleanup when only edges fail. Never accept an atlas solely because JSON validation passes.

If two `$imagegen` repairs preserve the correct poses and identity but still render one entire row at a uniformly different camera scale, normalize that extracted row deterministically instead of regenerating forever. Use the upright frame as the target and preserve every frame's original center/trajectory:

```bash
python3 "$SKILL_DIR/scripts/normalize_row_scale.py" \
  --reference "$RUN_DIR/frames-final/idle/00.png" \
  --input-dir "$RUN_DIR/frames-final/jumping" \
  --output-dir "$RUN_DIR/frames-normalized/jumping" \
  --target-frame last
```

Accept this only when the scale factor is at most `1.5`, no frame clips, the row already passed semantic QA, and the same uniform factor is applied to every frame. Re-run inspection, atlas composition, validation, contact sheet, previews, and independent visual QA afterward.

LANCZOS normalization may create disconnected low-alpha key-colored dots. After normalization, run the same second-pass per-frame chroma cleanup on the normalized outputs before replacing the production row; never package the raw normalized frames.

## 5. Package and install

After QA passes, install under `${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/`:

```text
pet.json
spritesheet.webp
```

Manifest:

```json
{
  "id": "<pet-id>",
  "displayName": "<Display Name>",
  "description": "<one sentence>",
  "spritesheetPath": "spritesheet.webp"
}
```

Also export a shareable ZIP containing the same two files plus `contact-sheet.png`, `validation.json`, and preview GIFs. Do not overwrite an existing pet id unless the user explicitly requests replacement; choose a versioned id instead.

Tell the user to open `Settings → Pets`, refresh, select the new pet, and run `Show pet` if the current app session does not refresh automatically.

Report the installed id, package path, deliverable ZIP, validation result, final style/identity prompt summary, and that the built-in `$imagegen` path was used.
