#!/usr/bin/env python3

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == '__main__':
    # initialize window
    stdkeys.create_window()

    keyboard = "q2we4r5ty7u8i9op-[=]"

    keyL = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']  # Purely for recognizing note input
    notes = [GuitarString(440 * (1.059463**(x-12))) for x in range(len(keyboard))] 

    n_iters = 0
    while True:
        # it turns out that the bottleneck is in polling for key events
        # for every iteration, so we'll do it less often, say every 
        # 1000 or so iterations
        if n_iters == 1000:
            stdkeys.poll()
            n_iters = 0
        n_iters += 1

        # check if the user has typed a key; if so, process it
        if stdkeys.has_next_key_typed():
            key = stdkeys.next_key_typed()
            if key in keyboard:
                notes[keyboard.index(key)].pluck()
                print(keyL[keyboard.index(key) % len(keyL)])

        # compute the sum of samples if the note is pressed
        sample = 0
        sample = sum(note.sample() for note in notes if note.isVibrating)

        # play the sample
        play_sample(sample)

        # advance the simulation of each guitar string by one step if the note was pressed
        for note in notes:
            if note.isVibrating:
                note.tick()