import pigpio
import time
import random

PIN = 18
pi = pigpio.pi()
VOLUME = 15000

def sound_shutdown():
    notes = [(1046, 0.1), (784, 0.1), (659, 0.2)]
    for freq, dur in notes:
        pi.hardware_PWM(PIN, int(freq), VOLUME)
        time.sleep(dur)

def sound_off_retro():
    for f in range(800, 400, -40):
        pi.hardware_PWM(PIN, f, VOLUME)
        time.sleep(0.03)

def sound_goodbye():
    notes = [(659, 0.2), (523, 0.4)]
    for freq, dur in notes:
        pi.hardware_PWM(PIN, int(freq), VOLUME)
        time.sleep(dur)

if pi.connected:
    final_sounds = [sound_shutdown, sound_off_retro, sound_goodbye]
    random.choice(final_sounds)()
    pi.hardware_PWM(PIN, 0, 0)
    pi.stop()