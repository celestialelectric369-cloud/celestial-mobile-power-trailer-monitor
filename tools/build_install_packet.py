#!/usr/bin/env python3
"""
Celestial Electric - Mobile Power Trailer Monitor
Enclosure & Home-Run Install Packet generator.
Single-sources the BOM addendum + pull schedule to CSV, Markdown, and a
branded ReportLab PDF so the three never diverge.
ASCII-only text, Celestial Electric brand palette.
"""

import csv
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

OUT = "."   # run from repo root; outputs land beside the script inputs
TODAY = date.today().isoformat()
DOC_NO = "CEL-MPT-INS-001"
REV = "1.0"

# ---- Brand palette ----
CEL_ORANGE = HexColor("#F16029")
CEL_BLUE   = HexColor("#1466B0")
CEL_CYAN   = HexColor("#39C3F2")
CEL_VIOLET = HexColor("#92278F")
CEL_DARK   = HexColor("#0D0F12")
GREY_BG    = HexColor("#EEF2F5")
GREY_LINE  = HexColor("#C9D2DA")

# ---------------------------------------------------------------------------
# ASSUMPTIONS (edit these to your measured runs; footage auto-recalculates)
# ---------------------------------------------------------------------------
DOOR_RUN_FT = 25      # enclosure -> door contact
LEAK_RUN_FT = 15      # enclosure -> leak sensor (lowest point)
USB_RUN_FT  = 6       # dedicated 5V USB-C supply -> enclosure bulkhead
SLACK       = 1.15    # 15% pull slack
SERVICE_LOOP_FT = 2   # per end, per run
RUNS_SIGNAL = 2       # door + leak share one standardized cable type (22/4)

signal_ft = DOOR_RUN_FT + LEAK_RUN_FT
loops_ft  = SERVICE_LOOP_FT * 2 * RUNS_SIGNAL
cable_needed = round(signal_ft * SLACK + loops_ft)
SPOOL_REC = 100 if cable_needed <= 100 else 250

# ---------------------------------------------------------------------------
# INSTALL BOM ADDENDUM  (adds to data/bom.csv; does not replace it)
# cols: qty, item, spec, purpose, source_example, notes
# ---------------------------------------------------------------------------
BOM = [
    ("1", "Enclosure, polycarbonate NEMA 4X (non-metallic)",
     "~8x6x4 in, IP66/4X, clear or opaque lid",
     "House board + DIN terminals; RF-transparent for WiFi",
     "Bud/Polycase/Hammond or equiv",
     "MUST be non-metallic - a metal box blocks the on-board WiFi antenna."),
    ("1", "DIN rail, 35 mm", "steel/aluminum, cut to ~6 in",
     "Mount terminal blocks + board carrier",
     "AutomationDirect/DIN-rail stock",
     "Trim to enclosure interior width."),
    ("10", "Feed-through terminal blocks, 2.5 mm^2", "screw or spring, DIN-mount",
     "Land all field conductors (serviceable)",
     "Phoenix/Wago/Dinkle or equiv",
     "7 used + spares. Do NOT solder field wires to the board."),
    ("1", "Terminal end bracket + end plate set", "35 mm DIN",
     "Retain the terminal stack", "matches terminal brand",
     "2 end brackets + 1 end plate typical."),
    ("2", "Ground/shield terminal block", "grounding type, DIN-mount",
     "Single-point shield/GND landing bar", "matches terminal brand",
     "Shield lands here at ENCLOSURE end only."),
    ("3", "Cable gland, IP68", "PG7 or M12, 3.0-6.5 mm cable OD",
     "Seal + strain-relief the two signal home runs",
     "Heyco/generic nylon glands",
     "2 used (door, leak) + 1 spare. Bottom entry."),
    ("1", "USB-C panel-mount bulkhead pass-through", "IP67, C-female to C-female",
     "Power entry for the dedicated 5V supply",
     "generic IP67 USB-C bulkhead",
     "Cleaner + sealed vs. trying to gland a molded USB plug."),
    ("1", f"Shielded cable, 22 AWG / 4-cond, stranded ({SPOOL_REC} ft spool)",
     "overall foil shield + drain, ~5-6 mm OD",
     "Both home runs (standardized on one SKU)",
     "security/alarm cable (e.g. 22/4 shielded)",
     f"~{cable_needed} ft needed (door {DOOR_RUN_FT} + leak {LEAK_RUN_FT} + slack/loops). "
     "22/4 gives a spare conductor for future use."),
    ("1", "Wire ferrules, 22 AWG (0.34 mm^2) + crimp tool", "insulated ferrules assortment",
     "Terminate stranded conductors into terminals",
     "generic ferrule kit",
     "Matches Celestial ferrule discipline; prevents strand splay."),
    ("2", "Resistor, 4.7k ohm 1/4 W", "5% carbon film",
     "External pull-up: door line D2 -> 5V",
     "reuse from stock",
     "1 used + spare. Stiffens the long door line vs. noise."),
    ("2", "Panel-mount LED holder/bezel, 5 mm", "chrome or black bezel",
     "Face-mount the green/red status LEDs",
     "generic 5mm LED holders",
     "Uses the 5mm LEDs + 220 ohm from the base BOM."),
    ("4", "Anti-vibration mount / rubber isolator", "well-nut or grommet mount, M4/M5",
     "Isolate enclosure from trailer vibration",
     "McMaster/generic",
     "Prevents fatigue on solder joints + terminals."),
    ("1", "Self-fusing silicone tape + heat-shrink assortment", "-",
     "Shield termination + far-end drain dressing",
     "generic",
     "Cut + tape shield/drain at each sensor end."),
    ("1", "Wire label set (heat-shrink or self-lam wrap)", "printable",
     "Both-end labels per pull schedule",
     "Brady/generic",
     "Label DR-01, WL-01, PWR-01, ENC-01."),
    ("1", "Cable ties + adhesive mounts", "UV-rated (trailer)",
     "Dress conductors + form drip loops",
     "generic UV-black ties",
     "Use UV-rated for a mobile/outdoor environment."),
    ("1", "[FUTURE] Waterproof DS18B20 1-Wire temp probe + 4.7k", "1-Wire, waterproof lead",
     "Remote temperature WITHOUT extending I2C",
     "Adafruit/generic DS18B20",
     "Optional. I2C/BME280 must stay local; 1-Wire runs long."),
    ("2", "[FUTURE] Clamp-on ferrite core", "for 5-6 mm cable",
     "Extra EMI suppression on home runs if needed",
     "Wurth/generic",
     "Optional. Add only if noise persists after shielding."),
]
BOM_COLS = ["qty", "item", "spec", "purpose", "source_example", "notes"]

