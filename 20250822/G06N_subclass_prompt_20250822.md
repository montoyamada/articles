# G06N Subclassification Analysis Prompt - August 22, 2025

## Context
Following the comprehensive G06N patent analysis completed on August 21, 2025, this prompt captures the deep dive into G06N subclassifications as recommended in the original report.

## Initial Setup
```
Prerequisites:
- G06N_all.xlsx file with 77,265 patents
- Previous analysis filtered to 2014-2024 (72,404 patents)
- Understanding that G06N covers AI technologies
```

## Analysis Request
```
From the G06N report recommendations:
"1. Deep dive into specific G06N subclassifications to understand technology nuances"

Try this first recommendation you proposed.
```

## Step-by-Step Analysis Process

### Step 1: Understanding G06N Structure
```python
# G06N IPC Subclassification Structure:
# G06N3: Neural Networks (biological models)
# G06N5: Knowledge-based models (expert systems, logic)
# G06N7: Probabilistic models (fuzzy logic, Bayesian)
# G06N10: Quantum computing
# G06N20: Machine learning
# G06N99: Other computational models
```

### Step 2: Extract Subclassifications
```python
# Parse classifications column with regex
patterns = re.findall(r'G06N\s*(\d+)(?:/(\d+))?', str(classifications))

# Expected format in data:
# "IPC: G06N 3/08 : IPC: G06N 3/04 : IPC: G06N 20/00"
```

### Step 3: Analyze Distribution
```python
# Count main subcategories (G06N3, G06N20, etc.)
main_subcategories = Counter()

# Count detailed classifications (G06N3/08, G06N20/00, etc.)
detailed_classifications = Counter()

# Track by year for temporal analysis
subcat_by_year = defaultdict(lambda: defaultdict(int))
```

### Step 4: Create Visualizations
Generate 6-panel comprehensive visualization:
1. **Stacked Area Chart** - Evolution of subcategories over time
2. **Pie Chart** - Overall distribution
3. **Growth Rate Comparison** - Year-over-year trends
4. **Technology Focus Shift** - Relative proportions
5. **Emerging Technologies** - Quantum and probabilistic trends
6. **2024 Breakdown** - Current year distribution

Save as: `g06n_subclassification_analysis.png`

### Step 5: Generate Reports
Create comprehensive markdown reports:
- English: `G06N_subclassification_report.md`
- Japanese: `G06N_subclassification_report_JP.md`

## Expected Key Findings

### Distribution (2014-2024)
```
Total G06N classifications: ~118,602
Patents with G06N: 72,404

Main Categories:
- G06N3 (Neural Networks): ~42.4% (50,324 classifications)
- G06N20 (Machine Learning): ~28.7% (34,045 classifications)
- G06N5 (Knowledge Systems): ~17.2% (20,352 classifications)
- G06N7 (Probabilistic): ~6.2% (7,333 classifications)
- G06N99 (Other): ~3.1% (3,715 classifications)
- G06N10 (Quantum): ~2.4% (2,832 classifications)
```

### Top Detailed Classifications
```
1. G06N20/00 - Machine learning general: 25.60%
2. G06N3/08 - Learning methods: 16.58%
3. G06N3/04 - Architecture/Structure: 11.19%
4. G06N5/04 - Inference methods: 8.36%
5. G06N5/02 - Knowledge representation: 5.28%
```

### 2024 Trends
```
ALL subcategories show decline:
- Neural Networks (G06N3): -12.7%
- Machine Learning (G06N20): -16.9%
- Knowledge Systems (G06N5): -24.2%
=> Indicates broad market consolidation
```

## Python Code Template

