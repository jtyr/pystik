#!/usr/bin/python2

import pygame
import pygame.midi as pymidi
import pygame.mixer as pymix
import signal
import sys


def handler(signal, frame):
    try:
        # Close and quit everything on CTRL+C
        midi.close()
        pymidi.quit()
        pymix.quit()
        pygame.quit()
    except Exception:
        pass

    sys.exit(0)


def check_chord(press, play, press_d, play_d):
    press_ret = True
    play_ret = True

    # Compare the pressed and played strings with the chord layout
    for i, string in enumerate(('e', 'B', 'G', 'D', 'A', 'E')):
        if press[string] != press_d[i]:
            press_ret = False

        if (
            play[string] is None and play_d[i] == 1 or
            play[string] is not None and play_d[i] == 0
        ):
            play_ret = False

    return press_ret & play_ret


def print_guitar(msg, press, play):
    print "\n" * 2
    print "Message:   %s" % msg

    sys.stdout.write("Pressed:   ")

    # Print the fret vector
    for string in ('e', 'B', 'G', 'D', 'A', 'E'):
        sys.stdout.write(str(press[string]))

        if string != 'E':
            sys.stdout.write(', ')
        else:
            print ""

    sys.stdout.write("Strumming: ")

    # Print the strumming vector
    for string in ('e', 'B', 'G', 'D', 'A', 'E'):
        sys.stdout.write('0' if play[string] is None else '1')

        if string != 'E':
            sys.stdout.write(', ')
        else:
            print ""

    # Detect some basic chords
    chord = '?'
    if check_chord(press, play, (0, 2, 2, 2, 0, 0), (1, 1, 1, 1, 1, 0)):
        chord = "A"
    elif check_chord(press, play, (0, 1, 2, 2, 0, 0), (1, 1, 1, 1, 1, 0)):
        chord = "Am"
    elif check_chord(press, play, (0, 2, 0, 2, 0, 0), (1, 1, 1, 1, 1, 0)):
        chord = "A7"
    elif check_chord(press, play, (0, 1, 0, 2, 3, 0), (1, 1, 1, 1, 1, 0)):
        chord = "C"
    elif check_chord(press, play, (0, 1, 0, 2, 3, 0), (1, 1, 1, 1, 1, 1)):
        chord = "C/E"
    elif check_chord(press, play, (2, 3, 2, 0, 0, 0), (1, 1, 1, 1, 0, 0)):
        chord = "D"
    elif check_chord(press, play, (1, 3, 2, 0, 0, 0), (1, 1, 1, 1, 0, 0)):
        chord = "Dm"
    elif check_chord(press, play, (0, 0, 1, 2, 2, 0), (1, 1, 1, 1, 1, 1)):
        chord = "E"
    elif check_chord(press, play, (0, 0, 0, 2, 2, 0), (1, 1, 1, 1, 1, 1)):
        chord = "Em"
    elif check_chord(press, play, (1, 1, 2, 3, 0, 0), (1, 1, 1, 1, 1, 0)):
        chord = "F"
    elif check_chord(press, play, (3, 0, 0, 0, 2, 3), (1, 1, 1, 1, 1, 1)):
        chord = "G"
    elif check_chord(press, play, (1, 0, 0, 0, 2, 3), (1, 1, 1, 1, 1, 1)):
        chord = "G7"

    print "Chord:     %s" % chord

    # Build the fretboard visualization
    for string in ('e', 'B', 'G', 'D', 'A', 'E'):
        # Indicate which string was played
        if play[string] is None:
            sys.stdout.write("x %s|" % string)
        else:
            sys.stdout.write("o %s|" % string)

        # Fret part
        for fret in range(1, 6):
            if press[string] == fret:
                sys.stdout.write("--X--|")
            else:
                sys.stdout.write("-----|")

        # Strumming part
        if play[string] is None:
            print "---------------------|"
        else:
            print "----------X----------|"

    print ""


def mute_string(string, sound):
    for n in range(6):
        # Stop the playback
        sound['%s%d' % (string, n)].stop()


def play_note(string, press, sound):
    sound['%s%d' % (string, press[string])].play()


