#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pigpio
import time
import sys
import argparse

PIN = 18
VOLUME = 15000          
SILENCE_BETWEEN_NOTES = 0.05

def play_notes(pi, notes, pause_between=0.05):
    for freq, dur in notes:
        if freq == 0:
            time.sleep(dur)
        else:
            pi.hardware_PWM(PIN, int(freq), VOLUME)
            time.sleep(dur)
            pi.hardware_PWM(PIN, 0, 0)
            time.sleep(pause_between)
    pi.hardware_PWM(PIN, 0, 0)

def play_sweep(pi, start_freq, end_freq, step, step_duration):
    if start_freq > end_freq:
        step = -abs(step)
    else:
        step = abs(step)
    for f in range(start_freq, end_freq, step):
        pi.hardware_PWM(PIN, f, VOLUME)
        time.sleep(step_duration)
    pi.hardware_PWM(PIN, 0, 0)

def play_siren(pi, base_freq, cycles=4, offset=200):
    for _ in range(cycles):
        pi.hardware_PWM(PIN, base_freq, VOLUME)
        time.sleep(0.4)
        pi.hardware_PWM(PIN, max(100, base_freq - offset), VOLUME)
        time.sleep(0.4)
    pi.hardware_PWM(PIN, 0, 0)

def melody_happy_boot(pi):
    play_notes(pi, [(523, 0.1), (659, 0.15)])

def melody_apple_retro(pi):
    play_notes(pi, [(440, 0.1), (880, 0.2)])

def melody_scifi_ready(pi):
    play_notes(pi, [(600, 0.05), (800, 0.05), (1200, 0.1)])

def melody_gameboy_arpeggio(pi):
    play_notes(pi, [(523, 0.08), (659, 0.08), (784, 0.08), (1046, 0.15)])

def melody_bios_post_ok(pi):
    play_notes(pi, [(800, 0.2)])

def melody_bios_ram_error(pi):
    for _ in range(3):
        play_notes(pi, [(800, 0.6)])

def melody_bios_video_error(pi):
    play_notes(pi, [(800, 0.6)])
    time.sleep(0.1)
    play_notes(pi, [(800, 0.2)])
    play_notes(pi, [(800, 0.2)])

def melody_bios_motherboard(pi):
    for _ in range(9):
        play_notes(pi, [(800, 0.15)])
        time.sleep(0.05)

def melody_bios_siren(pi):
    play_siren(pi, 800, cycles=4, offset=200)

def melody_shutdown_descending(pi):
    play_notes(pi, [(1046, 0.1), (784, 0.1), (659, 0.2)])

def melody_shutdown_sweep(pi):
    play_sweep(pi, 800, 400, -40, 0.03)

def melody_shutdown_goodbye(pi):
    play_notes(pi, [(659, 0.2), (523, 0.4)])

def melody_sound_ready(pi):
    play_notes(pi, [(523, 0.1), (659, 0.15)], pause_between=0)
    time.sleep(2)
    play_notes(pi, [(659, 0.15), (523, 0.1)], pause_between=0)

def melody_still_alive(pi):
    notes = [
        (1568, 0.2), (1397, 0.2), (1319, 0.2), (1319, 0.2), (1397, 0.4),
        (0, 0.2),
        (1568, 0.2), (1397, 0.2), (1319, 0.2), (1319, 0.2), (1397, 0.4),
        (1175, 0.4), (0, 0.1),
        (880, 0.2), (880, 0.2), (1319, 0.4),
        (1175, 0.2), (1047, 0.2), (1047, 0.2), (1175, 0.2), (1319, 0.4),
        (0, 0.1),
        (880, 0.2), (880, 0.2), (1319, 0.4)
    ]
    play_notes(pi, notes, pause_between=0.02)