### Complete Analysis Script
```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter, defaultdict

# Load data
df = pd.read_excel('G06N_all.xlsx')
df['year'] = pd.to_datetime(df['issued'], errors='coerce').dt.year
df_filtered = df[(df['year'] >= 2014) & (df['year'] <= 2024)].copy()

# Extract classifications
all_classifications = []
patent_classifications = []

for idx, row in df_filtered.iterrows():
    classifications = row['classifications']
    if pd.notna(classifications) and isinstance(classifications, str):
        # Parse G06N patterns
        patterns = re.findall(r'G06N\s*(\d+)(?:/(\d+))?', str(classifications))
        patent_class_list = []
        for main, sub in patterns:
            if sub:
                classification = f'G06N{main}/{sub}'
            else:
                classification = f'G06N{main}'
            all_classifications.append(classification)
            patent_class_list.append(classification)
        if patent_class_list:
            patent_classifications.append((row['year'], patent_class_list))

# Analyze distributions
main_subcategories = Counter()
detailed_classifications = Counter()
subcat_by_year = defaultdict(lambda: defaultdict(int))

for classification in all_classifications:
    match = re.match(r'G06N(\d+)', classification)
    if match:
        main_num = match.group(1)
        main_subcategories[f'G06N{main_num}'] += 1
        detailed_classifications[classification] += 1

# Year-by-year analysis
for year, classifications in patent_classifications:
    for classification in classifications:
        match = re.match(r'G06N(\d+)', classification)
        if match:
            main_num = match.group(1)
            subcat_by_year[year][f'G06N{main_num}'] += 1
```

### Visualization Colors
```python
subcat_info = {
    'G06N3': ('Neural Networks', '#FF6B6B'),
    'G06N20': ('Machine Learning', '#4ECDC4'),
    'G06N5': ('Knowledge Systems', '#45B7D1'),
    'G06N7': ('Probabilistic Models', '#96CEB4'),
    'G06N10': ('Quantum Computing', '#FECA57'),
    'G06N99': ('Other Models', '#A8A8A8')
}
```

## Key Insights to Highlight

### Technology Hierarchy
1. **Neural Networks Dominance**: 42.4% confirms deep learning's central role
2. **ML Strong Second**: 28.7% shows classical ML remains vital
3. **Traditional AI Persists**: Knowledge systems at 17.2% still relevant
4. **Quantum Emerging**: 2.4% small but growing steadily

### Market Signals (2024)
- **Universal Decline**: All categories down 12-24%
- **Not Technology-Specific**: Broad market consolidation
- **Maturation Phase**: Shift from quantity to quality

### Strategic Implications
1. **Differentiation Needed**: G06N3/G06N20 space crowded
2. **Niche Opportunities**: G06N7 (probabilistic) and G06N10 (quantum)
3. **Hybrid Value**: Combining multiple subcategories

## Report Structure

### Main Sections
1. **Executive Summary**: Key findings and percentages
2. **IPC Structure**: Table of G06N subcategories
3. **Distribution Analysis**: Overall and detailed classifications
4. **Temporal Trends**: Year-over-year evolution
5. **Technology Deep Dives**: Analysis of each major category
6. **Market Insights**: 2024 signals and patterns
7. **Strategic Implications**: R&D and patent strategy
8. **Conclusions**: 5 key takeaways
9. **Recommendations**: Immediate and strategic actions

### Visualization Panels
1. Stacked area chart showing evolution
2. Pie chart of overall distribution
3. Growth rate comparison lines
4. Technology focus shift percentages
5. Emerging tech bar charts
6. 2024 distribution horizontal bars

## Verification Checklist
- [ ] Total classifications should be ~118,602
- [ ] Patents with G06N should be 72,404
- [ ] G06N3 should be largest at ~42%
- [ ] G06N20 should be second at ~29%
- [ ] All categories should show 2024 decline
- [ ] G06N20/00 should be top detailed classification

## Output Files
1. `g06n_subclassification_analysis.png` - 6-panel visualization
2. `G06N_subclassification_report.md` - English report
3. `G06N_subclassification_report_JP.md` - Japanese report
4. `G06N_subclass_prompt_20250822.md` - This prompt file

## Future Analysis Suggestions
Based on subclassification findings:
1. **Deep dive into G06N3/08** - Learning methods evolution
2. **G06N10 growth analysis** - Quantum computing trajectory
3. **Cross-classification patents** - Hybrid technology analysis
4. **G06N3/04 architecture trends** - CNN/RNN/Transformer evolution
5. **Company specialization** - Which companies focus on which subcategories

## Important Notes
- Classifications format varies: "G06N 3/08" or "G06N3/08"
- Some patents have multiple G06N classifications
- Detailed classifications (e.g., G06N3/08) provide more granularity
- 2024 decline is universal, not limited to specific technologies

---

*Prompt created: August 22, 2025*  
*Building on: August 21, 2025 G06N analysis*  
*Data source: G06N_all.xlsx (72,404 patents, 2014-2024)*  
*Focus: Technology nuances through subclassification analysis*