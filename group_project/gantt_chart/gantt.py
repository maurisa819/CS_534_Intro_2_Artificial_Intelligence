import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Define tasks
tasks = [
    "Divide raw data\ninto train, test,\nand validation",
    "DistilBERT for\ndata cleaning\n(and compare\nwith TD-IDF)",
    "Implement Random\nForest, XGBoost,\nand MLP models",
    "Train, test,\nand validate models\nusing distilled data",
    "Evaluate model\nfitness & performance"
]

# Start and end dates
start_date = datetime(2025, 6, 16)
end_date = datetime(2025, 8, 3)
total_days = (end_date - start_date).days

num_tasks = len(tasks)

# Compute start and end dates for each task evenly
task_intervals = []
for i in range(num_tasks):
    task_start = start_date + timedelta(days=int(i * total_days / num_tasks))
    task_end = start_date + timedelta(days=int((i + 1) * total_days / num_tasks))
    task_intervals.append((task_start, task_end))

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))

# Convert dates and plot bars
for i, (task, interval) in enumerate(zip(tasks, task_intervals)):
    start_num = mdates.date2num(interval[0])
    end_num = mdates.date2num(interval[1])
    ax.barh(i, end_num - start_num, left=start_num, height=0.4, align='center')

# Format y-axis
ax.set_yticks(range(num_tasks))
ax.set_yticklabels(tasks)
ax.invert_yaxis()  # Highest task at top

# Format x-axis for dates
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.title("Group ProjectAI and ML Solutions to Phishing Detection")
plt.xlabel("Date")
plt.tight_layout()
plt.show()
