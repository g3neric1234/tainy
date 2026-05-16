# Tainy |:]

Scripts for the Raspberry Pi Model B Plus Rev 1.2.

## Overview

This repository contains a small collection of my scripts designed for my Raspberry Pi (i named him "Tainy" lol) to:

* Play retro-inspired startup and shutdown sounds
* Simulate classic BIOS beep codes
* Generate PWM melodies using a passive buzzer
* Send boot notifications to Telegram
* Test and preview multiple sound effects interactively

`all.py`, `startup.py` and `shutdown.py` uses the `pigpio` daemon for hardware PWM generation on GPIO 18.

---

## Scripts

### `all.py`

Main interactive melody player and testing utility.

Includes:

* Happy boot sounds
* Apple-style retro tones
* Sci-Fi startup effects
* Gameboy arpeggios
* BIOS POST beep codes
* Emergency siren simulation
* Shutdown sounds
* "Still Alive" melody from Portal

Functions available:

* Interactive terminal menu
* Play a specific melody
* List all melodies
* Test all sounds sequentially

Example:

```bash
python3 all.py
```

List melodies:

```bash
python3 all.py -l
```

Play a specific melody:

```bash
python3 all.py -p 4
```

Test every melody:

```bash
python3 all.py -t
```

---

### `startup.py`

Boot notification and startup sound script.

Features:

  * Waits for internet connectivity
  * Retrieves:
  * Local IP
  * Public IP
  * Connected WiFi SSID
  * Current startup time
  * Sends a formatted Telegram notification
  * Plays a retro Gameboy-style startup melody

---

### `shutdown.py`

Shutdown sound effect script.

Randomly plays one of several shutdown melodies:

* Descending shutdown tone
* Retro frequency sweep
* Goodbye melody

Designed to run automatically during system shutdown.

---

## Requirements

```bash
sudo apt update
sudo apt install python3-pip pigpio
pip3 install pigpio requests pytz
```

Start the pigpio daemon:

```bash
sudo pigpiod
```

---

## Autostart

```bash
sudo nano /etc/systemd/system/tainy-startup.service
```

Code:

```ini
[Unit]
Description=Tainy Startup Script
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/tainy/startup.py
Restart=no

[Install]
WantedBy=multi-user.target
```

Enable service:

```bash
sudo systemctl enable tainy-startup.service
```

---

## License

MIT License

---
