"""Build the README header demo gif.

Renders a typewriter-style animation of a real BareBear `trace=True` run.
Output: assets/demo.gif at the repo root.

Run:
    python3 scripts/build_demo_gif.py
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "demo.gif"

WIDTH = 880
HEIGHT = 520
PAD_X = 26
PAD_Y = 26
LINE_HEIGHT = 22
FONT_SIZE = 15

BG = (13, 17, 23)
FG = (220, 226, 232)
DIM = (140, 150, 160)
ACCENT_GREEN = (126, 211, 33)
ACCENT_BLUE = (125, 196, 255)
ACCENT_PURPLE = (199, 146, 234)
ACCENT_YELLOW = (240, 200, 100)
ACCENT_RED = (255, 130, 130)

LINE_FRAME_MS = 220
PAUSE_FRAME_MS = 700
FINAL_HOLD_MS = 2400


def load_mono_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFNSMono.ttf",
        "/Library/Fonts/Menlo.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = load_mono_font(FONT_SIZE)


def color_for(line: str) -> tuple[int, int, int]:
    s = line.strip()
    if not s:
        return FG
    if s.startswith("$"):
        return ACCENT_YELLOW
    if "BAREBEAR run" in s or "status: completed" in s:
        return ACCENT_PURPLE
    if s.startswith("─── turn"):
        return ACCENT_BLUE
    if s.startswith(">"):
        return DIM
    if s.startswith("<"):
        return ACCENT_GREEN
    if s.startswith("→"):
        return FG
    if s.startswith("=="):
        return DIM
    if s.startswith("goal:") or s.startswith("tools:"):
        return DIM
    return FG


SCRIPT = [
    "$ python lesson_02_agent_loop.py",
    "",
    "============================================================",
    "BAREBEAR run — task: a1b2c3d4",
    "goal: Greet a user named Alice",
    "tools: ['greet']",
    "============================================================",
    "",
    "─── turn 1 ───",
    "> calling model with 2 messages, 1 tools available",
    "< tool call: greet(name=\"Alice\")",
    "→ greet returned: Hello, Alice!",
    "",
    "─── turn 2 ───",
    "> calling model with 4 messages, 1 tools available",
    "< final answer: Hello, Alice! How can I help you today?",
    "",
    "============================================================",
    "status: completed  |  turns: 2  |  tokens: 187  |  cost: $0.0001",
    "============================================================",
]


def draw_window_chrome(draw: ImageDraw.ImageDraw) -> None:
    bar_h = 30
    draw.rectangle([(0, 0), (WIDTH, bar_h)], fill=(40, 44, 52))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 18 + i * 22
        cy = bar_h // 2
        draw.ellipse([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=color)
    draw.text((WIDTH // 2 - 70, 8), "barebear — agent loop", fill=DIM, font=FONT)


def render_frame(visible_lines: list[str], cursor: bool) -> Image.Image:
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_window_chrome(draw)

    y = PAD_Y + 30
    for line in visible_lines:
        draw.text((PAD_X, y), line, fill=color_for(line), font=FONT)
        y += LINE_HEIGHT

    if cursor and visible_lines:
        last = visible_lines[-1]
        bbox = FONT.getbbox(last)
        text_w = bbox[2] - bbox[0]
        cx = PAD_X + text_w + 4
        cy = y - LINE_HEIGHT
        draw.rectangle([(cx, cy + 3), (cx + 9, cy + LINE_HEIGHT - 4)], fill=FG)
    return img


def build_frames() -> tuple[list[Image.Image], list[int]]:
    """One frame per visible-state, with explicit per-frame durations.

    Line-at-a-time reveal: short pause for normal lines, longer pause when
    the loop reaches a turn boundary or a tool call so the eye can land.
    """
    frames: list[Image.Image] = []
    durations: list[int] = []

    rendered: list[str] = []
    for line in SCRIPT:
        rendered.append(line)
        frames.append(render_frame(rendered, cursor=line != "" and not line.startswith("=")))

        s = line.strip()
        if (
            s.startswith("─── turn")
            or s.startswith("→")
            or s.startswith("< final")
            or s.startswith("status:")
        ):
            durations.append(PAUSE_FRAME_MS)
        elif line == "":
            durations.append(LINE_FRAME_MS // 2)
        else:
            durations.append(LINE_FRAME_MS)

    # Hold the completed terminal at the end before the gif loops.
    final = render_frame(rendered, cursor=False)
    frames.append(final)
    durations.append(FINAL_HOLD_MS)
    return frames, durations


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames, durations = build_frames()
    print(f"rendering {len(frames)} frames -> {OUT}")
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    size_kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
