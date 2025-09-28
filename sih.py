import csv
from datetime import datetime, timedelta
from collections import Counter

# CSV file names
SYMPTOM_FILE = "symptom_reports.csv"
SENSOR_FILE = "sensor_readings.csv"

# Safe water thresholds
SAFE_PH_MIN, SAFE_PH_MAX = 6.5, 8.5
TURBIDITY_THRESHOLD = 5.0
TDS_THRESHOLD = 1000.0

# --------- Helpers ---------
def save_symptom(name, village, symptom):
    with open(SYMPTOM_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, village, symptom, datetime.now().isoformat()])
    print(f"✅ Saved symptom: {symptom} from {village}")

def save_sensor(village, pH, turbidity, tds, temp):
    with open(SENSOR_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([village, pH, turbidity, tds, temp, datetime.now().isoformat()])
    print(f"✅ Saved sensor reading for {village}")

def check_water(pH, turbidity, tds):
    reasons = []
    if pH < SAFE_PH_MIN or pH > SAFE_PH_MAX:
        reasons.append(f"pH out of range ({pH})")
    if turbidity > TURBIDITY_THRESHOLD:
        reasons.append(f"High turbidity ({turbidity})")
    if tds > TDS_THRESHOLD:
        reasons.append(f"High TDS ({tds})")
    return reasons

def check_outbreak(hours=24, threshold=5):
    try:
        with open(SYMPTOM_FILE, "r") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        return {}

    now = datetime.now()
    start = now - timedelta(hours=hours)
    counts = Counter()
    for row in rows:
        _, village, symptom, ts = row
        if datetime.fromisoformat(ts) >= start:
            counts[village] += 1

    return {v: (c, c >= threshold) for v, c in counts.items()}

# --------- Demo Menu ---------
while True:
    print("\n--- Smart Health Monitoring ---")
    print("1. Report Symptom")
    print("2. Add Sensor Data")
    print("3. Check Alerts")
    print("4. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        name = input("Name: ")
        village = input("Village: ")
        symptom = input("Symptom: ")
        save_symptom(name, village, symptom)

    elif choice == "2":
        village = input("Village: ")
        pH = float(input("pH: "))
        turb = float(input("Turbidity: "))
        tds = float(input("TDS: "))
        temp = float(input("Temperature: "))
        save_sensor(village, pH, turb, tds, temp)
        reasons = check_water(pH, turb, tds)
        if reasons:
            print(f"⚠️ Water Unsafe: {', '.join(reasons)}")
        else:
            print("✅ Water Safe")

    elif choice == "3":
        outbreaks = check_outbreak()
        if not outbreaks:
            print("No reports yet.")
        else:
            for v, (cnt, flagged) in outbreaks.items():
                if flagged:
                    print(f"⚠️ Outbreak Alert in {v}: {cnt} cases in last 24h")
                else:
                    print(f"{v}: {cnt} cases (normal)")

    elif choice == "4":
        break

    else:
        print("Invalid option")
