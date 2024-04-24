import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

file = input('Input filename (excl .csv): ')+".csv"

split = 'Split (GPS)'


with open(file, 'r') as f:
    all_lines = f.readlines()

data_start = 0
for i, line in enumerate(all_lines):
    if line == "Per-Stroke Data:\n":
        data_start = i

all_lines.pop(data_start+3)
relevant_data = all_lines[data_start+2:]
with open('temp.csv', 'w') as f:
    f.write("".join(relevant_data))

data = pd.read_csv('temp.csv')
os.remove('temp.csv')

data[split] = pd.to_timedelta(data[split]) / np.timedelta64(1, 's')
data['Elapsed Time'] = pd.to_timedelta(data['Elapsed Time']).dt.total_seconds()


def format_seconds(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f'{minutes:02d}:{seconds:02d}'


fig, ax = plt.subplots()
ax2 = ax.twinx()

ax.set_ylim(data[split].max(), data[split].min()-10)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: format_seconds(x)))
ax.grid(axis='y')

sns.lineplot(data, ax=ax, x='Elapsed Time', y=split, label='Split', color='C0')
sns.lineplot(data, ax=ax2, x='Elapsed Time', y='Stroke Rate', label='Rate', color='C1')

# Collect handles and labels from both axes
handles, labels = ax.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Combine handles and labels from both axes
handles.extend(handles2)
labels.extend(labels2)
ax.get_legend().remove()
ax2.get_legend().remove()

# Create a unified legend
plt.legend(handles, labels, loc='best')

ax.invert_yaxis()
plt.show()

