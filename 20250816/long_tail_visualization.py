import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy import stats

# Read the data
df = pd.read_excel('LLM_all_removed.xlsx')

# Clean assignee names
def clean_assignee(name):
    if pd.isna(name):
        return 'UNASSIGNED'
    name = name.strip().lstrip(':').strip()
    return name

df['clean_assignee'] = df['assignees'].apply(clean_assignee)
df['issued_date'] = pd.to_datetime(df['issued'])
df['year'] = df['issued_date'].dt.year

# Count patents per assignee
assignee_counts = df['clean_assignee'].value_counts()

# Create comprehensive visualization
fig = plt.figure(figsize=(18, 12))

# 1. Power Law Distribution
ax1 = plt.subplot(2, 3, 1)
# Sort assignees by patent count
sorted_counts = assignee_counts.values
x_rank = np.arange(1, len(sorted_counts) + 1)
ax1.loglog(x_rank, sorted_counts, 'b-', alpha=0.6, linewidth=1)
ax1.set_xlabel('Assignee Rank (log scale)')
ax1.set_ylabel('Number of Patents (log scale)')
ax1.set_title('Power Law Distribution of Patent Holdings', fontweight='bold')
ax1.grid(True, alpha=0.3)
# Add reference lines
ax1.axhline(y=10, color='r', linestyle='--', alpha=0.5, label='Long tail threshold (10 patents)')
ax1.axhline(y=1, color='g', linestyle='--', alpha=0.5, label='Single patent')
ax1.legend(fontsize=8)

# 2. Distribution Histogram
ax2 = plt.subplot(2, 3, 2)
bins = [1, 2, 3, 4, 5, 6, 10, 20, 50, 100, 500, 6000]
hist_data = []
labels = []
for i in range(len(bins)-1):
    if i == 0:
        count = (assignee_counts == bins[i]).sum()
        labels.append(f'{bins[i]}')
    else:
        count = ((assignee_counts >= bins[i]) & (assignee_counts < bins[i+1])).sum()
        if bins[i+1] <= 10:
            labels.append(f'{bins[i]}-{bins[i+1]-1}')
        else:
            labels.append(f'{bins[i]}-{bins[i+1]}')
    hist_data.append(count)

colors = plt.cm.viridis(np.linspace(0, 1, len(hist_data)))
bars = ax2.bar(range(len(hist_data)), hist_data, color=colors)
ax2.set_xticks(range(len(labels)))
ax2.set_xticklabels(labels, rotation=45, ha='right')
ax2.set_ylabel('Number of Assignees')
ax2.set_title('Distribution of Assignees by Patent Count', fontweight='bold')
ax2.set_yscale('log')
# Add value labels
for bar, val in zip(bars, hist_data):
    if val > 0:
        ax2.text(bar.get_x() + bar.get_width()/2, val * 1.1, f'{val:,}', 
                ha='center', fontsize=8)

# 3. Cumulative Patent Share
ax3 = plt.subplot(2, 3, 3)
cumsum = assignee_counts.cumsum()
cumsum_pct = (cumsum / cumsum.iloc[-1]) * 100
x_pct = (np.arange(1, len(cumsum) + 1) / len(cumsum)) * 100

ax3.plot(x_pct, cumsum_pct, 'b-', linewidth=2)
ax3.set_xlabel('Percentage of Assignees')
ax3.set_ylabel('Cumulative % of Patents')
ax3.set_title('Lorenz Curve: Patent Concentration', fontweight='bold')
ax3.grid(True, alpha=0.3)
# Add reference lines
ax3.plot([0, 100], [0, 100], 'r--', alpha=0.5, label='Perfect equality')
ax3.axhline(y=80, color='g', linestyle=':', alpha=0.5)
ax3.axvline(x=16.9, color='g', linestyle=':', alpha=0.5)
ax3.text(20, 75, '16.9% hold 80%', fontsize=9, color='green')
ax3.legend(fontsize=8)

# 4. Geographic Distribution in Long Tail
ax4 = plt.subplot(2, 3, 4)
long_tail = assignee_counts[assignee_counts <= 10].index
long_tail_df = df[df['clean_assignee'].isin(long_tail)]

