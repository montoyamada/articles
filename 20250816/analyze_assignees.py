import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Read and prepare data
df = pd.read_excel('LLM_all_removed.xlsx')
df['issued_date'] = pd.to_datetime(df['issued'])
df['year'] = df['issued_date'].dt.year

# Normalize assignee names
def normalize_assignee(name):
    if pd.isna(name):
        return 'UNASSIGNED'
    name = name.strip().lstrip(':').strip()
    name = re.sub(r'\s*\([A-Z]{2}\)\s*$', '', name)
    name = name.upper()
    if 'INTERNATIONAL BUSINESS MACHINES' in name or 'IBM' in name:
        return 'IBM'
    if 'GOOGLE' in name:
        return 'Google'
    if 'MICROSOFT' in name:
        return 'Microsoft'
    if 'SAMSUNG ELECTRONICS' in name:
        return 'Samsung'
    if 'AMAZON TECHNOLOGIES' in name:
        return 'Amazon'
    if 'APPLE' in name:
        return 'Apple'
    if 'CAPITAL ONE' in name:
        return 'Capital One'
    if 'INTEL' in name:
        return 'Intel'
    if 'ADOBE' in name:
        return 'Adobe'
    if 'NVIDIA' in name:
        return 'NVIDIA'
    return name

df['normalized_assignee'] = df['assignees'].apply(normalize_assignee)

# Create visualizations
fig = plt.figure(figsize=(16, 10))

# 1. Top 15 Patent Holders Bar Chart
ax1 = plt.subplot(2, 2, 1)
all_counts = df['normalized_assignee'].value_counts()
# Filter to exclude UNASSIGNED
mask = all_counts.index != 'UNASSIGNED'
top_15 = all_counts[mask].head(15)

colors = plt.cm.tab20(np.linspace(0, 1, len(top_15)))
bars = ax1.barh(range(len(top_15)), top_15.values, color=colors)
ax1.set_yticks(range(len(top_15)))
ax1.set_yticklabels(top_15.index, fontsize=9)
ax1.set_xlabel('Number of Patents')
ax1.set_title('Top 15 LLM Patent Holders', fontweight='bold')
ax1.invert_yaxis()

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_15.values)):
    ax1.text(val + 50, bar.get_y() + bar.get_height()/2, f'{val:,}', 
             va='center', fontsize=8)

# 2. Market Share Pie Chart
ax2 = plt.subplot(2, 2, 2)
# Get top 10 excluding UNASSIGNED
mask = all_counts.index != 'UNASSIGNED'
top_10 = all_counts[mask].head(10)

others_count = len(df) - top_10.sum() - all_counts.get('UNASSIGNED', 0)
pie_data = list(top_10.values) + [others_count]
pie_labels = list(top_10.index) + ['Others']

wedges, texts, autotexts = ax2.pie(pie_data, labels=pie_labels, autopct='%1.1f%%',
                                    startangle=90, textprops={'fontsize': 8})
ax2.set_title('Patent Market Share', fontweight='bold')

# 3. Yearly Trends for Top 5 Players
ax3 = plt.subplot(2, 2, 3)
df_recent = df[(df['year'] >= 2018) & (df['year'] <= 2024)]
top_5_names = ['IBM', 'Google', 'Microsoft', 'Samsung', 'Amazon']

for player in top_5_names:
    player_df = df_recent[df_recent['normalized_assignee'] == player]
    yearly = player_df.groupby('year').size()
    ax3.plot(yearly.index, yearly.values, marker='o', label=player, linewidth=2)

ax3.set_xlabel('Year')
ax3.set_ylabel('Number of Patents')
ax3.set_title('Patent Filing Trends - Top 5 Players (2018-2024)', fontweight='bold')
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3)

# 4. Technology Giants Comparison
ax4 = plt.subplot(2, 2, 4)
categories = {
    'US Tech Giants': ['IBM', 'GOOGLE', 'MICROSOFT', 'AMAZON', 'APPLE', 'INTEL'],
    'Asian Tech': ['SAMSUNG', 'TENCENT', 'BAIDU', 'LG', 'SONY'],
    'AI Specialists': ['NVIDIA', 'DEEPMIND', 'OPENAI'],
    'Enterprise': ['ORACLE', 'SAP', 'ADOBE', 'SALESFORCE'],
    'Finance': ['CAPITAL ONE', 'BANK OF AMERICA', 'JPMORGAN']
}

cat_totals = []
cat_names = []
for cat_name, companies in categories.items():
    total = 0
    for comp in companies:
        # Count exact matches
        total += (df['normalized_assignee'].str.upper() == comp.upper()).sum()
    if total > 0:
        cat_totals.append(total)
        cat_names.append(cat_name)

bars = ax4.bar(cat_names, cat_totals, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
ax4.set_xlabel('Category')
ax4.set_ylabel('Total Patents')
ax4.set_title('Patents by Industry Category', fontweight='bold')
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'{int(height):,}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('patent_assignee_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print('\nVisualization saved as: patent_assignee_analysis.png')