# ---------------------------------------------------------------------------
# PULL / LABEL SCHEDULE - field home runs
# cols: tag, from, to, signal, cable, conductors_used, length_ft, notes
# ---------------------------------------------------------------------------
PULLS = [
    ("DR-01", "ENC-01 TB (D2 sig + GND)", "Door contact (frame)",
     "Door open/close", "22/4 shielded", "white=sig, black=return (2 of 4)",
     str(DOOR_RUN_FT),
     "Reed on frame, magnet on leaf. Shield to GND bar at ENC end only; "
     "cut+tape at device. Drip loop at gland."),
    ("WL-01", "ENC-01 TB (D3 DO, 5V, GND)", "Leak sensor (floor/drip pan)",
     "Water/leak", "22/4 shielded", "red=V+, black=GND, white=DO (3 of 4)",
     str(LEAK_RUN_FT),
     "Mount at lowest point. Green = spare. Shield at ENC end only; "
     "cut+tape at device. Drip loop at gland."),
    ("PWR-01", "5V USB-C supply (dedicated)", "ENC-01 USB-C bulkhead",
     "5V power", "USB-C (supply lead)", "USB-C",
     str(USB_RUN_FT),
     ">= 2 A supply. Enter via IP67 bulkhead, NOT a gland. Short/quality cable; "
     "drip loop."),
]
PULL_COLS = ["tag", "from", "to", "signal", "cable", "conductors_used",
             "length_ft", "notes"]

# ---------------------------------------------------------------------------
# INTERNAL TERMINATION MAP (enclosure)
# ---------------------------------------------------------------------------
TERMS = [
    ("D2",  "TB-1 (DR sig)",  "DR-01 white", "Door signal; 4.7k pull-up TB-1 -> 5V"),
    ("GND", "TB-2 (DR ret)",  "DR-01 black", "Door return"),
    ("D3",  "TB-3 (WL DO)",   "WL-01 white", "Leak digital out"),
    ("5V",  "TB-4 (WL V+)",   "WL-01 red",   "Leak sensor power"),
    ("GND", "TB-5 (WL GND)",  "WL-01 black", "Leak return"),
    ("-",   "GND/shield bar", "both drains", "Shields land here, ENC end ONLY"),
    ("D5",  "via 220 ohm",    "green LED",   "Face LED - NORMAL (internal)"),
    ("D6",  "via 220 ohm",    "red LED",     "Face LED - ALERT (internal)"),
    ("USB-C","board USB-C port","bulkhead",  "Power from PWR-01 bulkhead"),
]
TERM_COLS = ["board_pin", "terminal", "field_conductor", "notes"]

# ===========================================================================
# EMIT CSV
# ===========================================================================
def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

