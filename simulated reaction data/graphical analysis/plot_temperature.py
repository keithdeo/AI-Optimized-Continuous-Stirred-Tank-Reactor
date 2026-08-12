import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

p = Path(__file__).parent / 'reaction_data_copy.csv'

data = pd.read_csv(p)

plt.figure(figsize=(8,6))
plt.scatter(data['Temperature (K)'], data['Conversion A to B'])
plt.xlabel('Temperature (K)')
plt.ylabel('Conversion A to B')
plt.title('Conversion A to B vs Temperature')
plt.tight_layout()
out = Path(__file__).parent / 'reaction_plot.png'
plt.savefig(out)
print(f"Saved plot to {out}")
