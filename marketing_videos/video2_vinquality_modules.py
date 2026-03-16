"""
vinQuality Marketing Video 2: Modular Architecture & Pricing
Duration: ~55 seconds | 1080p | 30fps | Professional Voiceover + Sitar
Showcases: Module marketplace, pricing tiers, discount system, SLA & workflows
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
    ("vinQuality. Modular quality management, built your way.", 0.5, 4.5),
    ("Choose exactly the modules you need. From NCMR tracking to CAPA management, "
     "calibration to analytics — each module works independently or together as a unified platform.",
     6.0, 16.0),
    ("The more modules you add, the more you save. Two modules earn ten percent off. "
     "Three modules, fifteen percent. Four or more, twenty percent off every seat.",
     19.0, 29.0),
    ("Built-in SLA tracking ensures nothing falls through the cracks. "
     "Configurable multi-step workflows route approvals exactly where they need to go.",
     31.0, 41.0),
    ("vinQuality. Start with one module. Scale to the full platform. "
     "Visit vinqms.com to begin your free trial.",
     43.0, 53.0),
]

# ── Brand colours ──
BG_DARK    = "#0F172A"
BG_CARD    = "#1E293B"
TEAL       = "#0D9488"
TEAL_LIGHT = "#5EEAD4"
WHITE      = "#FFFFFF"
GRAY       = "#94A3B8"
RED        = "#EF4444"
AMBER      = "#F59E0B"
BLUE       = "#2563EB"
PURPLE     = "#7C3AED"
GREEN      = "#10B981"
CYAN       = "#22D3EE"
PINK       = "#F472B6"
SLATE50    = "#F8FAFC"

FPS = 30
DURATION = 55
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
        alpha_s = min(1.0, max(0, (phase - 1.0) / 1.5))
        alpha_b = min(1.0, max(0, (phase - 2.0) / 1.0))

        # Teal accent line — animated width
        line_w = progress * 0.4
        ax.plot([0.3, 0.3 + line_w], [0.58, 0.58], color=TEAL, lw=4, alpha=alpha_t)

        # Main title
        ax.text(0.5, 0.68, "vinQuality", fontsize=56, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha_t,
                fontfamily='sans-serif')

        # Subtitle
        ax.text(0.5, 0.50, "Modular Quality Management",
                fontsize=26, color=TEAL_LIGHT, ha='center', va='center', alpha=alpha_s,
                fontfamily='sans-serif', fontstyle='italic')

        # Feature badges
        badges = ["Pay Per Module", "Scale As You Grow", "Mix & Match", "No Bloat"]
        for i, badge_text in enumerate(badges):
            x = 0.2 + i * 0.2
            delay = 2.5 + i * 0.35
            a = min(1.0, max(0, (phase - delay) / 0.8))
            rect = FancyBboxPatch((x - 0.08, 0.30), 0.16, 0.06,
                                   boxstyle="round,pad=0.01",
                                   facecolor=TEAL, alpha=a * 0.3, edgecolor=TEAL,
                                   linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, 0.33, badge_text, fontsize=11, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='600')

    # ═══════════════════════════════════════════════════════════
    #  SCENE 2: Module Showcase — 2x3 Grid (5–18s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 18:
        t_local = phase - 5

        ax = fig.add_axes([0.02, 0.05, 0.96, 0.88])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        fig.text(0.5, 0.96, "CHOOSE YOUR MODULES", fontsize=22,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        modules = [
            ("NCMR",        "$55/mo", "Non-conformance tracking\nwith full traceability",       RED),
            ("Deviations",  "$45/mo", "Process deviation control\nand impact assessment",       AMBER),
            ("CAPA",        "$45/mo", "Corrective & preventive\naction management",             BLUE),
            ("SCAR",        "$35/mo", "Supplier corrective action\nrequest workflows",          PURPLE),
            ("Analytics",   "$25/mo", "Real-time dashboards\nand trend reporting",              TEAL),
            ("Calibration", "$55/mo", "Instrument calibration\nschedule and tracking",          GREEN),
        ]

        # 2 rows x 3 columns layout
        for idx, (name, price, desc, clr) in enumerate(modules):
            col = idx % 3
            row = idx // 3
            cx = 0.18 + col * 0.30        # card center x
            cy = 0.68 - row * 0.45        # card center y
            card_w = 0.22
            card_h = 0.34

            # Staggered appearance delay
            delay = 0.5 + idx * 1.0
            a = min(1.0, max(0, (t_local - delay) / 0.8))

            # Slide-up offset for entrance animation
            slide_offset = max(0, (1.0 - min(1.0, max(0, (t_local - delay) / 0.8)))) * 0.05
            cy_anim = cy - slide_offset

            # Card background
            card = FancyBboxPatch((cx - card_w / 2, cy_anim - card_h / 2), card_w, card_h,
                                   boxstyle="round,pad=0.012",
                                   facecolor=BG_CARD, alpha=a,
                                   edgecolor='#334155', linewidth=1.5)
            ax.add_patch(card)

            # Colored top accent bar
            accent = FancyBboxPatch((cx - card_w / 2, cy_anim + card_h / 2 - 0.025), card_w, 0.025,
                                     boxstyle="square",
                                     facecolor=clr, alpha=a * 0.9, edgecolor='none')
            ax.add_patch(accent)

            # Module icon circle
            icon_circle = Circle((cx, cy_anim + card_h / 2 - 0.08), 0.028,
                                  facecolor=clr, alpha=a * 0.25)
            ax.add_patch(icon_circle)
            icon_dot = Circle((cx, cy_anim + card_h / 2 - 0.08), 0.015,
                               facecolor=clr, alpha=a * 0.8)
            ax.add_patch(icon_dot)

            # Module name
            ax.text(cx, cy_anim + card_h / 2 - 0.14, name, fontsize=16, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Price
            ax.text(cx, cy_anim + card_h / 2 - 0.20, price, fontsize=14, color=clr,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Description
            ax.text(cx, cy_anim - card_h / 2 + 0.06, desc, fontsize=9.5, color=GRAY,
                    ha='center', va='center', alpha=a, linespacing=1.5)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 3: Multi-Module Discounts (18–30s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 30:
        t_local = phase - 18

        ax = fig.add_axes([0.02, 0.05, 0.96, 0.88])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        fig.text(0.5, 0.96, "MULTI-MODULE DISCOUNTS", fontsize=22,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        # ── Discount tier cards ──
        tiers = [
            ("2 Modules", "10% OFF", 0.10, BLUE),
            ("3 Modules", "15% OFF", 0.15, TEAL),
            ("4+ Modules", "20% OFF", 0.20, GREEN),
        ]

        for i, (label, pct_text, pct_val, clr) in enumerate(tiers):
            delay = 0.5 + i * 1.2
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            cx = 0.20 + i * 0.30
            cy = 0.72

            # Card
            card = FancyBboxPatch((cx - 0.10, cy - 0.12), 0.20, 0.24,
                                   boxstyle="round,pad=0.012",
                                   facecolor=BG_CARD, alpha=a,
                                   edgecolor=clr, linewidth=2)
            ax.add_patch(card)

            # Tier label
            ax.text(cx, cy + 0.08, label, fontsize=14, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Percentage — large
            ax.text(cx, cy - 0.01, pct_text, fontsize=22, color=clr,
                    ha='center', va='center', fontweight='bold', alpha=a)

            # Progress bar background
            bar_bg = FancyBboxPatch((cx - 0.07, cy - 0.09), 0.14, 0.025,
                                     boxstyle="round,pad=0.003",
                                     facecolor=WHITE, alpha=a * 0.1, edgecolor='none')
            ax.add_patch(bar_bg)

            # Progress bar fill — animated
            fill_progress = min(1.0, max(0, (t_local - delay - 0.3) / 1.0))
            bar_fill = FancyBboxPatch((cx - 0.07, cy - 0.09), 0.14 * fill_progress, 0.025,
                                       boxstyle="round,pad=0.003",
                                       facecolor=clr, alpha=a * 0.7, edgecolor='none')
            ax.add_patch(bar_fill)

        # ── Example calculation ──
        calc_delay = 5.0
        calc_a = min(1.0, max(0, (t_local - calc_delay) / 1.0))

        # Calculation card
        calc_card = FancyBboxPatch((0.10, 0.08), 0.80, 0.35,
                                    boxstyle="round,pad=0.015",
                                    facecolor=BG_CARD, alpha=calc_a,
                                    edgecolor='#334155', linewidth=1.5)
        ax.add_patch(calc_card)

        ax.text(0.50, 0.38, "Example: 3-Module Bundle", fontsize=16, color=WHITE,
                ha='center', va='center', fontweight='bold', alpha=calc_a)

        # Step 1: Module list
        step1_a = min(1.0, max(0, (t_local - 5.5) / 0.8))
        module_items = [
            ("NCMR", "$55", RED, 0.20),
            ("CAPA", "$45", BLUE, 0.42),
            ("Analytics", "$25", TEAL, 0.64),
        ]
        for name, price, clr, mx in module_items:
            mini_card = FancyBboxPatch((mx - 0.04, 0.26), 0.14, 0.07,
                                        boxstyle="round,pad=0.006",
                                        facecolor=clr, alpha=step1_a * 0.15,
                                        edgecolor=clr, linewidth=1)
            ax.add_patch(mini_card)
            ax.text(mx + 0.03, 0.305, name, fontsize=12, color=WHITE,
                    ha='center', va='center', fontweight='600', alpha=step1_a)
            ax.text(mx + 0.03, 0.275, price, fontsize=11, color=clr,
                    ha='center', va='center', fontweight='bold', alpha=step1_a)

        # Plus signs between modules
        for px in [0.33, 0.55]:
            ax.text(px, 0.29, "+", fontsize=18, color=GRAY, ha='center', va='center',
                    fontweight='bold', alpha=step1_a)

        # Step 2: Calculation line
        step2_a = min(1.0, max(0, (t_local - 7.0) / 0.8))

        ax.text(0.20, 0.19, "$55 + $45 + $25 = $125/mo", fontsize=15, color=GRAY,
                va='center', alpha=step2_a, fontfamily='sans-serif')

        # Arrow
        if step2_a > 0.1:
            ax.annotate('', xy=(0.62, 0.19), xytext=(0.56, 0.19),
                        arrowprops=dict(arrowstyle='->', color=TEAL_LIGHT,
                                       lw=2.5, alpha=step2_a))

        # Step 3: Final price with discount
        step3_a = min(1.0, max(0, (t_local - 8.5) / 0.8))

        highlight = FancyBboxPatch((0.62, 0.14), 0.26, 0.10,
                                    boxstyle="round,pad=0.008",
                                    facecolor=TEAL, alpha=step3_a * 0.2,
                                    edgecolor=TEAL, linewidth=2)
        ax.add_patch(highlight)
        ax.text(0.75, 0.21, "$106.25/mo", fontsize=20, color=TEAL_LIGHT,
                ha='center', va='center', fontweight='bold', alpha=step3_a)
        ax.text(0.75, 0.16, "15% off", fontsize=12, color=GREEN,
                ha='center', va='center', fontweight='600', alpha=step3_a)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 4: SLA & Workflow Engine (30–42s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 42:
        t_local = phase - 30
        gs = GridSpec(1, 2, figure=fig, wspace=0.20, left=0.06, right=0.96, top=0.88, bottom=0.08)

        fig.text(0.5, 0.95, "SLA TRACKING & WORKFLOW ENGINE", fontsize=18,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        # ── Left panel: SLA Dashboard ──
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
        ax1.set_facecolor(BG_CARD); ax1.axis('off')

        ax1.text(0.5, 0.95, "SLA Compliance Dashboard", fontsize=15, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # SLA metric rows
        sla_items = [
            ("NCMR Response Time",   "4h",  "8h",  0.50, GREEN,  "On Track"),
            ("NCMR Resolution",      "5d",  "10d", 0.50, GREEN,  "On Track"),
            ("CAPA Initial Review",  "20h", "24h", 0.83, AMBER,  "Warning"),
            ("CAPA Closure",         "32d", "30d", 1.07, RED,    "Breached"),
            ("SCAR Response",        "2d",  "5d",  0.40, GREEN,  "On Track"),
            ("Deviation Resolution", "6d",  "7d",  0.86, AMBER,  "Warning"),
        ]

        for i, (metric, actual, target, ratio, clr, status) in enumerate(sla_items):
            delay = 0.5 + i * 0.7
            a = min(1.0, max(0, (t_local - delay) / 0.7))
            y = 0.82 - i * 0.12

            # Metric label
            ax1.text(0.04, y + 0.025, metric, fontsize=9.5, color=WHITE,
                     va='center', fontweight='500', alpha=a, transform=ax1.transAxes)

            # Actual / Target
            ax1.text(0.04, y - 0.015, f"{actual} / {target}", fontsize=8, color=GRAY,
                     va='center', alpha=a, transform=ax1.transAxes)

            # Progress bar background
            bar_bg = FancyBboxPatch((0.48, y - 0.01), 0.35, 0.03,
                                     boxstyle="round,pad=0.003",
                                     facecolor=WHITE, alpha=a * 0.08, edgecolor='none',
                                     transform=ax1.transAxes)
            ax1.add_patch(bar_bg)

            # Progress bar fill
            fill_w = min(0.35, 0.35 * min(ratio, 1.0))
            anim_progress = min(1.0, max(0, (t_local - delay - 0.2) / 0.8))
            bar_fill = FancyBboxPatch((0.48, y - 0.01), fill_w * anim_progress, 0.03,
                                       boxstyle="round,pad=0.003",
                                       facecolor=clr, alpha=a * 0.7, edgecolor='none',
                                       transform=ax1.transAxes)
            ax1.add_patch(bar_fill)

            # Status badge
            badge = FancyBboxPatch((0.85, y - 0.015), 0.13, 0.04,
                                    boxstyle="round,pad=0.004",
                                    facecolor=clr, alpha=a * 0.2,
                                    edgecolor=clr, linewidth=1,
                                    transform=ax1.transAxes)
            ax1.add_patch(badge)
            ax1.text(0.915, y + 0.005, status, fontsize=7.5, color=clr,
                     ha='center', va='center', fontweight='600', alpha=a,
                     transform=ax1.transAxes)

        # Breached item: extra indicator for CAPA Closure
        if t_local > 3.5:
            breach_a = min(1.0, (t_local - 3.5) / 0.8)
            # Overshoot bar (past 100%) shown in red
            overshoot_x = 0.48 + 0.35
            overshoot_w = min(0.02, 0.35 * 0.07)
            bar_over = FancyBboxPatch((overshoot_x, 0.82 - 3 * 0.12 - 0.01), overshoot_w, 0.03,
                                       boxstyle="square",
                                       facecolor=RED, alpha=breach_a * 0.9, edgecolor='none',
                                       transform=ax1.transAxes)
            ax1.add_patch(bar_over)

        # ── Right panel: Workflow Configuration ──
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_facecolor(BG_CARD); ax2.axis('off')

        ax2.text(0.5, 0.95, "Multi-Step Approval Workflow", fontsize=15, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # Workflow nodes (vertical chain)
        wf_nodes = [
            ("Submit",       "Creator submits\nrecord for review",    GRAY,   0.84),
            ("QA Review",    "Quality analyst\nreviews findings",     BLUE,   0.68),
            ("Supervisor",   "Supervisor approves\nor sends back",    AMBER,  0.52),
            ("QA Manager",   "Manager e-signs\nfinal disposition",    TEAL,   0.36),
            ("Closed",       "Record archived\nwith full audit trail", GREEN, 0.20),
        ]

        for i, (node_name, node_desc, clr, ny) in enumerate(wf_nodes):
            delay = 1.0 + i * 1.2
            a = min(1.0, max(0, (t_local - delay) / 0.8))

            # Node circle
            node_circle = Circle((0.15, ny), 0.035, facecolor=clr, alpha=a * 0.8,
                                  transform=ax2.transAxes)
            ax2.add_patch(node_circle)
            ax2.text(0.15, ny, str(i + 1), fontsize=12, color=WHITE,
                     ha='center', va='center', fontweight='bold', alpha=a,
                     transform=ax2.transAxes)

            # Node label
            ax2.text(0.28, ny + 0.02, node_name, fontsize=12, color=WHITE,
                     va='center', fontweight='bold', alpha=a, transform=ax2.transAxes)

            # Node description
            ax2.text(0.28, ny - 0.035, node_desc, fontsize=8.5, color=GRAY,
                     va='center', alpha=a, linespacing=1.4, transform=ax2.transAxes)

            # Connector line to next node
            if i < len(wf_nodes) - 1:
                next_ny = wf_nodes[i + 1][3]
                arrow_delay = delay + 0.6
                arrow_a = min(1.0, max(0, (t_local - arrow_delay) / 0.5))
                ax2.plot([0.15, 0.15], [ny - 0.04, next_ny + 0.04],
                         color=TEAL_LIGHT, lw=2, alpha=arrow_a * 0.6,
                         transform=ax2.transAxes, linestyle='--')
                # Arrowhead
                ax2.annotate('', xy=(0.15, next_ny + 0.04), xytext=(0.15, next_ny + 0.07),
                             arrowprops=dict(arrowstyle='->', color=TEAL_LIGHT,
                                            lw=2, alpha=arrow_a * 0.6),
                             xycoords=ax2.transAxes, textcoords=ax2.transAxes)

            # Side annotation: e-signature badge for QA Manager
            if node_name == "QA Manager" and a > 0.5:
                esig_badge = FancyBboxPatch((0.68, ny - 0.03), 0.28, 0.06,
                                             boxstyle="round,pad=0.006",
                                             facecolor=TEAL, alpha=a * 0.15,
                                             edgecolor=TEAL, linewidth=1,
                                             transform=ax2.transAxes)
                ax2.add_patch(esig_badge)
                ax2.text(0.82, ny, "E-Signature Required", fontsize=8.5, color=TEAL_LIGHT,
                         ha='center', va='center', fontweight='600', alpha=a,
                         transform=ax2.transAxes)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 5: Closing Card (42–55s)
    # ═══════════════════════════════════════════════════════════
    else:
        t_local = phase - 42
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        alpha = min(1.0, t_local / 2.0)

        # Main title
        ax.text(0.5, 0.72, "vinQuality", fontsize=60, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha,
                fontfamily='sans-serif')

        # Teal accent line — animated
        line_w = min(0.35, t_local * 0.08)
        ax.plot([0.325, 0.325 + line_w], [0.64, 0.64], color=TEAL, lw=4, alpha=alpha)

        # Subtitle
        sub_a = min(1.0, max(0, (t_local - 1.5) / 1.5))
        ax.text(0.5, 0.55, "Start with one module. Scale to the full platform.",
                fontsize=22, color=TEAL_LIGHT, ha='center', va='center',
                alpha=sub_a, fontstyle='italic')

        # Module name list — two rows of three
        module_names = ["NCMR", "Deviations", "CAPA", "SCAR", "Calibration", "Analytics"]
        module_colors = [RED, AMBER, BLUE, PURPLE, GREEN, TEAL]
        for i, (mod, clr) in enumerate(zip(module_names, module_colors)):
            row = i // 3
            col = i % 3
            x = 0.25 + col * 0.25
            y = 0.42 - row * 0.09
            delay = 3.0 + i * 0.3
            a = min(1.0, max(0, (t_local - delay) / 0.8))

            # Small colored dot before name
            dot = Circle((x - 0.03, y), 0.008, facecolor=clr, alpha=a,
                          transform=ax.transAxes)
            ax.add_patch(dot)

            ax.text(x, y, mod, fontsize=14, color=WHITE, ha='center',
                    va='center', alpha=a, fontweight='500',
                    transform=ax.transAxes)

        # CTA at bottom
        if t_local > 6:
            cta_a = min(1.0, (t_local - 6) / 1.5)

            # CTA background pill
            cta_bg = FancyBboxPatch((0.25, 0.09), 0.50, 0.07,
                                     boxstyle="round,pad=0.012",
                                     facecolor=TEAL, alpha=cta_a * 0.15,
                                     edgecolor=TEAL, linewidth=2)
            ax.add_patch(cta_bg)

            ax.text(0.5, 0.125, "Start Your Free Trial  |  vinqms.com",
                    fontsize=16, color=TEAL_LIGHT, ha='center', va='center',
                    alpha=cta_a, fontweight='600')


# ── Render ──
BASE = os.path.dirname(__file__)

print("=" * 60)
print("Rendering vinQuality Modules Video (frames)...")
print("=" * 60)
anim_obj = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000/FPS)
writer = animation.FFMpegWriter(fps=FPS, bitrate=5000, extra_args=['-pix_fmt', 'yuv420p'])
silent_path = os.path.join(BASE, "vq_modules_silent.mp4")
anim_obj.save(silent_path, writer=writer)
plt.close()
print("Video frames done.")

print("Generating voiceover...")
vo_path = os.path.join(BASE, "vq_modules_vo.mp3")
create_voiceover_track(VO_SEGMENTS, DURATION, vo_path)

print("Muxing with sitar background...")
final_path = os.path.join(BASE, "VinQuality_Modular_QMS.mp4")
mux_video_audio_with_music(silent_path, vo_path, final_path, DURATION)

for f in [silent_path, vo_path]:
    try: os.remove(f)
    except OSError: pass

print(f"\n[OK] vinQuality Modules video complete: {final_path}")