write_csv(f"{OUT}/install_bom_addendum.csv", BOM_COLS, BOM)
write_csv(f"{OUT}/pull_schedule.csv", PULL_COLS, PULLS)

# ===========================================================================
# EMIT MARKDOWN
# ===========================================================================
def md_table(header, rows):
    out = "| " + " | ".join(header) + " |\n"
    out += "| " + " | ".join("---" for _ in header) + " |\n"
    for r in rows:
        cells = [str(c).replace("|", "/") for c in r]
        out += "| " + " | ".join(cells) + " |\n"
    return out

with open(f"{OUT}/install_bom_addendum.md", "w") as f:
    f.write(f"# Install BOM Addendum\n\n")
    f.write(f"**Doc:** {DOC_NO} (BOM) &middot; **Rev:** {REV} &middot; "
            f"**Date:** {TODAY} &middot; Helios Prime\n\n")
    f.write("Adds enclosure + home-run hardware to the base `data/bom.csv`. "
            "Does not replace it.\n\n")
    f.write(f"**Cable sizing (from assumptions):** door {DOOR_RUN_FT} ft + "
            f"leak {LEAK_RUN_FT} ft, +{int((SLACK-1)*100)}% slack + service loops "
            f"= ~{cable_needed} ft needed -> buy {SPOOL_REC} ft spool of 22/4 shielded.\n\n")
    f.write(md_table(["Qty", "Item", "Spec", "Purpose", "Source (example)", "Notes"], BOM))
    f.write("\n> Source links are examples/equivalents - verify before ordering. "
            "Items tagged [FUTURE] are optional.\n")

with open(f"{OUT}/pull_schedule.md", "w") as f:
    f.write(f"# Pull / Label Schedule\n\n")
    f.write(f"**Doc:** {DOC_NO} (PLL) &middot; **Rev:** {REV} &middot; "
            f"**Date:** {TODAY} &middot; Helios Prime\n\n")
    f.write("## Field home runs\n\n")
    f.write(md_table(["Tag", "From", "To", "Signal", "Cable", "Cond. used",
                      "Len (ft)", "Notes"], PULLS))
    f.write("\n## Internal termination map (enclosure)\n\n")
    f.write(md_table(["Board pin", "Terminal", "Field conductor", "Notes"], TERMS))
    f.write("\n> Shield grounded at the enclosure end ONLY; cut and tape the drain "
            "at each sensor. Label both ends of every run.\n")

# ===========================================================================
# EMIT BRANDED PDF PACKET
# ===========================================================================
styles = getSampleStyleSheet()
body = ParagraphStyle("body", parent=styles["Normal"], fontName="Helvetica",
                      fontSize=9, leading=12, textColor=CEL_DARK)
cell = ParagraphStyle("cell", parent=body, fontSize=7.6, leading=9.4)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontName="Helvetica-Bold",
                    fontSize=15, textColor=CEL_DARK, spaceBefore=6, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=11.5, textColor=CEL_BLUE, spaceBefore=10, spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=8, textColor=colors.grey)

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    # header band
    canvas.setFillColor(CEL_DARK)
    canvas.rect(0, h - 0.72*inch, w, 0.72*inch, fill=1, stroke=0)
    canvas.setFillColor(CEL_ORANGE)
    canvas.rect(0, h - 0.78*inch, w, 0.06*inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawString(0.6*inch, h - 0.42*inch, "CELESTIAL ELECTRIC")
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(CEL_CYAN)
    canvas.drawString(0.6*inch, h - 0.58*inch,
                      "Mobile Power Trailer Monitor - Enclosure & Home-Run Install Packet")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawRightString(w - 0.6*inch, h - 0.36*inch, f"DOC: {DOC_NO}")
    canvas.drawRightString(w - 0.6*inch, h - 0.48*inch, f"REV {REV}  |  {TODAY}")
    canvas.drawRightString(w - 0.6*inch, h - 0.60*inch, "Helios Prime")
    # footer
    canvas.setStrokeColor(CEL_ORANGE)
    canvas.setLineWidth(1)
    canvas.line(0.6*inch, 0.62*inch, w - 0.6*inch, 0.62*inch)
    canvas.setFillColor(colors.grey)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(0.6*inch, 0.46*inch,
        "SAFETY: Low-voltage sensing ONLY. No connection to battery / PV / inverter / "
        "generator / transfer switch / line voltage.")
    canvas.drawRightString(w - 0.6*inch, 0.46*inch, f"Page {doc.page}")
    canvas.restoreState()

def make_table(header, rows, col_widths, zebra=True):
    data = [[Paragraph(c, cellb) for c in header]]
    for r in rows:
        data.append([Paragraph(str(c), cell) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    st = [
        ("BACKGROUND", (0, 0), (-1, 0), CEL_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, GREY_LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), GREY_BG))
    t.setStyle(TableStyle(st))
    return t

doc = BaseDocTemplate(f"{OUT}/CEL-MPT-INS-001_install_packet.pdf", pagesize=letter,
                      leftMargin=0.6*inch, rightMargin=0.6*inch,
                      topMargin=0.95*inch, bottomMargin=0.8*inch)
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="pt", frames=[frame], onPage=header_footer)])

