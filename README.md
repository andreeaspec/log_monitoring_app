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

## Output after running the program for the sample logs.log file

```text
ERROR: Task ID 39547 duration: 0:11:29
ERROR: Task ID 45135 duration: 0:12:23
WARNING: Task ID 71766 duration: 0:05:47
ERROR: Task ID 81258 duration: 0:14:46
WARNING: Task ID 87228 duration: 0:09:28
WARNING: Task ID 50295 duration: 0:06:35
WARNING: Task ID 27222 duration: 0:06:08
WARNING: Task ID 87570 duration: 0:07:53
WARNING: Task ID 99672 duration: 0:05:13
WARNING: Task ID 86716 duration: 0:05:34
ERROR: Task ID 22003 duration: 0:11:13
ERROR: Task ID 85742 duration: 0:12:17
WARNING: Task ID 98746 duration: 0:07:17
ERROR: Task ID 39860 duration: 0:19:52
ERROR: Task ID 52532 duration: 0:13:53
ERROR: Task ID 62401 duration: 0:10:24
ERROR: Task ID 23703 duration: 0:13:26
ERROR: Task ID 70808 duration: 0:33:43
WARNING: Task ID 24482 duration: 0:08:36

Process finished with exit code 0
```

## Running the Script

Make sure your `logs.log` file is in the same directory, then run:

```bash
python main.py
```