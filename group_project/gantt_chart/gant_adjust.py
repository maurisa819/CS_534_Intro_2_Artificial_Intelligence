import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Task definitions
tasks = [
    "1. Split raw data\ninto train/test\n/validation",
    "2. DistilBERT cleaning\n(and TD-IDF compare)",
    "3. Implement RF,\nXGBoost, MLP",
    "4. Train/test/validate\nusing distilled data",
    "5. Evaluate model\nfitness & perf"
]

# Project bounds
start = datetime(2025, 6, 16)
end = datetime(2025, 8, 3)
total_days = (end - start).days  # 48 days

# Allocations (as fractions of total_days)
fractions = [0.15, 0.55, 0.25, 0.07, 0.03]

# Compute intervals
intervals = []
cursor = start
for frac in fractions:
    duration = timedelta(days=total_days * frac)
    intervals.append((cursor, cursor + duration))
    cursor += duration

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
for i, (task, (s, e)) in enumerate(zip(tasks, intervals)):
    ax.barh(i, mdates.date2num(e) - mdates.date2num(s),
            left=mdates.date2num(s), height=0.4)

# Formatting
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels(tasks)
ax.invert_yaxis()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
plt.title("Adjusted Gantt Chart (June 16 – Aug 3 2025)")
plt.xlabel("Date")
plt.tight_layout()
plt.show()
