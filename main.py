import network
import ntptime
import time
from machine import I2C, Pin, RTC
from lcd1602 import LCD

# ================= CONFIGURATION =================
SSID = "LintonTribe8"          # Your WiFi Name
PASSWORD = "Fhandl77"  # Your WiFi Password
UTC_OFFSET_HOURS = -7            # Adjust for your Timezone
# =================================================

# Hardware Setup (Pins 6 and 7 as confirmed working)
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = LCD(i2c)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    lcd.clear()
    lcd.message("Connecting WiFi")
    
    max_wait = 15
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        time.sleep(1)
        
    if wlan.isconnected():
        lcd.clear()
        lcd.message("WiFi Connected")
        time.sleep(1)
    else:
        lcd.clear()
        lcd.message("WiFi Failed!")
        raise RuntimeError("Network failed")

def sync_time():
    try:
        lcd.clear()
        lcd.message("Syncing Time...")
        ntptime.settime() 
    except:
        lcd.clear()
        lcd.message("Sync Failed")
        time.sleep(2)

def update_display(date_str, time_str):
    """Safely updates the display using cursor control or write method"""
    d_row = date_str.center(16)
    t_row = time_str.center(16)
    
    try:
        # Standard method for most libraries
        lcd.setCursor(0, 0)
        lcd.message(d_row)
        lcd.setCursor(0, 1)
        lcd.message(t_row)
    except AttributeError:
        # Fallback if your library uses .write(col, row, text)
        lcd.write(0, 0, d_row)
        lcd.write(0, 1, t_row)

def get_datetime_strings():
    # Calculate local time based on UTC + Offset
    local_seconds = time.time() + (UTC_OFFSET_HOURS * 3600)
    tm = time.localtime(local_seconds)
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Date Format: "Feb 21, 2026"
    date_str = "{} {:02d}, {:04d}".format(months[tm[1]-1], tm[2], tm[0])
    # Time Format: "12:30:45"
    time_str = "{:02d}:{:02d}:{:02d}".format(tm[3], tm[4], tm[5])
    
    return date_str, time_str

# --- Main Run ---
try:
    connect_wifi()
    sync_time()
    lcd.clear()
    
    while True:
        d_text, t_text = get_datetime_strings()
        update_display(d_text, t_text)
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    print("Program stopped")
