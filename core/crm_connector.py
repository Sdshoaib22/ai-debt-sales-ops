import time
import os
import csv
from datetime import datetime

LOG_FILE = "logs/push_log.csv"

def push_to_crm(leads):
    """
    Simulated CRM API push with logging.
    """

    time.sleep(1)

    # Ensure logs folder exists
    os.makedirs("logs", exist_ok=True)

    # Write log
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        for lead in leads:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                lead.get("first_name"),
                lead.get("last_name"),
                lead.get("priority"),
                lead.get("conversion_score")
            ])

    return {
        "status": "success",
        "pushed_count": len(leads),
        "message": "Leads successfully sent to CRM and logged"
    }
