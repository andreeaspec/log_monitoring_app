import logging
from datetime import datetime, timedelta
import csv

LOG_FILENAME = "logs.log"
START_EVENT = "START"
END_EVENT = "END"

# Thresholds used to trigger the alerts
warning_threshold = timedelta(minutes=5)
error_threshold = timedelta(minutes=10)


# Function to parse time in HH:MM:SS format
def parse_time(t):
    return datetime.strptime(t.strip('"'), "%H:%M:%S")


'''
    This application parses a CSV logs file (logs.log) in this format:
        <timestamp>,<task-description>,<event>,<task-id>
        11:35:23,task description 1, START,37980
        11:37:23,task description 2, END,37984
        (...)
    Then it computes the duration of each task, by grouping the entries by <task-id> in a dictionary.
    We only keep the START time for each event in the dictionary, and as soon as we encounter the END event
    we just compute the duration (END - START) without storing the END timestamp.
     -> For tasks taking more than 5 minutes => WARN
     -> For tasks taking more than 10 minutes => ERROR
'''


def main():
    # Dictionary to hold START time per task ID
    start_times = {}

    # Configure application logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Read the CSV file and parse it
    with open(LOG_FILENAME, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for csv_row in reader:
            if len(csv_row) != 4:
                continue  # skip malformed rows
            timestamp, description, event, taskid = [item.strip() for item in csv_row]
            time_obj = parse_time(timestamp)

            if START_EVENT == event:
                start_times[taskid] = time_obj
            elif END_EVENT == event:
                if taskid in start_times:
                    duration = time_obj - start_times[taskid]
                    if duration > error_threshold:
                        logging.error(f"Task ID {taskid} took too long: {duration}")
                    elif duration > warning_threshold:
                        logging.warning(f"Task ID {taskid} duration: {duration}")

                    # Delete the start time to free memory
                    del start_times[taskid]
                else:
                    logging.error(f"END event found for Task ID {taskid} with no corresponding START event!")


if __name__ == "__main__":
    main()