MELODIES = [
    ("Happy Boot (C5->E5)", melody_happy_boot),
    ("Apple Retro (A4->A5)", melody_apple_retro),
    ("Sci-Fi Ready (fast rise)", melody_scifi_ready),
    ("Gameboy Arpeggio", melody_gameboy_arpeggio),
    ("BIOS POST OK (1 beep)", melody_bios_post_ok),
    ("BIOS RAM Error (3 long)", melody_bios_ram_error),
    ("BIOS Video Error (1 long + 2 short)", melody_bios_video_error),
    ("BIOS Motherboard Error (9 short)", melody_bios_motherboard),
    ("BIOS Emergency Siren", melody_bios_siren),
    ("Shutdown descending (C6->G5->E5)", melody_shutdown_descending),
    ("Shutdown retro sweep (800->400 Hz)", melody_shutdown_sweep),
    ("Shutdown Goodbye (E5->C5)", melody_shutdown_goodbye),
    ("Special Ready Sound", melody_sound_ready),
    ("Still Alive (Portal)", melody_still_alive),
]

def list_melodies():
    print("Available melodies:")
    for idx, (name, _) in enumerate(MELODIES, start=1):
        print("  %2d. %s" % (idx, name))

def play_melody(pi, index):
    if 1 <= index <= len(MELODIES):
        name, func = MELODIES[index-1]
        print(">> Playing: %s" % name)
        func(pi)
        print(">> Playback finished.")
    else:
        print(">> ERROR: Invalid index %d. Use -l to see options." % index)
        sys.exit(1)

def play_all(pi):
    print("\n>> Playing all melodies in sequence...\n")
    for idx, (name, func) in enumerate(MELODIES, start=1):
        print(">> %d. %s" % (idx, name))
        func(pi)
        time.sleep(0.5)
    print("\n>> Test completed!")

def show_menu():
    print("\n" + "=" * 55)
    print("   MELODY PLAYER FOR RASPBERRY PI (PWM)")
    print("=" * 55)
    for idx, (name, _) in enumerate(MELODIES, start=1):
        print("%2d. %s" % (idx, name))
    print(" 0. Exit")
    print(" T. Test all melodies in sequence")
    print("=" * 55)

def interactive_mode(pi):
    try:
        while True:
            show_menu()
            option = input("Select an option: ").strip().upper()
            if option == "0":
                break
            elif option == "T":
                play_all(pi)
            else:
                try:
                    idx = int(option) - 1
                    if 0 <= idx < len(MELODIES):
                        name, func = MELODIES[idx]
                        print("\n>> Playing: %s" % name)
                        func(pi)
                        print(">> Playback finished.")
                    else:
                        print(">> Invalid option. Use a number from 1 to %d or T." % len(MELODIES))
                except ValueError:
                    print(">> Invalid input.")
    except KeyboardInterrupt:
        print("\n>> Interruption received. Exiting...")

def main():
    parser = argparse.ArgumentParser(
        description="Melody player for Raspberry Pi using PWM (pigpio)."
    )
    parser.add_argument("-t", "--test-all", action="store_true",
                        help="Plays all melodies in sequence.")
    parser.add_argument("-l", "--list", action="store_true",
                        help="Lists available melodies with their numbers.")
    parser.add_argument("-p", "--play", type=int, metavar="N",
                        help="Plays melody number N (use -l to see list).")
    args = parser.parse_args()

    pi = pigpio.pi()
    if not pi.connected:
        print("ERROR: Could not connect to the pigpio daemon.")
        print("Make sure to run 'sudo pigpiod' before executing this script.")
        sys.exit(1)
    print("Connection with pigpio established.")

    try:
        if args.list:
            list_melodies()
        elif args.play is not None:
            play_melody(pi, args.play)
        elif args.test_all:
            play_all(pi)
        else:
            interactive_mode(pi)
    finally:
        pi.hardware_PWM(PIN, 0, 0)
        pi.stop()
        print("Pigpio connection closed. Goodbye.")

if __name__ == "__main__":
    main()