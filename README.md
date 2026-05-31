# 📡 Sensor Data Logger

An embedded systems project that reads real-time temperature and humidity from a DHT11 sensor via Arduino, streams the data over USB serial communication to a PC, and visualises it live using Python and Matplotlib.

Built by **Nuhu Usman** as part of the NNPC Offshore Lab Embedded Systems & Data Science Training Programme at Sa'adu Zungur University Bauchi.

---

## 🧠 How It Works
[DHT11 Sensor]
|
| (reads temp & humidity every 2 seconds)
↓
[Arduino Uno]
|
| (sends CSV data over USB Serial at 9600 baud)
↓
[Your PC — Python]
|
├── visualiser.py     → Live chart on screen
├── sensor_log.csv    → Auto-saved data log
└── analyse_log.py    → Summary stats + chart
---

## 🛒 Hardware Required

| Component | Quantity |
|-----------|----------|
| Arduino Uno or Nano | 1 |
| DHT11 Temperature & Humidity Sensor | 1 |
| 10kΩ Resistor | 1 |
| Breadboard | 1 |
| Jumper Wires | 3 |
| USB Cable | 1 |

---

## 🔌 Wiring
DHT11 Pin 1 (VCC)  → Arduino 5V
DHT11 Pin 2 (DATA) → Arduino Digital Pin 2
DHT11 Pin 4 (GND)  → Arduino GND
Connect a 10kΩ resistor between DATA and VCC
---

## 🛠️ Setup

### Step 1 — Install Arduino Library
1. Open Arduino IDE
2. Go to Sketch → Include Library → Manage Libraries
3. Search for **DHT sensor library** by Adafruit and install it

### Step 2 — Upload Arduino Sketch
1. Open `sensor_logger.ino` in Arduino IDE
2. Connect Arduino via USB
3. Select your board and port under Tools
4. Click Upload

### Step 3 — Install Python Dependencies
pip install -r requirements.txt
### Step 4 — Run the Live Visualiser
python visualiser.py
---

## 📊 Analyse Saved Data

After collecting data, run:
python analyse_log.py
Code
Prints min, max, and average for temperature and humidity, and saves a chart as PNG.

---

## 🗂️ File Structure
sensor-data-logger/
├── sensor_logger.ino    # Arduino sketch
├── visualiser.py        # Live Python chart
├── analyse_log.py       # Log analysis and stats
├── requirements.txt     # Python dependencies
└── README.md
---

## 👤 Author

**Nuhu Usman** — Computer Science Graduate, BASUG 2025
- GitHub: [@nuhu-usman](https://github.com/nuhu-usman)
- LinkedIn: [linkedin.com/in/nuhu-usman](https://www.linkedin.com/in/nuhu-usman)
- Email: nuhuusman241@gmail.com
