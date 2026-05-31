"""
================================================================
SENSOR DATA LOGGER — Live Python Visualiser
Author : Nuhu Usman
GitHub : github.com/nuhu-usman

What this does:
  - Connects to the Arduino over USB (Serial port)
  - Reads temperature, humidity and heat index in real time
  - Plots a live updating chart on your screen
  - Saves all readings to a CSV log file automatically

Requirements:
  pip install pyserial matplotlib

How to run:
  1. Upload sensor_logger.ino to your Arduino first
  2. Connect Arduino to your PC via USB
  3. Run: python visualiser.py
================================================================
"""

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from datetime import datetime
import csv
import os
import sys
import time

BAUD_RATE   = 9600
MAX_POINTS  = 50
LOG_FILE    = "sensor_log.csv"
READ_TIMEOUT = 3

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        return None
    for port in ports:
        desc = port.description.lower()
        if any(kw in desc for kw in ['arduino', 'ch340', 'cp210', 'usb serial', 'usbserial']):
            return port.device
    return ports[0].device

timestamps   = deque(maxlen=MAX_POINTS)
temperatures = deque(maxlen=MAX_POINTS)
humidities   = deque(maxlen=MAX_POINTS)
heat_indexes = deque(maxlen=MAX_POINTS)

def setup_log_file():
    file_exists = os.path.isfile(LOG_FILE)
    log = open(LOG_FILE, 'a', newline='')
    writer = csv.writer(log)
    if not file_exists:
        writer.writerow(['datetime', 'arduino_ms', 'temperature_c', 'humidity_pct', 'heat_index_c'])
        print(f"[LOG] Created new log file: {LOG_FILE}")
    else:
        print(f"[LOG] Appending to existing log file: {LOG_FILE}")
    return log, writer

def parse_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    if line.startswith('timestamp'):
        return None
    parts = line.split(',')
    if len(parts) != 4:
        return None
    try:
        arduino_ms  = int(parts[0])
        temperature = float(parts[1])
        humidity    = float(parts[2])
        heat_index  = float(parts[3])
        return arduino_ms, temperature, humidity, heat_index
    except ValueError:
        return None

def main():
    print("=" * 55)
    print("  SENSOR DATA LOGGER — Nuhu Usman")
    print("  github.com/nuhu-usman/sensor-data-logger")
    print("=" * 55)

    port = find_arduino_port()
    if not port:
        print("\n[ERROR] No serial port found.")
        print("  Make sure your Arduino is plugged in via USB.")
        sys.exit(1)

    print(f"\n[OK] Found port: {port}")
    print(f"[OK] Connecting at {BAUD_RATE} baud...")

    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=READ_TIMEOUT)
        time.sleep(2)
        ser.reset_input_buffer()
        print("[OK] Connected to Arduino!\n")
    except serial.SerialException as e:
        print(f"\n[ERROR] Could not open port {port}: {e}")
        sys.exit(1)

    log_file, log_writer = setup_log_file()
    reading_count = 0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7))
    fig.suptitle('Live Sensor Data — Nuhu Usman | DHT11 Arduino Logger',
                 fontsize=13, fontweight='bold', color='#1B3A6B')
    fig.patch.set_facecolor('#F5F0E8')

    for ax in (ax1, ax2):
        ax.set_facecolor('#FFFFFF')
        ax.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

    line_temp, = ax1.plot([], [], color='#B5451B', linewidth=2.2, label='Temperature (°C)')
    line_heat, = ax1.plot([], [], color='#C9A84C', linewidth=1.5,
                          linestyle='--', label='Heat Index (°C)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.legend(loc='upper left', fontsize=9)

    line_hum,  = ax2.plot([], [], color='#3D6B5E', linewidth=2.2, label='Humidity (%)')
    ax2.set_ylabel('Humidity (%)')
    ax2.set_xlabel('Time')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.set_ylim(0, 100)

    status_text = fig.text(0.02, 0.01, 'Waiting for data...', fontsize=8,
                           color='#888888', fontstyle='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    def update(frame):
        nonlocal reading_count
        try:
            if ser.in_waiting > 0:
                raw = ser.readline().decode('utf-8', errors='ignore')
                parsed = parse_line(raw)
                if parsed:
                    arduino_ms, temp, hum, heat = parsed
                    now = datetime.now().strftime('%H:%M:%S')
                    reading_count += 1

                    timestamps.append(now)
                    temperatures.append(temp)
                    humidities.append(hum)
                    heat_indexes.append(heat)

                    log_writer.writerow([
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        arduino_ms, temp, hum, heat
                    ])
                    log_file.flush()

                    print(f"[{now}] Temp: {temp:.1f}°C  |  Humidity: {hum:.1f}%  |  "
                          f"Heat Index: {heat:.1f}°C  |  Reading #{reading_count}")

                    x = list(range(len(timestamps)))
                    line_temp.set_data(x, list(temperatures))
                    line_heat.set_data(x, list(heat_indexes))
                    line_hum.set_data(x,  list(humidities))

                    for ax in (ax1, ax2):
                        ax.relim()
                        ax.autoscale_view()
                        ax.set_xlim(0, max(MAX_POINTS, len(x)))
                        step = max(1, len(x) // 8)
                        ax.set_xticks(x[::step])
                        ax.set_xticklabels(list(timestamps)[::step], rotation=30, ha='right')

                    status_text.set_text(
                        f'Live  |  Readings: {reading_count}  |  '
                        f'Last: {temp:.1f}°C  {hum:.1f}%  |  Logged to: {LOG_FILE}'
                    )
        except Exception as e:
            status_text.set_text(f'Error: {e}')
        return line_temp, line_heat, line_hum, status_text

    ani = animation.FuncAnimation(fig, update, interval=500,
                                  blit=False, cache_frame_data=False)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n[DONE] Stopped. {reading_count} readings saved to {LOG_FILE}")
        ser.close()
        log_file.close()

if __name__ == '__main__':
    main()
