"""
vinQuality Marketing Video 1: Complete Platform Overview
Duration: ~65 seconds | 1080p | 30fps | Professional Voiceover + Sitar
Showcases: Dashboard, NCMR workflow, CAPA management, Audit trail, SLA tracking
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
    ("vinQuality. Enterprise Quality Management, Zero Overhead.",
     0.5, 5.0),

    ("Your quality dashboard shows everything at a glance. "
     "Open NCMRs, active CAPAs, SLA compliance, and pending approvals — all in real time.",
     6.5, 16.0),

    ("Create and track non-conformance reports with full traceability. "
     "Every NCMR follows a configurable workflow from creation through disposition and closure.",
     18.0, 28.0),

    ("The CAPA module links root cause analysis to corrective actions. "
     "Track effectiveness verification and drive continuous improvement across your organization.",
     30.0, 40.0),

    ("A SHA-256 cryptographic hash chain ensures every change is tamper-evident. "
     "21 CFR Part 11 compliant e-signatures with full audit trail for regulatory readiness.",
     42.0, 53.0),

    ("vinQuality. Modular quality management built for manufacturers. "
     "Start your free trial at vinqms.com.",
     56.0, 64.0),
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
DURATION = 66
TOTAL_FRAMES = FPS * DURATION

# ── Data ──
np.random.seed(42)
months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
ncmr_counts = [18, 22, 25, 20, 28, 24]
capa_counts = [8, 10, 12, 9, 14, 12]
sla_pct = [91, 88, 93, 90, 95, 94]

# Status distribution
status_labels = ['Open', 'In Review', 'Pending CAPA', 'Dispositioned', 'Closed']
status_counts = [8, 5, 7, 4, 24]
status_colors = [AMBER, '#FBBF24', BLUE, GREEN, TEAL]

fig = plt.figure(figsize=(19.2, 10.8), facecolor=BG_DARK)


def draw_frame(frame):
    fig.clear()
    fig.set_facecolor(BG_DARK)
    phase = frame / FPS

    # ═══════════════════════════════════════════════════════════
    #  SCENE 1: Title Card (0–6s)
    # ═══════════════════════════════════════════════════════════
    if phase < 6:
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        progress = min(1.0, phase / 2.0)
        alpha_t = min(1.0, phase / 1.5)
        alpha_s = min(1.0, max(0, (phase - 1.0) / 1.5))
        alpha_b = min(1.0, max(0, (phase - 2.5) / 1.0))

        # Teal accent line
        line_w = progress * 0.4
        ax.plot([0.3, 0.3 + line_w], [0.58, 0.58], color=TEAL, lw=4, alpha=alpha_t)

        ax.text(0.5, 0.66, "vinQuality", fontsize=56, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha_t,
                fontfamily='sans-serif')
        ax.text(0.5, 0.50, "Enterprise Quality Management System",
                fontsize=24, color=TEAL_LIGHT, ha='center', va='center', alpha=alpha_s,
                fontfamily='sans-serif', fontstyle='italic')

        features = ["NCMR Tracking", "CAPA Management", "21 CFR Part 11", "SHA-256 Audit"]
        for i, feat in enumerate(features):
            x = 0.2 + i * 0.2
            delay = 3.0 + i * 0.4
            a = min(1.0, max(0, (phase - delay) / 0.8))
            rect = FancyBboxPatch((x - 0.08, 0.30), 0.16, 0.06,
                                   boxstyle="round,pad=0.01",
                                   facecolor=TEAL, alpha=a * 0.3, edgecolor=TEAL,
                                   linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x, 0.33, feat, fontsize=11, color=WHITE, ha='center', va='center',
                    alpha=a, fontweight='600')

    # ═══════════════════════════════════════════════════════════
    #  SCENE 2: Dashboard Overview (6–18s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 18:
        t_local = phase - 6

        # Simulated app layout
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1920); ax.set_ylim(0, 1080)
        ax.set_facecolor(SLATE50); ax.axis('off')
        ax.invert_yaxis()

        # Sidebar
        sidebar = FancyBboxPatch((0, 0), 220, 1080, boxstyle="square",
                                  facecolor=BG_DARK, edgecolor='none')
        ax.add_patch(sidebar)

        # Logo
        logo_bg = FancyBboxPatch((20, 18), 36, 36, boxstyle="round,pad=2",
                                  facecolor=TEAL, edgecolor='none')
        ax.add_patch(logo_bg)
        ax.text(72, 40, "vinQuality", fontsize=16, color=WHITE, fontweight='bold', va='center')

        # Nav items
        nav_items = [
            ("Dashboard", TEAL, True),
            ("NCMRs", GRAY, False),
            ("Deviations", GRAY, False),
            ("CAPAs", GRAY, False),
            ("SCARs", GRAY, False),
            ("Analytics", GRAY, False),
            ("Calibration", GRAY, False),
        ]
        for i, (name, clr, active) in enumerate(nav_items):
            y = 80 + i * 44
            if active:
                bg = FancyBboxPatch((10, y - 6), 200, 36, boxstyle="round,pad=2",
                                     facecolor=TEAL, alpha=0.15, edgecolor='none')
                ax.add_patch(bg)
            ax.text(50, y + 12, name, fontsize=13, color=clr if not active else TEAL_LIGHT,
                    va='center', fontweight='600' if active else '400')

        # Top bar
        topbar = FancyBboxPatch((220, 0), 1700, 60, boxstyle="square",
                                 facecolor=WHITE, edgecolor='#E2E8F0', linewidth=1)
        ax.add_patch(topbar)
        ax.text(250, 34, "Quality Dashboard", fontsize=20, color=BG_DARK,
                fontweight='bold', va='center')

        # Stat cards (animated reveal)
        cards = [
            ("Open NCMRs", "24", "+3 this week", RED, 250),
            ("Active CAPAs", "12", "On track", TEAL, 490),
            ("SLA Compliance", "94%", "30-day avg", GREEN, 730),
            ("Pending Approvals", "7", "Action needed", AMBER, 970),
        ]
        for i, (label, val, sub, clr, x) in enumerate(cards):
            delay = 0.5 + i * 0.4
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            card = FancyBboxPatch((x, 80), 210, 100, boxstyle="round,pad=4",
                                   facecolor=WHITE, edgecolor='#E2E8F0', linewidth=1, alpha=a)
            ax.add_patch(card)
            ax.text(x + 20, 110, label, fontsize=12, color=GRAY, alpha=a)
            ax.text(x + 20, 148, val, fontsize=36, color=BG_DARK, fontweight='bold', alpha=a)
            ax.text(x + 100, 155, sub, fontsize=11, color=clr, alpha=a)

        # NCMR table (animated rows)
        table_bg = FancyBboxPatch((250, 200), 700, 420, boxstyle="round,pad=4",
                                   facecolor=WHITE, edgecolor='#E2E8F0', linewidth=1)
        ax.add_patch(table_bg)
        ax.text(270, 230, "Recent Non-Conformance Reports", fontsize=15,
                color=BG_DARK, fontweight='bold')

        headers = ["NCMR #", "Title", "Status", "Priority", "Assigned"]
        hx = [270, 440, 700, 810, 870]
        for hdr, hx_pos in zip(headers, hx):
            ax.text(hx_pos, 262, hdr, fontsize=10, color=GRAY, fontweight='600')

        rows = [
            ("NCMR-2026-00142", "Dimensional out-of-spec on shaft bearing", "In Review", "High", "J. Martinez"),
            ("NCMR-2026-00141", "Surface finish non-conformance on housing", "Pending CAPA", "Medium", "S. Patel"),
            ("NCMR-2026-00140", "Material certification mismatch — Lot 4421", "Dispositioned", "High", "R. Chen"),
            ("NCMR-2026-00139", "Weld porosity on assembly A-12", "Closed", "Low", "A. Kim"),
            ("NCMR-2026-00138", "Supplier packaging damage — PO 8812", "Open", "Medium", "T. Nguyen"),
        ]
        status_bg = {
            "In Review": ("#FEF3C7", AMBER),
            "Pending CAPA": ("#DBEAFE", BLUE),
            "Dispositioned": ("#D1FAE5", GREEN),
            "Closed": ("#F3E8FF", PURPLE),
            "Open": ("#FEF3C7", AMBER),
        }
        prio_bg = {
            "High": ("#FEE2E2", RED),
            "Medium": ("#FEF3C7", AMBER),
            "Low": ("#DBEAFE", BLUE),
        }

        for i, (ncmr_id, title, status, prio, assigned) in enumerate(rows):
            delay = 2.5 + i * 0.5
            a = min(1.0, max(0, (t_local - delay) / 0.6))
            y = 290 + i * 48

            # Row stripe
            if i % 2 == 0:
                stripe = FancyBboxPatch((255, y - 8), 690, 40, boxstyle="square",
                                         facecolor='#F8FAFC', edgecolor='none', alpha=a)
                ax.add_patch(stripe)

            ax.text(270, y + 12, ncmr_id, fontsize=11, color=TEAL, fontweight='500', alpha=a)
            ax.text(440, y + 12, title[:38], fontsize=11, color='#334155', alpha=a)

            sb, sf = status_bg.get(status, ('#F1F5F9', GRAY))
            badge = FancyBboxPatch((695, y), 90, 24, boxstyle="round,pad=3",
                                    facecolor=sb, edgecolor='none', alpha=a)
            ax.add_patch(badge)
            ax.text(740, y + 13, status, fontsize=9, color=sf, ha='center',
                    fontweight='600', alpha=a)

            pb, pf = prio_bg.get(prio, ('#F1F5F9', GRAY))
            pbadge = FancyBboxPatch((805, y), 52, 24, boxstyle="round,pad=3",
                                     facecolor=pb, edgecolor='none', alpha=a)
            ax.add_patch(pbadge)
            ax.text(831, y + 13, prio, fontsize=9, color=pf, ha='center',
                    fontweight='600', alpha=a)

            ax.text(870, y + 12, assigned, fontsize=11, color=GRAY, alpha=a)

        # Mini donut chart
        chart_bg = FancyBboxPatch((970, 200), 250, 200, boxstyle="round,pad=4",
                                   facecolor=WHITE, edgecolor='#E2E8F0', linewidth=1)
        ax.add_patch(chart_bg)
        ax.text(990, 230, "NCMRs by Status", fontsize=13, color=BG_DARK, fontweight='bold')

        # Draw donut segments
        if t_local > 3:
            chart_a = min(1.0, (t_local - 3) / 1.5)
            center_x, center_y = 1095, 330
            radius = 55
            total = sum(status_counts)
            angle_start = 90
            for cnt, clr in zip(status_counts, status_colors):
                angle_span = (cnt / total) * 360
                theta1 = np.radians(np.linspace(angle_start, angle_start + angle_span, 50))
                theta2 = np.radians(np.linspace(angle_start + angle_span, angle_start, 50))
                outer_x = center_x + radius * np.cos(theta1)
                outer_y = center_y - radius * np.sin(theta1)
                inner_x = center_x + (radius - 18) * np.cos(theta2)
                inner_y = center_y - (radius - 18) * np.sin(theta2)
                verts_x = np.concatenate([outer_x, inner_x])
                verts_y = np.concatenate([outer_y, inner_y])
                ax.fill(verts_x, verts_y, color=clr, alpha=chart_a * 0.85)
                angle_start += angle_span
            ax.text(center_x, center_y, "48", fontsize=22, color=BG_DARK,
                    ha='center', va='center', fontweight='bold', alpha=chart_a)

        # Trend chart
        trend_bg = FancyBboxPatch((970, 420), 250, 200, boxstyle="round,pad=4",
                                   facecolor=WHITE, edgecolor='#E2E8F0', linewidth=1)
        ax.add_patch(trend_bg)
        ax.text(990, 450, "Monthly Trend", fontsize=13, color=BG_DARK, fontweight='bold')

        if t_local > 4:
            trend_a = min(1.0, (t_local - 4) / 1.5)
            bar_w = 25
            for i, (m, cnt) in enumerate(zip(months, ncmr_counts)):
                bx = 1000 + i * 38
                bh = cnt * 4
                by = 600 - bh
                opacity_factor = 0.3 + 0.12 * i
                bar = FancyBboxPatch((bx, by), bar_w, bh, boxstyle="round,pad=1",
                                      facecolor=TEAL, alpha=trend_a * opacity_factor, edgecolor='none')
                ax.add_patch(bar)
                ax.text(bx + bar_w/2, 612, m, fontsize=8, color=GRAY, ha='center',
                        alpha=trend_a)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 3: NCMR Workflow (18–30s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 30:
        t_local = phase - 18

        ax = fig.add_axes([0.02, 0.05, 0.96, 0.88])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        fig.text(0.5, 0.96, "NCMR LIFECYCLE WORKFLOW", fontsize=20,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        steps = [
            ("Create", "Log non-conformance\nwith photos & details", RED, 0.08),
            ("Investigate", "Root cause analysis\n& impact assessment", AMBER, 0.24),
            ("Review", "Quality team reviews\nfindings & disposition", BLUE, 0.40),
            ("CAPA Link", "Link corrective actions\nfor systemic issues", PURPLE, 0.56),
            ("Disposition", "Accept, rework, scrap\nor return to supplier", GREEN, 0.72),
            ("Close", "Verify effectiveness\n& archive record", TEAL, 0.88),
        ]

        for i, (title, desc, clr, x) in enumerate(steps):
            delay = 0.5 + i * 1.2
            a = min(1.0, max(0, (t_local - delay) / 1.0))

            # Step card
            card = FancyBboxPatch((x - 0.05, 0.45), 0.12, 0.35,
                                   boxstyle="round,pad=0.008",
                                   facecolor=BG_CARD, alpha=a,
                                   edgecolor=clr, linewidth=2)
            ax.add_patch(card)

            # Step number circle
            circle = Circle((x + 0.01, 0.74), 0.025, facecolor=clr, alpha=a * 0.9)
            ax.add_patch(circle)
            ax.text(x + 0.01, 0.74, str(i + 1), fontsize=14, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)

            ax.text(x + 0.01, 0.64, title, fontsize=13, color=WHITE,
                    ha='center', va='center', fontweight='bold', alpha=a)
            ax.text(x + 0.01, 0.54, desc, fontsize=9, color=GRAY,
                    ha='center', va='center', alpha=a, linespacing=1.5)

            # Arrow to next
            if i < len(steps) - 1:
                arrow_delay = delay + 0.8
                arrow_a = min(1.0, max(0, (t_local - arrow_delay) / 0.5))
                ax.annotate('', xy=(x + 0.09, 0.62), xytext=(x + 0.065, 0.62),
                           arrowprops=dict(arrowstyle='->', color=TEAL_LIGHT,
                                          lw=2, alpha=arrow_a))

        # Bottom: compliance badges
        if t_local > 8:
            badge_a = min(1.0, (t_local - 8) / 1.5)
            badges = ["21 CFR Part 11", "ISO 9001", "AS9100", "IATF 16949"]
            for i, badge_text in enumerate(badges):
                bx = 0.2 + i * 0.2
                badge = FancyBboxPatch((bx - 0.06, 0.15), 0.12, 0.05,
                                        boxstyle="round,pad=0.005",
                                        facecolor=TEAL, alpha=badge_a * 0.2,
                                        edgecolor=TEAL, linewidth=1)
                ax.add_patch(badge)
                ax.text(bx, 0.175, badge_text, fontsize=10, color=WHITE,
                        ha='center', va='center', fontweight='500', alpha=badge_a)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 4: CAPA Management (30–42s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 42:
        t_local = phase - 30
        gs = GridSpec(1, 2, figure=fig, wspace=0.25, left=0.06, right=0.96, top=0.88, bottom=0.08)

        fig.text(0.5, 0.95, "CAPA MANAGEMENT & CONTINUOUS IMPROVEMENT", fontsize=18,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        # Left: CAPA record detail
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
        ax1.set_facecolor(BG_CARD); ax1.axis('off')
        for spine in ax1.spines.values():
            spine.set_color('#334155')

        ax1.text(0.5, 0.95, "CAPA-2026-00034", fontsize=16, color=TEAL_LIGHT,
                 ha='center', va='top', fontweight='bold')
        ax1.text(0.5, 0.88, "Linked to NCMR-2026-00142", fontsize=11,
                 color=GRAY, ha='center', va='top')

        fields = [
            ("Root Cause", "Worn tool insert causing dimensional drift on CNC lathe #4"),
            ("Corrective Action", "Replace insert per schedule; add SPC monitoring on critical dims"),
            ("Preventive Action", "Implement tool wear tracking system with automatic alerts"),
            ("Assigned To", "J. Martinez — Quality Engineering"),
            ("Due Date", "2026-04-15  |  SLA: 30 days remaining"),
            ("Status", "In Progress — 60% complete"),
        ]

        for i, (label, value) in enumerate(fields):
            delay = 0.8 + i * 0.8
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            y = 0.78 - i * 0.12
            bg_a = 0.12 if i % 2 == 0 else 0.06
            rect = FancyBboxPatch((0.03, y - 0.03), 0.94, 0.10,
                                   boxstyle="round,pad=0.005",
                                   facecolor=WHITE, alpha=a * bg_a, edgecolor='none',
                                   transform=ax1.transAxes)
            ax1.add_patch(rect)
            ax1.text(0.05, y + 0.02, label, fontsize=10, color=TEAL_LIGHT,
                     va='center', fontweight='600', alpha=a, transform=ax1.transAxes)
            ax1.text(0.05, y - 0.03, value[:65], fontsize=9, color=WHITE,
                     va='center', alpha=a, transform=ax1.transAxes)

        # Right: CAPA effectiveness metrics
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_facecolor(BG_CARD); ax2.axis('off')

        ax2.text(0.5, 0.95, "CAPA Effectiveness Dashboard", fontsize=15, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # Animated bar chart: CAPAs by category
        categories = ["Design", "Process", "Material", "Supplier", "Training"]
        cat_vals = [8, 14, 6, 10, 4]
        cat_colors = [BLUE, TEAL, AMBER, PURPLE, GREEN]
        max_val = max(cat_vals)

        for i, (cat, val, clr) in enumerate(zip(categories, cat_vals, cat_colors)):
            delay = 2.0 + i * 0.5
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            y = 0.80 - i * 0.13
            bar_w = (val / max_val) * 0.55

            bar = FancyBboxPatch((0.30, y - 0.02), bar_w * a, 0.06,
                                  boxstyle="round,pad=0.003",
                                  facecolor=clr, alpha=a * 0.7, edgecolor='none',
                                  transform=ax2.transAxes)
            ax2.add_patch(bar)
            ax2.text(0.05, y + 0.01, cat, fontsize=11, color=WHITE,
                     va='center', fontweight='500', alpha=a, transform=ax2.transAxes)
            ax2.text(0.30 + bar_w * a + 0.02, y + 0.01, str(val), fontsize=12,
                     color=clr, va='center', fontweight='bold', alpha=a, transform=ax2.transAxes)

        # Effectiveness rate circle
        if t_local > 6:
            eff_a = min(1.0, (t_local - 6) / 1.5)
            circle = Circle((0.5, 0.18), 0.10, facecolor=BG_DARK,
                            edgecolor=TEAL, linewidth=3, alpha=eff_a,
                            transform=ax2.transAxes)
            ax2.add_patch(circle)
            ax2.text(0.5, 0.19, "87%", fontsize=20, color=TEAL_LIGHT,
                     ha='center', va='center', fontweight='bold', alpha=eff_a,
                     transform=ax2.transAxes)
            ax2.text(0.5, 0.12, "Effectiveness Rate", fontsize=9, color=GRAY,
                     ha='center', va='center', alpha=eff_a, transform=ax2.transAxes)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 5: Audit Trail & Compliance (42–56s)
    # ═══════════════════════════════════════════════════════════
    elif phase < 56:
        t_local = phase - 42
        gs = GridSpec(1, 2, figure=fig, wspace=0.25, left=0.06, right=0.96, top=0.88, bottom=0.08)

        fig.text(0.5, 0.95, "TAMPER-EVIDENT AUDIT TRAIL & COMPLIANCE", fontsize=18,
                 color=TEAL_LIGHT, ha='center', fontweight='bold')

        # Left: Hash chain visualization
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
        ax1.set_facecolor(BG_CARD); ax1.axis('off')

        ax1.text(0.5, 0.95, "SHA-256 Hash Chain Audit Trail", fontsize=14, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        audit_entries = [
            ("14:23:05", "NCMR-142 created", "J. Martinez", "a3f8b2...c91d"),
            ("14:25:18", "Status → In Review", "System", "7d2e91...4f8a"),
            ("15:01:42", "Investigation added", "S. Patel", "b8c3d1...e72f"),
            ("15:45:09", "E-Signature applied", "R. Chen (QA Mgr)", "f1a9c4...3b6e"),
            ("16:12:33", "CAPA-034 linked", "J. Martinez", "c5e8f2...d41a"),
            ("16:30:00", "Disposition: Rework", "R. Chen (QA Mgr)", "92b4a7...8c3f"),
        ]

        for i, (time, action, user, hash_val) in enumerate(audit_entries):
            delay = 0.8 + i * 1.0
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            y = 0.82 - i * 0.12

            # Chain link indicator
            if i > 0:
                ax1.plot([0.06, 0.06], [y + 0.12, y + 0.06], color=TEAL, lw=2, alpha=a * 0.5)

            dot = Circle((0.06, y + 0.02), 0.012, facecolor=TEAL, alpha=a)
            ax1.add_patch(dot)

            ax1.text(0.12, y + 0.04, time, fontsize=9, color=GRAY, alpha=a, transform=ax1.transAxes)
            ax1.text(0.26, y + 0.04, action, fontsize=10, color=WHITE,
                     fontweight='500', alpha=a, transform=ax1.transAxes)
            ax1.text(0.26, y - 0.02, user, fontsize=8, color=GRAY, alpha=a, transform=ax1.transAxes)
            ax1.text(0.70, y + 0.01, hash_val, fontsize=9, color=TEAL_LIGHT,
                     alpha=a, fontfamily='monospace', transform=ax1.transAxes)

        # Right: E-signature + Compliance
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim(0, 1); ax2.set_ylim(0, 1)
        ax2.set_facecolor(BG_CARD); ax2.axis('off')

        ax2.text(0.5, 0.95, "21 CFR Part 11 E-Signatures", fontsize=14, color=WHITE,
                 ha='center', va='top', fontweight='bold')

        # E-signature card
        if t_local > 2:
            esig_a = min(1.0, (t_local - 2) / 1.5)
            sig_card = FancyBboxPatch((0.05, 0.55), 0.90, 0.32,
                                       boxstyle="round,pad=0.01",
                                       facecolor=BG_DARK, alpha=esig_a,
                                       edgecolor=TEAL, linewidth=2,
                                       transform=ax2.transAxes)
            ax2.add_patch(sig_card)
            ax2.text(0.5, 0.82, "Electronic Signature Record", fontsize=12,
                     color=TEAL_LIGHT, ha='center', fontweight='bold', alpha=esig_a,
                     transform=ax2.transAxes)
            ax2.text(0.10, 0.74, "Signer:", fontsize=10, color=GRAY, alpha=esig_a,
                     transform=ax2.transAxes)
            ax2.text(0.30, 0.74, "R. Chen, Quality Assurance Manager", fontsize=10,
                     color=WHITE, alpha=esig_a, transform=ax2.transAxes)
            ax2.text(0.10, 0.67, "Meaning:", fontsize=10, color=GRAY, alpha=esig_a,
                     transform=ax2.transAxes)
            ax2.text(0.30, 0.67, "Approved — Disposition authorized", fontsize=10,
                     color=GREEN, alpha=esig_a, transform=ax2.transAxes)
            ax2.text(0.10, 0.60, "Method:", fontsize=10, color=GRAY, alpha=esig_a,
                     transform=ax2.transAxes)
            ax2.text(0.30, 0.60, "Password re-authentication verified", fontsize=10,
                     color=WHITE, alpha=esig_a, transform=ax2.transAxes)

        # Compliance badges
        compliance = [
            ("21 CFR Part 11", "FDA electronic records\n& signatures"),
            ("ISO 9001:2015", "Quality management\nsystem requirements"),
            ("AS9100 Rev D", "Aerospace quality\nmanagement"),
            ("IATF 16949", "Automotive quality\nstandard"),
        ]

        for i, (std, desc) in enumerate(compliance):
            delay = 6.0 + i * 1.0
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            col = i % 2
            row = i // 2
            bx = 0.08 + col * 0.48
            by = 0.35 - row * 0.20

            badge = FancyBboxPatch((bx, by), 0.42, 0.15,
                                    boxstyle="round,pad=0.008",
                                    facecolor=TEAL, alpha=a * 0.15,
                                    edgecolor=TEAL, linewidth=1.5,
                                    transform=ax2.transAxes)
            ax2.add_patch(badge)
            ax2.text(bx + 0.21, by + 0.10, std, fontsize=11, color=WHITE,
                     ha='center', fontweight='bold', alpha=a, transform=ax2.transAxes)
            ax2.text(bx + 0.21, by + 0.03, desc, fontsize=8, color=GRAY,
                     ha='center', alpha=a, transform=ax2.transAxes, linespacing=1.3)

    # ═══════════════════════════════════════════════════════════
    #  SCENE 6: Closing (56–66s)
    # ═══════════════════════════════════════════════════════════
    else:
        t_local = phase - 56
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        ax.set_facecolor(BG_DARK); ax.axis('off')

        alpha = min(1.0, t_local / 2.0)

        ax.text(0.5, 0.68, "vinQuality", fontsize=60, fontweight='bold',
                color=WHITE, ha='center', va='center', alpha=alpha)

        line_w = min(0.35, t_local * 0.08)
        ax.plot([0.325, 0.325 + line_w], [0.60, 0.60], color=TEAL, lw=4, alpha=alpha)

        ax.text(0.5, 0.50, "Enterprise Quality Management, Zero Overhead.",
                fontsize=22, color=TEAL_LIGHT, ha='center', va='center',
                alpha=min(1, max(0, (t_local - 1.5) / 1.5)))

        modules = ["NCMR Tracking", "CAPA Management", "SCAR Workflow",
                   "Deviation Control", "Calibration", "Analytics & Reports"]
        for i, mod in enumerate(modules):
            row = i // 3
            col = i % 3
            x = 0.22 + col * 0.28
            y = 0.35 - row * 0.10
            delay = 3.0 + i * 0.3
            a = min(1.0, max(0, (t_local - delay) / 0.8))
            ax.text(x, y, mod, fontsize=13, color=WHITE, ha='center',
                    va='center', alpha=a, fontweight='500')

        if t_local > 6:
            a2 = min(1.0, (t_local - 6) / 1.5)
            ax.text(0.5, 0.10, "Start Your Free Trial  |  vinqms.com",
                    fontsize=15, color=TEAL_LIGHT, ha='center', va='center',
                    alpha=a2, fontweight='600')


# ── Render ──
BASE = os.path.dirname(__file__)

print("=" * 60)
print("Rendering vinQuality Overview Video (frames)...")
print("=" * 60)
anim_obj = animation.FuncAnimation(fig, draw_frame, frames=TOTAL_FRAMES, interval=1000/FPS)
writer = animation.FFMpegWriter(fps=FPS, bitrate=5000, extra_args=['-pix_fmt', 'yuv420p'])
silent_path = os.path.join(BASE, "vq_overview_silent.mp4")
anim_obj.save(silent_path, writer=writer)
plt.close()
print("Video frames done.")

print("Generating voiceover...")
vo_path = os.path.join(BASE, "vq_overview_vo.mp3")
create_voiceover_track(VO_SEGMENTS, DURATION, vo_path)

print("Muxing with sitar background...")
final_path = os.path.join(BASE, "VinQuality_Platform_Overview.mp4")
mux_video_audio_with_music(silent_path, vo_path, final_path, DURATION)

for f in [silent_path, vo_path]:
    try: os.remove(f)
    except OSError: pass

print(f"\n[OK] vinQuality Overview complete: {final_path}")
