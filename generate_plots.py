import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams.update({
    'font.family': 'serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'figure.dpi': 150,
})

BLUE   = '#1f4e79'
ORANGE = '#c55a11'
GRAY   = '#595959'
LBLUE  = '#9dc3e6'

# ══════════════════════════════════════════════════════════════════════════════
# Figure 1 – Cost trend: Financial Sector vs Global (IBM 2020-2025)
# ══════════════════════════════════════════════════════════════════════════════
years   = [2020, 2021, 2022, 2023, 2024, 2025]
finance = [5.85, 5.72, 5.97, 5.90, 6.08, 5.56]
global_ = [3.86, 4.24, 4.35, 4.45, 4.88, 4.44]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(years, finance, marker='o', color=BLUE,   linewidth=2, label='Financial Sector')
ax.plot(years, global_, marker='s', color=ORANGE, linewidth=2, linestyle='--', label='Global Average')

for x, y in zip(years, finance):
    ax.annotate(f'${y:.2f}M', (x, y), textcoords='offset points',
                xytext=(0, 8), ha='center', fontsize=8, color=BLUE)
for x, y in zip(years, global_):
    ax.annotate(f'${y:.2f}M', (x, y), textcoords='offset points',
                xytext=(0, -14), ha='center', fontsize=8, color=ORANGE)

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Average Cost (USD Millions)', fontsize=11)
ax.set_title('Average Data Breach Cost: Financial Sector vs. Global Average\n(IBM Reports 2020–2025)',
             fontsize=11, fontweight='bold', pad=12)
ax.legend(fontsize=10)
ax.set_xticks(years)
ax.set_ylim(3, 7.5)
fig.tight_layout()
fig.savefig('fig1_cost_trend.pdf', bbox_inches='tight')
fig.savefig('fig1_cost_trend.png', bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 2 – Premium: how much more does finance pay vs global? (gap over time)
# ══════════════════════════════════════════════════════════════════════════════
premium = [f - g for f, g in zip(finance, global_)]
pct     = [(f - g) / g * 100 for f, g in zip(finance, global_)]

fig, ax1 = plt.subplots(figsize=(7, 4))
bars = ax1.bar(years, premium, color=LBLUE, edgecolor=BLUE, linewidth=1.2, label='Absolute Premium (USD M)')
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Cost Premium (USD Millions)', fontsize=11, color=BLUE)
ax1.tick_params(axis='y', labelcolor=BLUE)
ax1.set_ylim(0, 3)

ax2 = ax1.twinx()
ax2.spines['top'].set_visible(False)
ax2.plot(years, pct, marker='D', color=ORANGE, linewidth=2, label='Relative Premium (%)')
ax2.set_ylabel('Relative Premium (%)', fontsize=11, color=ORANGE)
ax2.tick_params(axis='y', labelcolor=ORANGE)
ax2.set_ylim(0, 70)

for bar, p in zip(bars, premium):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
             f'+${p:.2f}M', ha='center', va='bottom', fontsize=8, color=BLUE)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper left')

ax1.set_title('Financial Sector Cost Premium Over Global Average (2020–2025)',
              fontsize=11, fontweight='bold', pad=12)
ax1.set_xticks(years)
fig.tight_layout()
fig.savefig('fig2_premium.pdf', bbox_inches='tight')
fig.savefig('fig2_premium.png', bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 3 – Root causes pie (IBM 2024)
# ══════════════════════════════════════════════════════════════════════════════
causes = ['Malicious /\nCyberattack', 'Human\nError', 'IT System\nFailure']
shares = [51, 26, 23]

fig, ax = plt.subplots(figsize=(5.5, 5.5))
wedge_colors = [BLUE, ORANGE, '#a6a6a6']
wedges, texts, autotexts = ax.pie(
    shares, labels=causes, autopct='%1.0f%%', colors=wedge_colors,
    startangle=140, pctdistance=0.75,
    wedgeprops=dict(edgecolor='white', linewidth=2),
    textprops={'fontsize': 10}
)
for at in autotexts:
    at.set_color('white')
    at.set_fontweight('bold')

ax.set_title('Root Causes of Data Breaches, All Industries (IBM 2024)',
             fontsize=11, fontweight='bold', pad=16)
fig.tight_layout()
fig.savefig('fig3_root_causes.pdf', bbox_inches='tight')
fig.savefig('fig3_root_causes.png', bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# Figure 4 – Attack vectors in Financial & Insurance (Verizon DBIR 2024)
# ══════════════════════════════════════════════════════════════════════════════
# Source: Verizon DBIR 2024 Finance & Insurance snapshot
vectors  = ['System\nIntrusion', 'Social\nEngineering', 'Miscellaneous\nErrors',
            'Web\nApplications', 'Privilege\nMisuse']
pct_fin  = [38, 31, 13, 10, 8]   # approximate % of breaches in Finance sector

fig, ax = plt.subplots(figsize=(7, 4))
y_pos = np.arange(len(vectors))
colors = [BLUE if i < 2 else GRAY for i in range(len(vectors))]
bars = ax.barh(y_pos, pct_fin, color=colors, edgecolor='white', height=0.55)

for bar, val in zip(bars, pct_fin):
    ax.text(val + 0.4, bar.get_y() + bar.get_height()/2,
            f'{val}%', va='center', fontsize=9)

ax.set_yticks(y_pos)
ax.set_yticklabels(vectors, fontsize=10)
ax.set_xlabel('Share of Breaches (%)', fontsize=11)
ax.set_title('Attack Patterns in Financial & Insurance Sector (Verizon DBIR 2024)',
             fontsize=11, fontweight='bold', pad=12)
ax.set_xlim(0, 50)
ax.invert_yaxis()

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=BLUE, label='Top 2 dominant vectors'),
                   Patch(facecolor=GRAY, label='Secondary vectors')]
ax.legend(handles=legend_elements, fontsize=9, loc='lower right')

fig.tight_layout()
fig.savefig('fig4_attack_vectors.pdf', bbox_inches='tight')
fig.savefig('fig4_attack_vectors.png', bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

print("\nAll figures generated successfully!")
