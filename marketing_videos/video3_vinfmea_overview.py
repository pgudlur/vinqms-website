"""
vinFMEA Marketing Video 3: Professional FMEA & Control Plan Suite Overview
Duration: ~60 seconds | 1080p | 30fps | Professional Voiceover + Sitar
Showcases: PFMEA worksheet, 4-level traceability, risk matrix, action priority
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
    ("vinFMEA. Professional failure mode and effects analysis.", 0.5, 4.5),
    ("The PFMEA worksheet follows the AIAG-VDA seven-step methodology. "
     "Rate severity, occurrence, and detection to calculate action priority. "
     "Track every action item from assignment through completion.",
     6.0, 20.0),
    ("Four levels of traceability connect system-level risks all the way through to control plans. "
     "When a design FMEA changes, process FMEAs and control plans update automatically.",
     22.0, 34.0),
    ("The interactive risk matrix visualizes your risk landscape at a glance. "
     "Identify high-priority failure modes and drive them down with targeted actions.",
     36.0, 47.0),
    ("vinFMEA. From system FMEA to control plans, complete traceability. "
     "Start your fourteen-day free trial at vinfmea.com.",
     50.0, 61.0),
]

# ── Brand colours ──
BG_DARK    = "#0F172A"
BG_CARD    = "#1E293B"
NAVY       = "#1E3A5F"
AMBER      = "#F59E0B"
WHITE      = "#FFFFFF"
GRAY       = "#94A3B8"
RED        = "#EF4444"
GREEN      = "#10B981"
BLUE       = "#2563EB"
TEAL       = "#0D9488"
CYAN       = "#22D3EE"
PURPLE     = "#7C3AED"

FPS = 30
DURATION = 65
TOTAL_FRAMES = FPS * DURATION

np.random.seed(42)

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
        alpha_s = min(1.0, max(0, (phase - 1.0) / 1.5))
        alpha_b = min(1.0, max(0, (phase - 2.5) / 1.0))

        # Amber accent line
        line_w = progress * 0.4
        ax.plot([0.3, 0.3 + line_w], [0.58, 0.58], color=AMBER, lw=4, alpha=alpha_t)

        ax.text(0.5, 0.68, "vinFMEA", fontsize=56, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha_t,
                fontfamily='sans-serif')
        ax.text(0.5, 0.50, "Professional FMEA & Control Plan Suite",
                fontsize=24, color=AMBER, ha='center', va='center', alpha=alpha_s,
                fontfamily='sans-serif', fontstyle='italic')

        badges = ["AIAG-VDA", "ISO 26262", "4-Level Traceability", "8 Languages"]
        for i, feat in enumerate(badges):
            x = 0.2 + i * 0.2
            delay = 2.5 + i * 0.35
            a = min(1.0, max(0, (phase - delay) / 0.8))
            rect = FancyBboxPatch((x - 0.08, 0.30), 0.16, 0.06,
                                   boxstyle="round,pad=0.01",
                                   facecolor=AMBER, alpha=a * 0.3, edgecolor=AMBER,
                                   linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, 0.33, feat, fontsize=11, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='600')

    # ═══════════════════════════════════════════════════════════
    #  SCENE 2: PFMEA Spreadsheet View (5–21s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 21:
        t_local = phase - 5

        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1920); ax.set_ylim(0, 1080)
        ax.set_facecolor(BG_DARK); ax.axis('off')
        ax.invert_yaxis()

        # ── Dark toolbar at top ──
        toolbar = FancyBboxPatch((0, 0), 1920, 60, boxstyle="square",
                                  facecolor=BG_CARD, edgecolor='#334155', linewidth=1)
        ax.add_patch(toolbar)

        tabs = [
            ("SFMEA", False), ("DFMEA", False), ("PFMEA", True), ("Control Plan", False)
        ]
        for i, (tab_name, active) in enumerate(tabs):
            tx = 80 + i * 160
            if active:
                tab_bg = FancyBboxPatch((tx - 50, 10), 120, 40, boxstyle="round,pad=3",
                                         facecolor=AMBER, alpha=0.25, edgecolor=AMBER,
                                         linewidth=1.5)
                ax.add_patch(tab_bg)
                ax.text(tx + 10, 32, tab_name, fontsize=14, color=AMBER,
                        ha='center', va='center', fontweight='bold')
            else:
                ax.text(tx + 10, 32, tab_name, fontsize=13, color=GRAY,
                        ha='center', va='center', fontweight='400')

        ax.text(1650, 32, "AIAG-VDA PFMEA", fontsize=12, color=GRAY,
                ha='center', va='center', fontweight='500')

        # ── Column headers ──
        header_bg = FancyBboxPatch((0, 68), 1920, 44, boxstyle="square",
                                    facecolor=NAVY, edgecolor='#334155', linewidth=1)
        ax.add_patch(header_bg)

        columns = [
            ("Step ID", 60), ("Process Step", 220), ("Failure Mode", 520),
            ("S", 800), ("O", 870), ("D", 940), ("AP", 1020), ("Status", 1160),
        ]
        for col_name, cx in columns:
            ax.text(cx, 90, col_name, fontsize=12, color=WHITE,
                    ha='left' if cx < 780 else 'center', va='center', fontweight='bold')

        # ── PFMEA rows ──
        pfmea_rows = [
            ("3.1", "CNC Machining — Bore", "Bore undersize (< tolerance)",
             "8", "4", "3", "H", "Open"),
            ("3.2", "CNC Machining — OD", "OD out-of-round",
             "7", "3", "4", "M", "In Progress"),
            ("4.1", "Surface Coating", "Adhesion failure (peel)",
             "9", "3", "2", "H", "Open"),
            ("4.2", "Surface Coating", "Coating thickness variation",
             "6", "4", "5", "M", "In Progress"),
            ("5.1", "Assembly — Torque", "Torque below spec",
             "9", "2", "3", "M", "Completed"),
            ("5.2", "Assembly — Press Fit", "Interference fit too loose",
             "8", "3", "2", "H", "Open"),
            ("6.1", "Final Inspection", "Missed defect (false accept)",
             "10", "2", "4", "H", "In Progress"),
        ]

        ap_colors = {"H": RED, "M": AMBER, "L": GREEN}
        status_colors_map = {
            "Open": (AMBER, "#3D2800"),
            "In Progress": (BLUE, "#1E3A5F"),
            "Completed": (GREEN, "#064E3B"),
        }

        for i, (step_id, proc_step, fail_mode, s, o, d, ap, status) in enumerate(pfmea_rows):
            delay = 1.0 + i * 0.7
            a = min(1.0, max(0, (t_local - delay) / 0.6))
            y = 130 + i * 56

            # Row stripe
            if i % 2 == 0:
                stripe = FancyBboxPatch((0, y - 8), 1920, 50, boxstyle="square",
                                         facecolor=BG_CARD, edgecolor='none', alpha=a * 0.5)
                ax.add_patch(stripe)
            else:
                stripe = FancyBboxPatch((0, y - 8), 1920, 50, boxstyle="square",
                                         facecolor=BG_DARK, edgecolor='none', alpha=a * 0.3)
                ax.add_patch(stripe)

            # Row separator
            ax.plot([0, 1920], [y + 42, y + 42], color='#334155', lw=0.5, alpha=a * 0.5)

            ax.text(60, y + 18, step_id, fontsize=12, color=CYAN, alpha=a,
                    fontweight='600')
            ax.text(220, y + 18, proc_step, fontsize=12, color=WHITE, alpha=a)
            ax.text(520, y + 18, fail_mode[:32], fontsize=11, color=GRAY, alpha=a)

            # S, O, D numeric cells
            ax.text(810, y + 18, s, fontsize=13, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='bold')
            ax.text(880, y + 18, o, fontsize=13, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='bold')
            ax.text(950, y + 18, d, fontsize=13, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='bold')

            # AP badge
            ap_clr = ap_colors.get(ap, GRAY)
            ap_bg = FancyBboxPatch((1000, y + 2), 40, 28, boxstyle="round,pad=3",
                                    facecolor=ap_clr, alpha=a * 0.25, edgecolor=ap_clr,
                                    linewidth=1.5)
            ax.add_patch(ap_bg)
            ax.text(1020, y + 18, ap, fontsize=13, color=ap_clr, ha='center', va='center',
                    alpha=a, fontweight='bold')

            # Status badge
            s_clr, s_bg = status_colors_map.get(status, (GRAY, BG_CARD))
            status_badge = FancyBboxPatch((1100, y + 2), 120, 28, boxstyle="round,pad=3",
                                           facecolor=s_bg, alpha=a * 0.4, edgecolor=s_clr,
                                           linewidth=1)
            ax.add_patch(status_badge)
            ax.text(1160, y + 18, status, fontsize=10, color=s_clr, ha='center', va='center',
                    alpha=a, fontweight='600')

        # ── Summary bar at bottom ──
        if t_local > 6:
            sum_a = min(1.0, (t_local - 6) / 1.5)
            summary_bg = FancyBboxPatch((0, 530), 1920, 50, boxstyle="square",
                                         facecolor=NAVY, alpha=sum_a * 0.6, edgecolor='#334155')
            ax.add_patch(summary_bg)
            ax.text(100, 558, "Total Failure Modes: 7", fontsize=13, color=WHITE,
                    va='center', alpha=sum_a, fontweight='600')
            ax.text(420, 558, "High: 4", fontsize=13, color=RED,
                    va='center', alpha=sum_a, fontweight='bold')
            ax.text(560, 558, "Medium: 2", fontsize=13, color=AMBER,
                    va='center', alpha=sum_a, fontweight='bold')
            ax.text(720, 558, "Low: 1", fontsize=13, color=GREEN,
                    va='center', alpha=sum_a, fontweight='bold')

    # ═══════════════════════════════════════════════════════════
    #  SCENE 3: 4-Level Traceability (21–35s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 35:
        t_local = phase - 21

        ax = fig.add_axes([0.02, 0.05, 0.96, 0.85])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        fig.text(0.5, 0.96, "4-LEVEL FMEA TRACEABILITY", fontsize=20,
                 color=AMBER, ha='center', fontweight='bold')

        levels = [
            ("System FMEA", "Top-level system\nfunctions & interfaces",
             "Braking system\nfailure modes", PURPLE, 0.08),
            ("Design FMEA", "Component design\nintent & requirements",
             "Caliper seal\nmaterial fatigue", BLUE, 0.31),
            ("Process FMEA", "Manufacturing process\nsteps & controls",
             "CNC bore undersize\ndue to tool wear", AMBER, 0.54),
            ("Control Plan", "Inspection methods\n& reaction plans",
             "SPC chart on bore\ndia. every 25 pcs", GREEN, 0.77),
        ]

        for i, (title, desc, example, clr, x) in enumerate(levels):
            delay = 0.5 + i * 1.5
            a = min(1.0, max(0, (t_local - delay) / 1.0))

            # Card
            card = FancyBboxPatch((x, 0.38), 0.18, 0.48,
                                   boxstyle="round,pad=0.01",
                                   facecolor=BG_CARD, alpha=a,
                                   edgecolor=clr, linewidth=2.5)
            ax.add_patch(card)

            # Level number circle
            circle = Circle((x + 0.09, 0.80), 0.028, facecolor=clr, alpha=a * 0.9)
            ax.add_patch(circle)
            ax.text(x + 0.09, 0.80, str(i + 1), fontsize=14, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Title
            ax.text(x + 0.09, 0.72, title, fontsize=13, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Description
            ax.text(x + 0.09, 0.62, desc, fontsize=9, color=GRAY,
                    ha='center', va='center', alpha=a, linespacing=1.5)

            # Example label
            ax.text(x + 0.09, 0.52, "Example:", fontsize=8, color=clr,
                    ha='center', va='center', fontweight='600', alpha=a)
            ax.text(x + 0.09, 0.44, example, fontsize=8, color=WHITE,
                    ha='center', va='center', alpha=a * 0.8, linespacing=1.4)

            # Arrow to next level
            if i < len(levels) - 1:
                arrow_delay = delay + 1.0
                arrow_a = min(1.0, max(0, (t_local - arrow_delay) / 0.5))
                ax.annotate('', xy=(x + 0.22, 0.62), xytext=(x + 0.185, 0.62),
                           arrowprops=dict(arrowstyle='->', color=AMBER,
                                          lw=2.5, alpha=arrow_a))

        # ── "Changes cascade automatically" animated highlight ──
        if t_local > 8:
            cascade_a = min(1.0, (t_local - 8) / 1.5)

            # Animated pulse that flows across the chain
            pulse_phase = (t_local - 8) % 4.0  # repeats every 4 seconds
            pulse_x = 0.08 + (pulse_phase / 4.0) * 0.87
            pulse_w = 0.18

            # Glowing bar flowing left to right
            for offset in np.linspace(-0.02, 0.02, 5):
                glow_a = cascade_a * 0.15 * (1.0 - abs(offset) / 0.02)
                ax.plot([pulse_x - pulse_w / 2, pulse_x + pulse_w / 2],
                        [0.34 + offset, 0.34 + offset],
                        color=AMBER, lw=6, alpha=glow_a)

            ax.text(0.5, 0.22, "Changes cascade automatically across all levels",
                    fontsize=16, color=AMBER, ha='center', va='center',
                    fontweight='bold', alpha=cascade_a)

            # Bottom connector line
            ax.plot([0.17, 0.86], [0.28, 0.28], color=AMBER, lw=2,
                    alpha=cascade_a * 0.4, linestyle='--')
            for lx in [0.17, 0.40, 0.63, 0.86]:
                dot = Circle((lx, 0.28), 0.008, facecolor=AMBER, alpha=cascade_a * 0.6)
                ax.add_patch(dot)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 4: Risk Matrix Heatmap (35–49s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 49:
        t_local = phase - 35
        gs = GridSpec(1, 2, figure=fig, wspace=0.15, left=0.06, right=0.96,
                      top=0.88, bottom=0.08, width_ratios=[1.2, 0.8])

        fig.text(0.5, 0.95, "RISK MATRIX & ACTION PRIORITY", fontsize=20,
                 color=AMBER, ha='center', fontweight='bold')

        # ── Left panel: 5x5 Risk Matrix ──
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlim(-0.5, 5.5); ax1.set_ylim(-0.5, 5.5)
        ax1.set_facecolor(BG_CARD); ax1.axis('off')

        ax1.text(2.5, 5.35, "Severity vs. Occurrence Risk Matrix", fontsize=14,
                 color=WHITE, ha='center', va='center', fontweight='bold')

        # Risk level colors: row=severity (bottom=1, top=5), col=occurrence (left=1, right=5)
        # Higher severity + higher occurrence = higher risk
        risk_grid = [
            # Occ=1   Occ=2   Occ=3   Occ=4   Occ=5     (Severity row)
            [GREEN,   GREEN,   GREEN,   AMBER,   AMBER],   # Sev=1 (bottom)
            [GREEN,   GREEN,   AMBER,   AMBER,   AMBER],   # Sev=2
            [GREEN,   AMBER,   AMBER,   RED,     RED],      # Sev=3
            [AMBER,   AMBER,   RED,     RED,     RED],      # Sev=4
            [AMBER,   RED,     RED,     RED,     RED],      # Sev=5 (top)
        ]

        # Draw grid cells
        for row in range(5):
            for col in range(5):
                delay = 0.5 + (row + col) * 0.15
                a = min(1.0, max(0, (t_local - delay) / 0.8))
                clr = risk_grid[row][col]
                cell = FancyBboxPatch((col + 0.05, row + 0.05), 0.9, 0.9,
                                       boxstyle="round,pad=0.02",
                                       facecolor=clr, alpha=a * 0.35,
                                       edgecolor=clr, linewidth=1)
                ax1.add_patch(cell)

        # Axis labels
        occ_labels = ["1\nRemote", "2\nLow", "3\nModerate", "4\nHigh", "5\nVery High"]
        sev_labels = ["1\nMinor", "2\nLow", "3\nModerate", "4\nHigh", "5\nCritical"]

        for i, label in enumerate(occ_labels):
            ax1.text(i + 0.5, -0.35, label, fontsize=8, color=GRAY,
                     ha='center', va='center')
        for i, label in enumerate(sev_labels):
            ax1.text(-0.4, i + 0.5, label, fontsize=8, color=GRAY,
                     ha='center', va='center')

        ax1.text(2.5, -0.8, "Occurrence", fontsize=11, color=WHITE,
                 ha='center', fontweight='600')
        ax1.text(-0.9, 2.5, "Severity", fontsize=11, color=WHITE,
                 ha='center', va='center', fontweight='600', rotation=90)

        # Data points appearing on the matrix with pulse effect
        data_points = [
            (3, 4, "3.1"),   # Bore undersize: S=8→row4, O=4→col3
            (2, 3, "3.2"),   # OD out-of-round: S=7→row3, O=3→col2
            (2, 4, "4.1"),   # Adhesion failure: S=9→row4, O=3→col2
            (3, 2, "4.2"),   # Coating thickness: S=6→row2, O=4→col3
            (1, 4, "5.1"),   # Torque below spec: S=9→row4, O=2→col1
            (2, 3, "5.2"),   # Press fit loose: S=8→row3, O=3→col2
            (1, 4, "6.1"),   # Missed defect: S=10→row4, O=2→col1
        ]

        for i, (col, row, label) in enumerate(data_points):
            delay = 3.0 + i * 0.6
            a = min(1.0, max(0, (t_local - delay) / 0.5))

            # Pulse ring effect
            pulse_t = max(0, t_local - delay - 0.5)
            pulse_r = 0.08 + pulse_t * 0.04 if pulse_t < 1.5 else 0.08
            pulse_a = a * max(0, 0.4 - pulse_t * 0.15) if pulse_t > 0 else 0

            if pulse_a > 0:
                ring = Circle((col + 0.5, row + 0.5), pulse_r,
                               facecolor='none', edgecolor=WHITE,
                               linewidth=2, alpha=pulse_a)
                ax1.add_patch(ring)

            # Data point dot
            dot = Circle((col + 0.5, row + 0.5), 0.12,
                          facecolor=WHITE, alpha=a * 0.9, edgecolor=BG_DARK,
                          linewidth=1.5)
            ax1.add_patch(dot)
            ax1.text(col + 0.5, row + 0.5, label, fontsize=7, color=BG_DARK,
                     ha='center', va='center', fontweight='bold', alpha=a)

        # ── Right panel: Action Priority bar chart ──
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_facecolor(BG_CARD); ax2.axis('off')

        ax2.text(0.5, 0.95, "Action Priority\nDistribution", fontsize=14, color=WHITE,
                 ha='center', va='top', fontweight='bold', linespacing=1.4)

        ap_data = [
            ("HIGH", 4, RED),
            ("MEDIUM", 2, AMBER),
            ("LOW", 1, GREEN),
        ]
        max_count = 4

        for i, (ap_label, count, clr) in enumerate(ap_data):
            delay = 5.0 + i * 0.8
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            y = 0.72 - i * 0.18

            # Label
            ax2.text(0.05, y + 0.02, ap_label, fontsize=13, color=clr,
                     va='center', fontweight='bold', alpha=a, transform=ax2.transAxes)

            # Bar
            bar_w = (count / max_count) * 0.50
            bar = FancyBboxPatch((0.30, y - 0.02), bar_w * a, 0.07,
                                  boxstyle="round,pad=0.005",
                                  facecolor=clr, alpha=a * 0.6, edgecolor='none',
                                  transform=ax2.transAxes)
            ax2.add_patch(bar)

            # Count
            ax2.text(0.30 + bar_w * a + 0.04, y + 0.02, str(count), fontsize=16,
                     color=clr, va='center', fontweight='bold', alpha=a,
                     transform=ax2.transAxes)

        # Total failure modes summary
        if t_local > 8:
            tot_a = min(1.0, (t_local - 8) / 1.5)

            summary_card = FancyBboxPatch((0.08, 0.08), 0.84, 0.18,
                                           boxstyle="round,pad=0.01",
                                           facecolor=BG_DARK, alpha=tot_a,
                                           edgecolor=AMBER, linewidth=2,
                                           transform=ax2.transAxes)
            ax2.add_patch(summary_card)
            ax2.text(0.5, 0.20, "7", fontsize=28, color=AMBER,
                     ha='center', va='center', fontweight='bold', alpha=tot_a,
                     transform=ax2.transAxes)
            ax2.text(0.5, 0.12, "Total Failure Modes", fontsize=10, color=GRAY,
                     ha='center', va='center', alpha=tot_a, transform=ax2.transAxes)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 5: Closing (49–65s)
    # ═══════════════════════════════════════════════════════════
    else:
        t_local = phase - 49
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        alpha = min(1.0, t_local / 2.0)

        ax.text(0.5, 0.72, "vinFMEA", fontsize=60, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha,
                fontfamily='sans-serif')

        # Amber accent line
        line_w = min(0.35, t_local * 0.08)
        ax.plot([0.325, 0.325 + line_w], [0.64, 0.64], color=AMBER, lw=4, alpha=alpha)

        ax.text(0.5, 0.54, "From System FMEA to Control Plans — Complete Traceability",
                fontsize=20, color=AMBER, ha='center', va='center',
                alpha=min(1, max(0, (t_local - 1.5) / 1.5)),
                fontstyle='italic')

        # Feature list
        modules = ["SFMEA", "DFMEA", "PFMEA", "Control Plans", "Risk Matrix", "Report Builder"]
        for i, mod in enumerate(modules):
            row = i // 3
            col = i % 3
            x = 0.22 + col * 0.28
            y = 0.39 - row * 0.10
            delay = 3.0 + i * 0.3
            a = min(1.0, max(0, (t_local - delay) / 0.8))

            # Small bullet dot
            dot = Circle((x - 0.04, y), 0.005, facecolor=AMBER, alpha=a)
            ax.add_patch(dot)
            ax.text(x, y, mod, fontsize=14, color=WHITE, ha='center',
                    va='center', alpha=a, fontweight='500')

        # CTA
        if t_local > 7:
            a2 = min(1.0, (t_local - 7) / 1.5)

            cta_bg = FancyBboxPatch((0.25, 0.08), 0.50, 0.07,
                                     boxstyle="round,pad=0.008",
                                     facecolor=AMBER, alpha=a2 * 0.15,
                                     edgecolor=AMBER, linewidth=1.5)
            ax.add_patch(cta_bg)
            ax.text(0.5, 0.115, "Start 14-Day Free Trial  |  vinfmea.com",
                    fontsize=16, color=AMBER, ha='center', va='center',
                    alpha=a2, fontweight='600')


# ── Render ──
BASE = os.path.dirname(__file__)

print("=" * 60)
print("Rendering vinFMEA Platform Overview Video (frames)...")
print("=" * 60)
anim_obj = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000/FPS)
writer = animation.FFMpegWriter(fps=FPS, bitrate=5000, extra_args=['-pix_fmt', 'yuv420p'])
silent_path = os.path.join(BASE, "vf_overview_silent.mp4")
anim_obj.save(silent_path, writer=writer)
plt.close()
print("Video frames done.")

print("Generating voiceover...")
vo_path = os.path.join(BASE, "vf_overview_vo.mp3")
create_voiceover_track(VO_SEGMENTS, DURATION, vo_path)

print("Muxing with sitar background...")
final_path = os.path.join(BASE, "VinFMEA_Platform_Overview.mp4")
mux_video_audio_with_music(silent_path, vo_path, final_path, DURATION)

for f in [silent_path, vo_path]:
    try: os.remove(f)
    except OSError: pass

print(f"\n[OK] vinFMEA Platform Overview complete: {final_path}")
