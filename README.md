# Task Duration Monitor

This Python application parses a log file (`logs.log`) in CSV format and computes the execution duration of tasks, 
printing warnings or errors based on fixed thresholds (5 minutes and 10 minutes respectively).

## Input File: `logs.log`

The input is a CSV file without headers, where each row represents a task event in the following format:

```text
<timestamp>,<task-description>,<event>,<task-id>
```


- **timestamp**: Task event time in `HH:MM:SS` format (24-hour clock).
- **task-description**: Free text describing the task (ignored by the logic).
- **event**: Either `START` or `END`.
- **task-id**: Numeric ID used to correlate task START and END events.

### Example:

```text
11:35:23,task description A, START,37980
11:40:30,task description A, END,37980
11:45:00,background task B, START,81258
```

---

## How It Works

The script follows a simple and efficient algorithm:

1. **Parse each line** of the CSV log file.
2. **On START**: Store the timestamp in a dictionary, keyed by `task-id`.
3. **On END**:
   - Look up the matching START time.
   - Compute `duration = END - START`.
   - Based on the duration:
     - If > 10 minutes → log as `ERROR`.
     - If > 5 minutes → log as `WARNING`.
   - Remove the task from memory.
4. **If an END has no matching START**, log an `ERROR`.

---

## Example Output

```text
WARNING: Task ID 37980 duration: 0:05:07
ERROR: Task ID 38200 took too long: 0:10:42
ERROR: END event found for Task ID 38201 with no corresponding START event!
```

---

## Running the Script

Make sure your `logs.log` file is in the same directory, then run:

```bash
python main.py
```