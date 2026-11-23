#!/usr/bin/env python3
"""Generate the light and dark lifecycle images for the README."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
WIDTH = 1600
HEIGHT = 2800

THEMES = {
    "light": {
        "page": "#f7f9fc", "card": "#ffffff", "border": "#dfe6ef",
        "ink": "#17243b", "muted": "#5f6f85", "line": "#3f668c",
        "blue": "#2f64ad", "blue_dark": "#244f86",
        "badge": "#edf2f8", "badge_border": "#d3deea", "phase": "#eef3f8",
    },
    "dark": {
        "page": "#101722", "card": "#172233", "border": "#2b3a4e",
        "ink": "#edf4fb", "muted": "#b1bfd0", "line": "#6f91b4",
        "blue": "#4a78ba", "blue_dark": "#315b91",
        "badge": "#243449", "badge_border": "#40536b", "phase": "#1d2a3b",
    },
}

FONT_DIR = Path(r"C:\Windows\Fonts")
SERIF = str(FONT_DIR / "georgiaz.ttf")
SANS = str(FONT_DIR / "segoeui.ttf")
SANS_BOLD = str(FONT_DIR / "segoeuib.ttf")


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def draw_phase(draw, theme, title, y, height, number):
    draw.rounded_rectangle((80, y, 1520, y + height), radius=28,
                           fill=hex_rgb(theme["card"]), outline=hex_rgb(theme["border"]), width=3)
    draw.rounded_rectangle((80, y, 1520, y + 78), radius=28, fill=hex_rgb(theme["phase"]))
    draw.rectangle((80, y + 50, 1520, y + 78), fill=hex_rgb(theme["phase"]))
    draw.text((130, y + 14), f"{number}. {title}",
              font=font(SERIF, 38), fill=hex_rgb(theme["ink"]))


def badge(draw, theme, text, x, y, width=None):
    if width is None:
        width = max(130, 18 * len(text) + 48)
    draw.rounded_rectangle((x, y, x + width, y + 52), radius=26,
                           fill=hex_rgb(theme["badge"]), outline=hex_rgb(theme["badge_border"]), width=2)
    bbox = draw.textbbox((0, 0), text, font=font(SANS_BOLD, 20))
    draw.text((x + (width - (bbox[2] - bbox[0])) / 2, y + 10),
              text, font=font(SANS_BOLD, 20),
              fill=hex_rgb("#eaf1f8" if theme_name == "dark" else "#25364c"))


def wrap_line(draw, text, max_width, text_font):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=text_font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def action_box(draw, theme, lines, y):
    x, width, height = 520, 430, 100
    draw.rounded_rectangle((x, y, x + width, y + height), radius=16,
                           fill=hex_rgb(theme["blue"]), outline=hex_rgb(theme["blue_dark"]), width=3)
    text_font = font(SANS_BOLD, 23)
    wrapped = []
    for line in lines:
        wrapped.extend(wrap_line(draw, line, width - 52, text_font))
    if len(wrapped) > 3:
        wrapped = wrapped[:3]
    baseline = y + (height - len(wrapped) * 32) / 2
    for i, line in enumerate(wrapped):
        draw.text((x + 26, baseline + i * 32), line,
                  font=text_font, fill=(255, 255, 255))


def draw_step(draw, theme, number, title, icon, y, badges, lines):
    cx = 108
    draw.ellipse((cx - 28, y + 14, cx + 28, y + 70), fill=hex_rgb(theme["ink"]))
    bbox = draw.textbbox((0, 0), str(number), font=font(SANS_BOLD, 28))
    draw.text((cx - (bbox[2] - bbox[0]) / 2, y + 24), str(number),
              font=font(SANS_BOLD, 28), fill=hex_rgb(theme["page"]))
    draw.text((174, y + 25), f"{icon}  {title}",
              font=font(SANS_BOLD, 25), fill=hex_rgb(theme["ink"]))
    action_box(draw, theme, lines, y)
    for i, item in enumerate(badges):
        text = item if isinstance(item, str) else item[0]
        width = None if isinstance(item, str) else item[1]
        badge(draw, theme, text, 980, y + i * 58, width)


def build(theme_name):
    global THEME
    THEME = THEMES[theme_name]
    theme = THEME
    image = Image.new("RGB", (WIDTH, HEIGHT), hex_rgb(theme["page"]))
    draw = ImageDraw.Draw(image)

    draw.text((80, 70), "From brief to a signed, traceable outcome",
              font=font(SERIF, 64), fill=hex_rgb(theme["ink"]))
    draw.text((80, 145),
              "Start with context, move one artefact at a time, and keep evidence until the work is closed.",
              font=font(SANS, 29), fill=hex_rgb(theme["muted"]))

    draw.rounded_rectangle((80, 210, 106, 236), radius=6, fill=hex_rgb(theme["blue"]))
    draw.text((118, 204), "You decide", font=font(SANS_BOLD, 21), fill=hex_rgb(theme["ink"]))
    draw.rounded_rectangle((300, 210, 326, 236), radius=6,
                           fill=hex_rgb(theme["badge"]), outline=hex_rgb(theme["badge_border"]), width=2)
    draw.text((338, 204), "Agents draft", font=font(SANS_BOLD, 21), fill=hex_rgb(theme["ink"]))
    draw.rounded_rectangle((535, 210, 561, 236), radius=6, fill=hex_rgb(theme["ink"]))
    draw.text((573, 204), "Gate or step", font=font(SANS_BOLD, 21), fill=hex_rgb(theme["ink"]))

    draw_phase(draw, theme, "Set up the workbench", 285, 500, "1")
    draw_step(draw, theme, 1, "Start", "⌂", 390, ["/start-here", "/setup-check"],
              ["Open this folder as the project.", "The hook and ledger become active."])
    draw_step(draw, theme, 2, "Make it yours", "◉", 520, ["/onboard", ("context-check", 170)],
              ["Fill product, team and policy context.", "Use /onboard or edit the context files."])
    draw_step(draw, theme, 3, "Choose the work", "≡", 650, ["/new-initiative", "/track"],
              ["Create work/<slug> from the brief.", "Choose the full or lite track."])

    draw_phase(draw, theme, "Discover and decide", 815, 500, "2")
    draw_step(draw, theme, 4, "Add evidence", "＋", 920, ["/discover", ("inputs/", 150)],
              ["Put interviews, tickets and data in", "work/<slug>/inputs/."])
    draw_step(draw, theme, 5, "Frame the opportunity", "△", 1050, ["/frame", "/prioritise"],
              ["Discover, frame and compare options.", "Read the findings and approve each gate."])
    draw_step(draw, theme, 6, "Write the PRD", "▤", 1180, ["/prd", "/coverage"],
              ["Create stable requirement IDs.", "Add BDD acceptance before sign-off."])

    draw_phase(draw, theme, "Draft, check and refine", 1345, 610, "3")
    draw_step(draw, theme, 7, "Build the backlog chain", "◫", 1450, ["/stories", "/test-scenarios"],
              ["Link requirement → story → test.", "Every scenario carries a stable ID."])
    draw_step(draw, theme, 8, "Independently review", "◇", 1580, ["/critique", "/trace"],
              ["Run a critic, coverage or trace check.", "Fix gaps before approval."])
    draw_step(draw, theme, 9, "Refine and release", "✓", 1710, ["/refine", "/release"],
              ["Prepare refinement and rollout.", "A full track adds comms and post-launch."])

    draw_phase(draw, theme, "Hand off, build and close", 1985, 520, "4")
    draw_step(draw, theme, 10, "Create a build spec", "⌁", 2090, ["/handoff", "build-spec-writer"],
              ["Copy approved story and AC verbatim.", "Fill every TECH LEAD gap before approval."])
    draw_step(draw, theme, 11, "Build and test", "⚙", 2220, ["/trace", "@scenario-id"],
              ["Developers or coding agents build.", "Tests carry the scenario IDs back."])
    draw_step(draw, theme, 12, "Close the loop", "↺", 2350, ["/close", "/post-launch"],
              ["Compare evidence with the PRD.", "Reopen gaps or start the next round."])

    draw.text((140, 2550),
              "New evidence starts the next round; /start-here tells you where to begin.",
              font=font(SERIF, 25), fill=hex_rgb(theme["muted"]))

    draw.rectangle((0, 2690, WIDTH, 2800), fill=hex_rgb(theme["ink"]))
    draw.text((80, 2718), "github.com/bdesouza291/ai_po_playbook",
              font=font(SANS, 21), fill=hex_rgb(theme["page"]))
    draw.text((1520, 2718), "AI Product Owner template",
              font=font(SANS, 21), anchor="ra", fill=hex_rgb(theme["page"]))

    output = ROOT / f"lifecycle-{theme_name}.png"
    image.save(output, "PNG")


for theme_name in ("light", "dark"):
    build(theme_name)

print("Generated lifecycle-light.png and lifecycle-dark.png")
