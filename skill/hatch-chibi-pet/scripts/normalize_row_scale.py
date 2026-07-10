#!/usr/bin/env python3
"""Uniformly scale one extracted animation row to a reference standing height."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


def alpha_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.convert("RGBA").getchannel("A").getbbox()
    if bbox is None:
        raise SystemExit("frame has no visible pixels")
    return bbox


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def scale_frame(image: Image.Image, factor: float, margin: int) -> Image.Image:
    rgba = image.convert("RGBA")
    left, top, right, bottom = alpha_bbox(rgba)
    sprite = rgba.crop((left, top, right, bottom))
    width = max(1, round(sprite.width * factor))
    height = max(1, round(sprite.height * factor))
    max_width = rgba.width - margin * 2
    max_height = rgba.height - margin * 2
    if width > max_width or height > max_height:
        raise SystemExit(
            f"scaled sprite {width}x{height} exceeds safe area "
            f"{max_width}x{max_height}"
        )

    sprite = sprite.resize((width, height), Image.Resampling.LANCZOS)
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    out_left = clamp(round(center_x - width / 2), margin, rgba.width - margin - width)
    out_top = clamp(round(center_y - height / 2), margin, rgba.height - margin - height)
    output = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
    output.alpha_composite(sprite, (out_left, out_top))

    pixels = output.load()
    for y in range(output.height):
        for x in range(output.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha == 0 and (red or green or blue):
                pixels[x, y] = (0, 0, 0, 0)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--target-frame",
        default="last",
        help="Frame used to calculate scale: first, last, or a file name.",
    )
    parser.add_argument("--margin", type=int, default=4)
    parser.add_argument("--max-factor", type=float, default=1.5)
    args = parser.parse_args()

    frames = sorted(args.input_dir.glob("*.png"))
    if not frames:
        raise SystemExit(f"no PNG frames in {args.input_dir}")
    if args.target_frame == "first":
        target_path = frames[0]
    elif args.target_frame == "last":
        target_path = frames[-1]
    else:
        target_path = args.input_dir / args.target_frame
        if target_path not in frames:
            raise SystemExit(f"target frame not found: {target_path}")

    reference = Image.open(args.reference).convert("RGBA")
    target = Image.open(target_path).convert("RGBA")
    ref_bbox = alpha_bbox(reference)
    target_bbox = alpha_bbox(target)
    reference_height = ref_bbox[3] - ref_bbox[1]
    target_height = target_bbox[3] - target_bbox[1]
    factor = reference_height / target_height
    if factor <= 0 or factor > args.max_factor:
        raise SystemExit(
            f"unsafe scale factor {factor:.4f}; max allowed is {args.max_factor:.4f}"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for frame_path in frames:
        output = scale_frame(Image.open(frame_path), factor, args.margin)
        output_path = args.output_dir / frame_path.name
        output.save(output_path)
        bbox = alpha_bbox(output)
        results.append(
            {
                "frame": frame_path.name,
                "bbox": list(bbox),
                "width": bbox[2] - bbox[0],
                "height": bbox[3] - bbox[1],
            }
        )

    print(
        json.dumps(
            {
                "ok": True,
                "reference": str(args.reference),
                "target_frame": str(target_path),
                "reference_height": reference_height,
                "target_height_before": target_height,
                "scale_factor": round(factor, 6),
                "output_dir": str(args.output_dir),
                "frames": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