def extract_country(assignee):
    match = re.search(r'\(([A-Z]{2})\)\s*$', assignee)
    if match:
        return match.group(1)
    return 'Unknown'

long_tail_df['country'] = long_tail_df['clean_assignee'].apply(extract_country)
country_dist = long_tail_df['country'].value_counts().head(10)

colors = plt.cm.tab20(np.arange(len(country_dist)))
bars = ax4.barh(range(len(country_dist)), country_dist.values, color=colors)
ax4.set_yticks(range(len(country_dist)))
ax4.set_yticklabels(country_dist.index)
ax4.set_xlabel('Number of Patents')
ax4.set_title('Top 10 Countries in Long Tail (≤10 patents)', fontweight='bold')
ax4.invert_yaxis()
# Add value labels
for bar, val in zip(bars, country_dist.values):
    ax4.text(val + 50, bar.get_y() + bar.get_height()/2, f'{val:,}', 
            va='center', fontsize=9)

# 5. Temporal Evolution of Long Tail
ax5 = plt.subplot(2, 3, 5)
years = range(2014, 2025)
long_tail_yearly = []
total_yearly = []

for year in years:
    year_df = df[df['year'] == year]
    year_counts = year_df['clean_assignee'].value_counts()
    long_tail_year = (year_counts <= 10).sum()
    long_tail_yearly.append(long_tail_year)
    total_yearly.append(len(year_counts))

ax5.plot(years, long_tail_yearly, 'b-', marker='o', label='Long tail assignees', linewidth=2)
ax5_twin = ax5.twinx()
ax5_twin.plot(years, total_yearly, 'r-', marker='s', label='Total assignees', linewidth=2)

ax5.set_xlabel('Year')
ax5.set_ylabel('Long Tail Assignees (≤10 patents)', color='b')
ax5_twin.set_ylabel('Total Assignees', color='r')
ax5.set_title('Growth of Long Tail Over Time', fontweight='bold')
ax5.tick_params(axis='y', labelcolor='b')
ax5_twin.tick_params(axis='y', labelcolor='r')
ax5.grid(True, alpha=0.3)

# 6. Patent Share by Group
ax6 = plt.subplot(2, 3, 6)
groups = {
    'Single\n(1 patent)': assignee_counts[assignee_counts == 1].sum(),
    'Small\n(2-5)': assignee_counts[(assignee_counts >= 2) & (assignee_counts <= 5)].sum(),
    'Medium\n(6-10)': assignee_counts[(assignee_counts >= 6) & (assignee_counts <= 10)].sum(),
    'Large\n(11-50)': assignee_counts[(assignee_counts >= 11) & (assignee_counts <= 50)].sum(),
    'Very Large\n(51-100)': assignee_counts[(assignee_counts >= 51) & (assignee_counts <= 100)].sum(),
    'Giants\n(>100)': assignee_counts[assignee_counts > 100].sum()
}

sizes = list(groups.values())
labels = [f'{k}\n{v:,} patents\n({v/sum(sizes)*100:.1f}%)' for k, v in groups.items()]
colors = plt.cm.Set3(np.arange(len(groups)))

wedges, texts = ax6.pie(sizes, labels=labels, colors=colors, startangle=90)
ax6.set_title('Patent Distribution by Assignee Size', fontweight='bold')

# Adjust text size
for text in texts:
    text.set_fontsize(8)

plt.suptitle('Long Tail Analysis of LLM Patent Landscape', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('long_tail_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print('\nVisualization saved as: long_tail_analysis.png')

# Calculate and print Gini coefficient
def gini_coefficient(x):
    """Calculate Gini coefficient"""
    sorted_x = np.sort(x)
    n = len(x)
    cumsum = np.cumsum(sorted_x)
    return (2 * np.sum((np.arange(1, n+1)) * sorted_x)) / (n * cumsum[-1]) - (n + 1) / n

gini = gini_coefficient(assignee_counts.values)
print(f'\nGini Coefficient: {gini:.3f}')
print('(0 = perfect equality, 1 = perfect inequality)')
print(f'Interpretation: {"High" if gini > 0.6 else "Moderate"} concentration of patents among assignees')