story = []
story.append(Paragraph("Enclosure &amp; Home-Run Install Packet", h1))
story.append(Paragraph(
    "Companion to the bench build. Covers the parts, cabling, terminations, and "
    "field practices to move the monitor from breadboard into the trailer with "
    "remote (long home-run) door and leak sensors on a dedicated 5V USB-C feed.", body))
story.append(Spacer(1, 6))

story.append(Paragraph("Scope &amp; assumptions", h2))
assume = [
    ["Door contact home run", f"{DOOR_RUN_FT} ft"],
    ["Leak sensor home run", f"{LEAK_RUN_FT} ft"],
    ["USB-C power run", f"{USB_RUN_FT} ft"],
    ["Pull slack + service loops", f"+{int((SLACK-1)*100)}% and {SERVICE_LOOP_FT} ft/end"],
    ["Signal cable needed", f"~{cable_needed} ft  ->  buy {SPOOL_REC} ft spool 22/4 shielded"],
]
story.append(make_table(["Parameter", "Value / result"], assume,
                        [2.4*inch, 4.9*inch], zebra=True))
story.append(Paragraph("Adjust the run lengths at the top of the generator and all "
                       "footage recalculates.", small))

story.append(Paragraph("1. Install BOM addendum", h2))
story.append(Paragraph("Adds to the base bill of materials; does not replace it. "
                       "[FUTURE] items are optional.", body))
story.append(make_table(
    ["Qty", "Item", "Spec / rating", "Purpose", "Notes"],
    [(b[0], b[1], b[2], b[3], b[5]) for b in BOM],
    [0.35*inch, 1.55*inch, 1.35*inch, 1.55*inch, 2.05*inch]))

story.append(Paragraph("2. Pull / label schedule - field home runs", h2))
story.append(make_table(
    ["Tag", "From", "To", "Cable", "Cond. used", "Len", "Notes"],
    [(p[0], p[1], p[2], p[4], p[5], p[6], p[7]) for p in PULLS],
    [0.5*inch, 1.25*inch, 1.15*inch, 0.85*inch, 1.05*inch, 0.35*inch, 2.15*inch]))

story.append(Paragraph("3. Internal termination map (enclosure)", h2))
story.append(make_table(
    ["Board pin", "Terminal", "Field conductor", "Notes"],
    TERMS,
    [0.8*inch, 1.35*inch, 1.35*inch, 3.8*inch]))

story.append(Paragraph("4. Field practices (why)", h2))
practices = [
    "<b>Non-metallic enclosure.</b> The UNO R4 WiFi uses a PCB trace antenna; a "
    "metal box is a Faraday cage and will silently kill the Cloud link. Polycarbonate "
    "NEMA 4X keeps RF and the moisture/corrosion rating.",
    "<b>Shield single-point ground.</b> Land the drain at the enclosure GND bar only; "
    "cut and tape it at each sensor. Grounding both ends creates a loop that injects "
    "noise instead of blocking it.",
    "<b>Door pull-up.</b> The internal INPUT_PULLUP (~20-50k) is too weak for a long "
    "line. A 4.7k to 5V stiffens it against EMI false-trips. The leak sensor output is "
    "actively driven, so it needs only the shield.",
    "<b>Keep BME280 local.</b> I2C is not a long-run bus. For remote temperature use a "
    "DS18B20 (1-Wire), which is built for distance.",
    "<b>Power margin + entry.</b> Feed the board USB-C from a dedicated >= 2 A supply "
    "through an IP67 bulkhead (not a gland). Undersized supplies brown out on WiFi bursts.",
    "<b>Mechanical.</b> Bottom-entry glands with drip loops; land field wires on DIN "
    "terminals (never soldered to the board); mount the enclosure on vibration isolators.",
    "<b>Firmware backstop (REV 2.0).</b> Door/leak inputs require consecutive agreeing "
    "samples before a state change, and the BME280 self-recovers from a dropped "
    "connection - both matter on a vibrating, electrically noisy trailer.",
]
for p in practices:
    story.append(Paragraph("- " + p, body))
    story.append(Spacer(1, 2))

doc.build(story)

print("cable_needed_ft:", cable_needed, "spool_rec:", SPOOL_REC)
print("wrote CSV/MD/PDF to", OUT)