def read_msg(msg, press, play, sound):
    # Freting
    if msg[0] == 176 and msg[1] == 105:
        press['e'] = msg[2] - 64
        play['e'] = None
    elif msg[0] == 177 and msg[1] == 106:
        press['B'] = msg[2] - 59
        play['B'] = None
    elif msg[0] == 178 and msg[1] == 107:
        press['G'] = msg[2] - 55
        play['G'] = None
    elif msg[0] == 179 and msg[1] == 108:
        press['D'] = msg[2] - 50
        play['D'] = None
    elif msg[0] == 180 and msg[1] == 109:
        press['A'] = msg[2] - 45
        play['A'] = None
    elif msg[0] == 181 and msg[1] == 110:
        press['E'] = msg[2] - 40
        play['E'] = None
    # Strumming
    elif msg[0] == 144:
        play['e'] = msg[1] - 64
        mute_string('e', sound)
        play_note('e', press, sound)
    elif msg[0] == 145:
        play['B'] = msg[1] - 59
        mute_string('B', sound)
        play_note('B', press, sound)
    elif msg[0] == 146:
        play['G'] = msg[1] - 55
        mute_string('G', sound)
        play_note('G', press, sound)
    elif msg[0] == 147:
        play['D'] = msg[1] - 50
        mute_string('D', sound)
        play_note('D', press, sound)
    elif msg[0] == 148:
        play['A'] = msg[1] - 45
        mute_string('A', sound)
        play_note('A', press, sound)
    elif msg[0] == 149:
        play['E'] = msg[1] - 40
        mute_string('E', sound)
        play_note('E', press, sound)
    # Play stop events
    elif msg[0] == 128:
        play['e'] = None
        mute_string('e', sound)
    elif msg[0] == 129:
        play['B'] = None
        mute_string('B', sound)
    elif msg[0] == 130:
        play['G'] = None
        mute_string('G', sound)
    elif msg[0] == 131:
        play['D'] = None
        mute_string('D', sound)
    elif msg[0] == 132:
        play['A'] = None
        mute_string('A', sound)
    elif msg[0] == 133:
        play['E'] = None
        mute_string('E', sound)
    # Stop button
    elif msg[0] == 176 and msg[1] == 18 and msg[2] == 127:
        # Stop playing
        play = {
            'e': None,
            'B': None,
            'G': None,
            'D': None,
            'A': None,
            'E': None
        }


def main():
    # Catch CTRL+C
    signal.signal(signal.SIGINT, handler)

    # Initiate the MIDI and mixed interface
    pymidi.init()
    pymix.init()

    print "List of all MIDI devices:"

    # Get the list of all MIDI devices
    for i in range(pymidi.get_count()):
        dev = pymidi.get_device_info(i)

        if dev[2] == 1:
            print "%2d: %s - %s" % (i, dev[0], dev[1])

    # Let the user choose which one to play
    idx = raw_input("Please select your device: ")
    global midi

    # Try to open the selected device
    try:
        midi = pymidi.Input(int(idx))
    except Exception:
        print "Can not open device %s!" % idx
        sys.exit(1)

    # Initiate pressed and played strings
    press = {'e': 0, 'B': 0, 'G': 0, 'D': 0, 'A': 0, 'E': 0}
    play = {
        'e': None,
        'B': None,
        'G': None,
        'D': None,
        'A': None,
        'E': None
    }

    # Load all sounds to make them ready for playback
    sound = {}
    for string in ('e', 'B', 'G', 'D', 'A', 'E'):
        for fret in range(6):
            note = "%s%d" % (string, fret)
            sound[note] = pymix.Sound('sounds/%s.ogg' % note)

    # Print empty layout
    print_guitar(None, press, play)

    while True:
        if midi.poll():
            # Load as many messages as possible
            msgs = midi.read(100)

            # Walk through all messages and set press/play variables
            for m in msgs:
                msg = m[0]

                read_msg(msg, press, play, sound)

            # Print out the layout and play sounds
            print_guitar(msg, press, play)

        # Wait a bit to not to overload the CPU
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
