"""
vinFMEA Marketing Video 4: Control Plans & Standards Compliance
Duration: ~55 seconds | 1080p | 30fps | Professional Voiceover + Sitar
Showcases: Auto-generated control plans, AIAG-VDA/ISO 26262/IATF 16949/IEC 61508, multi-language, floating licenses
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

from voice_utils import create_voiceover_track, mux_video_audio_with_music

# ── Voiceover segments ──
VO_SEGMENTS = [
    ("vinFMEA. Control plans and standards compliance.", 0.5, 4.5),
    ("Control plans are generated automatically from your process FMEA. "
     "Every characteristic, specification, and reaction plan flows directly from your risk analysis. "
     "No manual data entry, no copy-paste errors.",
     6.0, 20.0),
    ("vinFMEA supports the major industry standards out of the box. "
     "AIAG-VDA for automotive, ISO 26262 for functional safety, "
     "IATF 16949, and IEC 61508 for industrial applications.",
     22.0, 40.0),
    ("Work in any of eight supported languages — English, German, Chinese, Japanese, and more. "
     "Floating licenses let your entire team collaborate. Five licenses, unlimited users.",
     42.0, 55.0),
    ("vinFMEA. Auto-generated control plans, global standards, any language. "
     "Start your free trial at vinfmea.com.",
     57.0, 66.0),
]

# ── Brand colours ──
BG_DARK    = "#0F172A"
BG_CARD    = "#1E293B"
AMBER      = "#F59E0B"
AMBER_LIGHT = "#FCD34D"
WHITE      = "#FFFFFF"
GRAY       = "#94A3B8"
RED        = "#EF4444"
GREEN      = "#10B981"
BLUE       = "#2563EB"
TEAL       = "#0D9488"
CYAN       = "#22D3EE"
PURPLE     = "#7C3AED"

FPS = 30
DURATION = 70
TOTAL_FRAMES = FPS * DURATION

fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_DARK)


def draw_frame(frame):
    fig.clear()
    fig.set_facecolor(BG_DARK)
    phase = frame / FPS

    # ═══════════════════════════════════════════════════════════
    #  SCENE 1: Title Card (0–5s)
    # ═══════════════════════════════════════════════════════════
    if phase < 5:
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        progress = min(1.0, phase / 2.0)
        alpha_t = min(1.0, phase / 1.5)
        alpha_s = min(1.0, max(0, (phase - 0.8) / 1.2))
        alpha_b = min(1.0, max(0, (phase - 2.0) / 1.0))

        # Amber accent line
        line_w = progress * 0.4
        ax.plot([0.3, 0.3 + line_w], [0.58, 0.58], color=AMBER, lw=4, alpha=alpha_t)

        ax.text(0.5, 0.68, "vinFMEA", fontsize=58, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha_t,
                fontfamily='sans-serif')
        ax.text(0.5, 0.50, "Control Plans & Standards Compliance",
                fontsize=24, color=AMBER_LIGHT, ha='center', va='center', alpha=alpha_s,
                fontfamily='sans-serif', fontstyle='italic')

        badges = ["Auto-Generated", "AIAG-VDA", "ISO 26262", "8 Languages"]
        for i, feat in enumerate(badges):
            x = 0.2 + i * 0.2
            delay = 2.2 + i * 0.35
            a = min(1.0, max(0, (phase - delay) / 0.8))
            rect = FancyBboxPatch((x - 0.08, 0.30), 0.16, 0.06,
                                   boxstyle="round,pad=0.01",
                                   facecolor=AMBER, alpha=a * 0.3, edgecolor=AMBER,
                                   linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, 0.33, feat, fontsize=11, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='600')

    # ═══════════════════════════════════════════════════════════
    #  SCENE 2: Control Plan Auto-Generation (5–21s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 21:
        t_local = phase - 5

        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1920); ax.set_ylim(0, 1080)
        ax.set_facecolor(BG_DARK); ax.axis('off')
        ax.invert_yaxis()

        # Scene title
        title_a = min(1.0, t_local / 1.0)
        ax.text(960, 40, "CONTROL PLAN — AUTO-GENERATED FROM PFMEA",
                fontsize=20, color=AMBER_LIGHT, ha='center', va='center',
                fontweight='bold', alpha=title_a)

        # "Auto-generated from PFMEA" badge with arrow
        badge_a = min(1.0, max(0, (t_local - 0.5) / 1.0))

        # Mini PFMEA icon (small box on the left)
        pfmea_box = FancyBboxPatch((80, 70), 140, 50, boxstyle="round,pad=4",
                                    facecolor=PURPLE, alpha=badge_a * 0.8, edgecolor=PURPLE,
                                    linewidth=1.5)
        ax.add_patch(pfmea_box)
        ax.text(150, 96, "PFMEA", fontsize=13, color=WHITE, ha='center', va='center',
                fontweight='bold', alpha=badge_a)

        # Arrow from PFMEA to badge
        arrow_progress = min(1.0, max(0, (t_local - 1.0) / 0.8))
        if arrow_progress > 0:
            arrow_end_x = 230 + arrow_progress * 100
            ax.annotate('', xy=(arrow_end_x, 95), xytext=(225, 95),
                       arrowprops=dict(arrowstyle='->', color=AMBER, lw=2.5,
                                      alpha=arrow_progress))

        # Auto-generated badge
        gen_badge_a = min(1.0, max(0, (t_local - 1.8) / 0.8))
        gen_badge = FancyBboxPatch((340, 72), 260, 46, boxstyle="round,pad=4",
                                    facecolor=GREEN, alpha=gen_badge_a * 0.25,
                                    edgecolor=GREEN, linewidth=1.5)
        ax.add_patch(gen_badge)
        ax.text(470, 96, "Auto-generated from PFMEA", fontsize=13, color=GREEN,
                ha='center', va='center', fontweight='600', alpha=gen_badge_a)

        # Control Plan document header
        doc_bg = FancyBboxPatch((60, 140), 1800, 60, boxstyle="round,pad=4",
                                 facecolor=BG_CARD, edgecolor=AMBER, linewidth=2,
                                 alpha=title_a)
        ax.add_patch(doc_bg)
        ax.text(960, 172, "Control Plan — Engine Block Assembly",
                fontsize=22, color=WHITE, ha='center', va='center',
                fontweight='bold', alpha=title_a)

        # Column headers
        col_headers = ["Op#", "Process Step", "Characteristic", "Specification",
                       "Method", "Sample", "Freq.", "Reaction Plan"]
        col_x = [90, 210, 480, 750, 1000, 1210, 1370, 1580]
        col_w = [90, 240, 240, 220, 180, 130, 160, 280]

        header_a = min(1.0, max(0, (t_local - 1.0) / 0.8))

        # Header row background
        hdr_bg = FancyBboxPatch((60, 210), 1800, 45, boxstyle="square",
                                 facecolor=AMBER, alpha=header_a * 0.2, edgecolor='none')
        ax.add_patch(hdr_bg)

        for hx, hdr in zip(col_x, col_headers):
            ax.text(hx, 234, hdr, fontsize=12, color=AMBER_LIGHT,
                    fontweight='700', va='center', alpha=header_a)

        # Control plan rows with realistic automotive data
        cp_rows = [
            ("10", "Rough Bore", "Bore Diameter", "82.000 ±0.025 mm",
             "CMM Probe", "5 pcs", "Every lot", "Quarantine & re-measure"),
            ("20", "Finish Bore", "Surface Roughness", "Ra 0.8 µm max",
             "Profilometer", "3 pcs", "Per shift", "Adjust feed rate, re-check"),
            ("30", "Deck Surface", "Flatness", "0.05 mm / 300 mm",
             "Dial Indicator", "1 pc", "Hourly", "Resurface & verify"),
            ("40", "Head Bolt Torque", "Torque Value", "95 ±5 Nm",
             "Torque Wrench", "100%", "Each assy", "Re-torque, escalate to QE"),
            ("50", "Coolant Passage", "Leak Test", "0.5 bar / 30 sec hold",
             "Pressure Test", "100%", "Each unit", "Reject & NCR, root cause"),
            ("60", "Final Inspect", "Visual / Dimensional", "Per drawing Rev C",
             "Go/No-Go Gage", "AQL 1.0", "Per lot", "Hold lot, sort 100%"),
        ]

        for i, (op, process, char, spec, method, sample, freq, reaction) in enumerate(cp_rows):
            delay = 2.5 + i * 1.2
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            y = 280 + i * 60

            # Row stripe
            if i % 2 == 0:
                stripe = FancyBboxPatch((60, y - 8), 1800, 52, boxstyle="square",
                                         facecolor=WHITE, alpha=a * 0.04, edgecolor='none')
                ax.add_patch(stripe)

            # Row separator line
            sep_line_a = a * 0.15
            ax.plot([60, 1860], [y - 8, y - 8], color=GRAY, lw=0.5, alpha=sep_line_a)

            row_data = [op, process, char, spec, method, sample, freq, reaction]
            row_colors = [AMBER, WHITE, CYAN, WHITE, GRAY, GRAY, GRAY, AMBER_LIGHT]
            row_weights = ['bold', '500', '600', '400', '400', '400', '400', '500']
            row_sizes = [13, 12, 12, 11, 11, 11, 11, 11]

            for val, cx, clr, fw, fs in zip(row_data, col_x, row_colors, row_weights, row_sizes):
                display_val = val[:32] if len(val) > 32 else val
                ax.text(cx, y + 18, display_val, fontsize=fs, color=clr,
                        va='center', fontweight=fw, alpha=a)

        # Bottom: row count indicator
        if t_local > 9:
            count_a = min(1.0, (t_local - 9) / 1.0)
            ax.text(960, 660, "6 control points auto-populated — 0 manual entries",
                    fontsize=14, color=GREEN, ha='center', va='center',
                    fontweight='600', alpha=count_a)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 3: Standards Compliance Cards (21–41s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 41:
        t_local = phase - 21

        ax = fig.add_axes([0.02, 0.05, 0.96, 0.88])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        fig.text(0.5, 0.96, "INDUSTRY STANDARDS — BUILT IN, NOT BOLTED ON",
                 fontsize=20, color=AMBER_LIGHT, ha='center', fontweight='bold')

        standards = [
            ("AIAG-VDA", "Automotive FMEA", "7-Step Method",
             "Unified approach combining\nAIAG & VDA methodologies.\nAction priority based on AP rating.",
             BLUE, 0.125),
            ("ISO 26262", "Functional Safety", "ASIL Levels A–D",
             "Systematic risk assessment\nfor automotive E/E systems.\nHardware & software metrics.",
             RED, 0.375),
            ("IATF 16949", "Automotive QMS", "Process Approach",
             "Customer-specific requirements,\ncontrol plan linkage, APQP\nintegration & PPAP support.",
             TEAL, 0.625),
            ("IEC 61508", "Industrial Safety", "SIL 1–4 Classification",
             "Safety integrity levels for\nindustrial process control.\nProbabilistic failure analysis.",
             PURPLE, 0.875),
        ]

        for i, (name, scope, key_req, desc, clr, cx) in enumerate(standards):
            delay = 0.8 + i * 1.8
            a = min(1.0, max(0, (t_local - delay) / 1.2))

            # Slide-up offset for animation
            y_offset = max(0, (1.0 - min(1.0, max(0, (t_local - delay) / 0.8)))) * 0.05

            # Card background
            card = FancyBboxPatch((cx - 0.10, 0.20 - y_offset), 0.20, 0.65,
                                   boxstyle="round,pad=0.01",
                                   facecolor=BG_CARD, alpha=a,
                                   edgecolor=clr, linewidth=2.5)
            ax.add_patch(card)

            # Standard name (large)
            ax.text(cx, 0.78 - y_offset, name, fontsize=22, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Color accent line under name
            ax.plot([cx - 0.06, cx + 0.06], [0.73 - y_offset, 0.73 - y_offset],
                    color=clr, lw=3, alpha=a)

            # Scope
            ax.text(cx, 0.67 - y_offset, scope, fontsize=13, color=clr,
                    ha='center', va='center', fontweight='600', alpha=a)

            # Key requirement badge
            req_badge = FancyBboxPatch((cx - 0.08, 0.56 - y_offset), 0.16, 0.05,
                                        boxstyle="round,pad=0.005",
                                        facecolor=clr, alpha=a * 0.25,
                                        edgecolor=clr, linewidth=1)
            ax.add_patch(req_badge)
            ax.text(cx, 0.585 - y_offset, key_req, fontsize=10, color=WHITE,
                    ha='center', va='center', fontweight='600', alpha=a)

            # Description text
            ax.text(cx, 0.42 - y_offset, desc, fontsize=10, color=GRAY,
                    ha='center', va='center', alpha=a, linespacing=1.6)

            # Bottom icon: checkmark circle
            check_a = min(1.0, max(0, (t_local - delay - 1.0) / 0.8))
            check_circle = Circle((cx, 0.26 - y_offset), 0.025, facecolor=clr,
                                   alpha=check_a * 0.3, edgecolor=clr, linewidth=1.5)
            ax.add_patch(check_circle)
            ax.text(cx, 0.26 - y_offset, "✓", fontsize=16, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=check_a)

        # Bottom label
        if t_local > 9:
            label_a = min(1.0, (t_local - 9) / 1.5)
            ax.text(0.5, 0.08, "All standards configurable per project — switch frameworks in one click",
                    fontsize=13, color=GRAY, ha='center', va='center', alpha=label_a)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 4: Multi-Language & Floating Licenses (41–56s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 56:
        t_local = phase - 41
        gs = GridSpec(1, 2, figure=fig, wspace=0.20, left=0.06, right=0.96, top=0.88, bottom=0.08)

        fig.text(0.5, 0.95, "GLOBAL TEAMS — 8 LANGUAGES, FLOATING LICENSES",
                 fontsize=18, color=AMBER_LIGHT, ha='center', fontweight='bold')

        # ── Left panel: Multi-language tabs ──
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
        ax1.set_facecolor(BG_CARD); ax1.axis('off')

        ax1.text(0.5, 0.96, "Multi-Language FMEA Data", fontsize=15, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # Determine which language tab is active based on time
        lang_cycle = (t_local % 9.0)  # Cycle through languages
        if lang_cycle < 3.0:
            active_lang = 0  # English
        elif lang_cycle < 6.0:
            active_lang = 1  # German
        else:
            active_lang = 2  # Japanese

        # Language tabs
        tab_labels = ["English", "Deutsch", "日本語"]
        tab_colors = [BLUE, AMBER, RED]
        for i, (label, tclr) in enumerate(zip(tab_labels, tab_colors)):
            tx = 0.10 + i * 0.30
            tab_a = min(1.0, max(0, (t_local - 0.5) / 1.0))
            is_active = (i == active_lang)

            tab_bg = FancyBboxPatch((tx, 0.82), 0.24, 0.06,
                                     boxstyle="round,pad=0.005",
                                     facecolor=tclr if is_active else BG_DARK,
                                     alpha=tab_a * (0.5 if is_active else 0.2),
                                     edgecolor=tclr, linewidth=1.5 if is_active else 0.8,
                                     transform=ax1.transAxes)
            ax1.add_patch(tab_bg)
            ax1.text(tx + 0.12, 0.85, label, fontsize=11, color=WHITE if is_active else GRAY,
                     ha='center', va='center', fontweight='bold' if is_active else '400',
                     alpha=tab_a, transform=ax1.transAxes)

        # FMEA data content per language
        lang_data = [
            # English
            [
                ("Function", "Transfer torque to driveshaft"),
                ("Failure Mode", "Insufficient clamping force"),
                ("Effect", "Vibration, potential decoupling"),
                ("Cause", "Worn friction surface"),
                ("Severity", "8"),
                ("Occurrence", "4"),
                ("Detection", "6"),
                ("AP", "High"),
            ],
            # German
            [
                ("Funktion", "Drehmoment auf Antriebswelle übertragen"),
                ("Fehlerart", "Unzureichende Klemmkraft"),
                ("Auswirkung", "Vibration, mögliche Entkopplung"),
                ("Ursache", "Verschlissene Reibfläche"),
                ("Bedeutung", "8"),
                ("Auftreten", "4"),
                ("Entdeckung", "6"),
                ("AP", "Hoch"),
            ],
            # Japanese
            [
                ("機能", "ドライブシャフトへトルク伝達"),
                ("故障モード", "クランプ力不足"),
                ("影響", "振動、結合解除の可能性"),
                ("原因", "摩擦面の摩耗"),
                ("重大度", "8"),
                ("発生度", "4"),
                ("検出度", "6"),
                ("AP", "高"),
            ],
        ]

        content_a = min(1.0, max(0, (t_local - 1.0) / 1.0))
        # Fade transition
        transition_progress = lang_cycle % 3.0
        fade_a = 1.0
        if transition_progress < 0.3:
            fade_a = min(1.0, transition_progress / 0.3)
        elif transition_progress > 2.7:
            fade_a = min(1.0, max(0, (3.0 - transition_progress) / 0.3))

        current_data = lang_data[active_lang]
        for i, (label, value) in enumerate(current_data):
            y = 0.72 - i * 0.085
            combined_a = content_a * fade_a

            # Alternate row shading
            if i % 2 == 0:
                row_bg = FancyBboxPatch((0.03, y - 0.025), 0.94, 0.07,
                                         boxstyle="round,pad=0.003",
                                         facecolor=WHITE, alpha=combined_a * 0.06,
                                         edgecolor='none', transform=ax1.transAxes)
                ax1.add_patch(row_bg)

            ax1.text(0.06, y + 0.01, label, fontsize=10, color=AMBER_LIGHT,
                     va='center', fontweight='600', alpha=combined_a, transform=ax1.transAxes)
            display_val = value[:36] if len(value) > 36 else value
            ax1.text(0.06, y - 0.025, display_val, fontsize=10, color=WHITE,
                     va='center', alpha=combined_a, transform=ax1.transAxes)

        # Language count footer
        if t_local > 4:
            foot_a = min(1.0, (t_local - 4) / 1.0)
            ax1.text(0.5, 0.04, "EN · DE · ZH · JA · FR · ES · KO · PT",
                     fontsize=10, color=GRAY, ha='center', va='center',
                     alpha=foot_a, transform=ax1.transAxes)

        # ── Right panel: Floating License Model ──
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_facecolor(BG_CARD); ax2.axis('off')

        ax2.text(0.5, 0.96, "Floating License Model", fontsize=15, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # Central license badge
        lic_a = min(1.0, max(0, (t_local - 1.5) / 1.2))
        lic_box = FancyBboxPatch((0.28, 0.58), 0.44, 0.22,
                                  boxstyle="round,pad=0.012",
                                  facecolor=AMBER, alpha=lic_a * 0.2,
                                  edgecolor=AMBER, linewidth=2.5,
                                  transform=ax2.transAxes)
        ax2.add_patch(lic_box)
        ax2.text(0.50, 0.73, "5 Licenses", fontsize=26, color=AMBER_LIGHT,
                 ha='center', va='center', fontweight='bold', alpha=lic_a,
                 transform=ax2.transAxes)
        ax2.text(0.50, 0.64, "Unlimited Users", fontsize=16, color=WHITE,
                 ha='center', va='center', fontweight='500', alpha=lic_a,
                 transform=ax2.transAxes)

        # User icons around the license box — representing concurrent users
        user_positions = [
            (0.12, 0.82), (0.88, 0.82), (0.12, 0.48),
            (0.88, 0.48), (0.50, 0.90),
            # Extra "waiting" users
            (0.30, 0.42), (0.70, 0.42), (0.12, 0.30),
            (0.88, 0.30), (0.50, 0.28),
        ]

        for i, (ux, uy) in enumerate(user_positions):
            delay = 2.5 + i * 0.4
            ua = min(1.0, max(0, (t_local - delay) / 0.8))
            is_active = i < 5  # First 5 are active (holding license)

            icon_color = GREEN if is_active else GRAY
            icon_border = GREEN if is_active else '#475569'

            # User head
            head = Circle((ux, uy + 0.025), 0.018, facecolor=icon_color,
                           alpha=ua * 0.7, edgecolor=icon_border, linewidth=1,
                           transform=ax2.transAxes)
            ax2.add_patch(head)

            # User body (small arc)
            body = FancyBboxPatch((ux - 0.022, uy - 0.025), 0.044, 0.03,
                                   boxstyle="round,pad=0.005",
                                   facecolor=icon_color, alpha=ua * 0.5,
                                   edgecolor='none', transform=ax2.transAxes)
            ax2.add_patch(body)

            # Status dot
            dot_color = GREEN if is_active else AMBER
            dot_label = "" if not is_active else ""
            status_dot = Circle((ux + 0.025, uy + 0.035), 0.008,
                                 facecolor=dot_color, alpha=ua * 0.9,
                                 transform=ax2.transAxes)
            ax2.add_patch(status_dot)

            # Connection line to center box
            if ua > 0.3:
                line_color = GREEN if is_active else GRAY
                # Calculate line endpoints toward center
                center_x, center_y = 0.50, 0.69
                ax2.plot([ux, center_x], [uy, center_y],
                         color=line_color, lw=0.8, alpha=ua * 0.2,
                         transform=ax2.transAxes, linestyle='--' if not is_active else '-')

        # Legend
        if t_local > 6:
            leg_a = min(1.0, (t_local - 6) / 1.0)
            # Active legend
            leg_dot1 = Circle((0.30, 0.14), 0.008, facecolor=GREEN, alpha=leg_a,
                               transform=ax2.transAxes)
            ax2.add_patch(leg_dot1)
            ax2.text(0.33, 0.14, "Active session", fontsize=10, color=GREEN,
                     va='center', alpha=leg_a, transform=ax2.transAxes)

            # Queued legend
            leg_dot2 = Circle((0.60, 0.14), 0.008, facecolor=AMBER, alpha=leg_a,
                               transform=ax2.transAxes)
            ax2.add_patch(leg_dot2)
            ax2.text(0.63, 0.14, "Queued — next available", fontsize=10, color=AMBER,
                     va='center', alpha=leg_a, transform=ax2.transAxes)

            # Cost note
            ax2.text(0.50, 0.05, "No per-seat pricing — scale your team freely",
                     fontsize=11, color=GRAY, ha='center', va='center',
                     alpha=leg_a, transform=ax2.transAxes)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 5: Closing (56–70s)
    # ═══════════════════════════════════════════════════════════
    else:
        t_local = phase - 56
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        alpha = min(1.0, t_local / 2.0)

        ax.text(0.5, 0.70, "vinFMEA", fontsize=62, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha,
                fontfamily='sans-serif')

        # Amber accent line
        line_w = min(0.35, t_local * 0.08)
        ax.plot([0.325, 0.325 + line_w], [0.62, 0.62], color=AMBER, lw=4, alpha=alpha)

        # Tagline
        ax.text(0.5, 0.53, "Auto-Generated Control Plans. Global Standards. Any Language.",
                fontsize=22, color=AMBER_LIGHT, ha='center', va='center',
                alpha=min(1, max(0, (t_local - 1.5) / 1.5)),
                fontfamily='sans-serif')

        # Feature list
        features = ["PFMEA → Control Plan", "AIAG-VDA & ISO 26262",
                     "IATF 16949 & IEC 61508", "8 Languages",
                     "Floating Licenses", "Cloud & On-Premise"]
        for i, feat in enumerate(features):
            row = i // 3
            col = i % 3
            x = 0.22 + col * 0.28
            y = 0.38 - row * 0.08
            delay = 3.0 + i * 0.3
            a = min(1.0, max(0, (t_local - delay) / 0.8))

            # Small amber bullet
            ax.plot(x - 0.03, y, marker='o', markersize=4, color=AMBER, alpha=a)
            ax.text(x, y, feat, fontsize=13, color=WHITE, ha='center',
                    va='center', alpha=a, fontweight='500')

        # CTA
        if t_local > 7:
            a2 = min(1.0, (t_local - 7) / 1.5)

            # CTA box
            cta_box = FancyBboxPatch((0.25, 0.09), 0.50, 0.07,
                                      boxstyle="round,pad=0.01",
                                      facecolor=AMBER, alpha=a2 * 0.15,
                                      edgecolor=AMBER, linewidth=2)
            ax.add_patch(cta_box)
            ax.text(0.5, 0.125, "Start 14-Day Free Trial  |  vinfmea.com",
                    fontsize=16, color=AMBER_LIGHT, ha='center', va='center',
                    alpha=a2, fontweight='700')


# ── Render ──
BASE = os.path.dirname(__file__)

print("=" * 60)
print("Rendering vinFMEA Control Plans & Standards Video (frames)...")
print("=" * 60)
anim_obj = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000/FPS)
writer = animation.FFMpegWriter(fps=FPS, bitrate=5000, extra_args=['-pix_fmt', 'yuv420p'])
silent_path = os.path.join(BASE, "vf_cp_silent.mp4")
anim_obj.save(silent_path, writer=writer)
plt.close()
print("Video frames done.")

print("Generating voiceover...")
vo_path = os.path.join(BASE, "vf_cp_vo.mp3")
create_voiceover_track(VO_SEGMENTS, DURATION, vo_path)

print("Muxing with sitar background...")
final_path = os.path.join(BASE, "VinFMEA_ControlPlans_Standards.mp4")
mux_video_audio_with_music(silent_path, vo_path, final_path, DURATION)

for f in [silent_path, vo_path]:
    try: os.remove(f)
    except OSError: pass

print(f"\n[OK] vinFMEA Control Plans & Standards complete: {final_path}")
