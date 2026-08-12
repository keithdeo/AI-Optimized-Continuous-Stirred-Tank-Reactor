import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

p = Path(__file__).parent / 'reaction_data_copy.csv'

data = pd.read_csv(p)

plt.figure(figsize=(8,6))
plt.scatter(data['Reaction Rate'], data['Conversion A to B'], s=10)
plt.xlabel('Reaction Rate')
plt.ylabel('Conversion A to B')
plt.title('Conversion A to B vs Reaction Rate')
plt.tight_layout()
out = Path(__file__).parent / 'reaction_rate_plot.png'
plt.savefig(out, dpi=150)
print(f"Saved plot to {out}")
