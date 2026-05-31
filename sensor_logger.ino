/*
 * ============================================================
 * SENSOR DATA LOGGER — Arduino Sketch
 * Author : Nuhu Usman
 * Board  : Arduino Uno / Nano
 * Sensors: DHT11 (Temperature & Humidity)
 *
 * What this does:
 *   - Reads temperature (°C) and humidity (%) every 2 seconds
 *   - Prints the values over Serial in CSV format
 *   - Python script on the PC reads this data and plots it live
 *
 * Wiring:
 *   DHT11 Pin 1 (VCC)  → Arduino 5V
 *   DHT11 Pin 2 (DATA) → Arduino Digital Pin 2
 *   DHT11 Pin 4 (GND)  → Arduino GND
 *   (Add a 10kΩ pull-up resistor between DATA and VCC)
 * ============================================================
 */

#include <DHT.h>

#define DHT_PIN     2
#define DHT_TYPE    DHT11
#define READ_DELAY  2000

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(9600);
    dht.begin();
    delay(2000);
    Serial.println("timestamp_ms,temperature_c,humidity_pct,heat_index_c");
    Serial.println("# SIWES Sensor Data Logger — Nuhu Usman");
    Serial.println("# Streaming data. Open Python visualiser to see live chart.");
}

void loop() {
    float humidity    = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) {
        Serial.println("# ERROR: Failed to read from DHT sensor. Check wiring.");
        delay(READ_DELAY);
        return;
    }

    float heatIndex = dht.computeHeatIndex(temperature, humidity, false);
    unsigned long timestamp = millis();

    Serial.print(timestamp);
    Serial.print(",");
    Serial.print(temperature, 2);
    Serial.print(",");
    Serial.print(humidity, 2);
    Serial.print(",");
    Serial.println(heatIndex, 2);

    delay(READ_DELAY);
}
