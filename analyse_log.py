"""
================================================================
SENSOR DATA LOGGER — Log Analyser
Author : Nuhu Usman

What this does:
  - Reads the saved sensor_log.csv file
  - Prints a statistical summary (min, max, average)
  - Generates a clean summary chart saved as PNG

Run after collecting data with visualiser.py:
  python analyse_log.py
================================================================
"""

import csv
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

LOG_FILE = "sensor_log.csv"

def load_log():
    if not os.path.isfile(LOG_FILE):
        print(f"[ERROR] Log file '{LOG_FILE}' not found.")
        print("  Run visualiser.py first to collect some data.")
        sys.exit(1)

    datetimes, temperatures, humidities, heat_indexes = [], [], [], []

    with open(LOG_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                datetimes.append(datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S'))
                temperatures.append(float(row['temperature_c']))
                humidities.append(float(row['humidity_pct']))
                heat_indexes.append(float(row['heat_index_c']))
            except (ValueError, KeyError):
                continue

    return datetimes, temperatures, humidities, heat_indexes

def print_summary(temperatures, humidities, heat_indexes):
    print("\n" + "=" * 50)
    print("  SENSOR LOG SUMMARY — Nuhu Usman")
    print("=" * 50)
    print(f"  Total Readings   : {len(temperatures)}")
    print()
    print(f"  Temperature (°C)")
    print(f"    Minimum  : {min(temperatures):.2f}°C")
    print(f"    Maximum  : {max(temperatures):.2f}°C")
    print(f"    Average  : {sum(temperatures)/len(temperatures):.2f}°C")
    print()
    print(f"  Humidity (%)")
    print(f"    Minimum  : {min(humidities):.2f}%")
    print(f"    Maximum  : {max(humidities):.2f}%")
    print(f"    Average  : {sum(humidities)/len(humidities):.2f}%")
    print()
    print(f"  Heat Index (°C)")
    print(f"    Minimum  : {min(heat_indexes):.2f}°C")
    print(f"    Maximum  : {max(heat_indexes):.2f}°C")
    print(f"    Average  : {sum(heat_indexes)/len(heat_indexes):.2f}°C")
    print("=" * 50 + "\n")

def plot_summary(datetimes, temperatures, humidities, heat_indexes):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    fig.suptitle('Sensor Data Log Summary — Nuhu Usman',
                 fontsize=13, fontweight='bold', color='#1B3A6B')
    fig.patch.set_facecolor('#F5F0E8')

    for ax in (ax1, ax2):
        ax.set_facecolor('#FFFFFF')
        ax.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

    ax1.plot(datetimes, temperatures, color='#B5451B', linewidth=2, label='Temperature (°C)')
    ax1.plot(datetimes, heat_indexes, color='#C9A84C', linewidth=1.5,
             linestyle='--', label='Heat Index (°C)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.fill_between(datetimes, temperatures, alpha=0.08, color='#B5451B')

    ax2.plot(datetimes, humidities, color='#3D6B5E', linewidth=2, label='Humidity (%)')
    ax2.set_ylabel('Humidity (%)')
    ax2.set_xlabel('Time')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.fill_between(datetimes, humidities, alpha=0.08, color='#3D6B5E')
    ax2.set_ylim(0, 100)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()

    plt.tight_layout()
    output = "sensor_summary_chart.png"
    plt.savefig(output, dpi=150, bbox_inches='tight')
    print(f"[OK] Summary chart saved to: {output}")
    plt.show()

def main():
    print("Loading log file...")
    datetimes, temperatures, humidities, heat_indexes = load_log()

    if not temperatures:
        print("[ERROR] No valid data found in log file.")
        sys.exit(1)

    print_summary(temperatures, humidities, heat_indexes)
    plot_summary(datetimes, temperatures, humidities, heat_indexes)

if __name__ == '__main__':
    main()
