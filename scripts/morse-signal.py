import numpy as np
import simpleaudio as sa
import argparse



FS = 44100
FREQ = 440
DIT = 60/1000

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}


def text2Morse(text):
    text = text.upper()
    words = text.split()

    return "       ".join(["   ".join([" ".join(MORSE_CODE_DICT[l]) for l in word]) for word in words])

    # return [" ".join(MORSE_CODE_DICT[l]) for l in text]

def makeBeep(
    seconds,
    frequency = FREQ,
    fs = FS
):
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, round(seconds * fs), False)

    # Generate a 440 Hz sine wave
    note = np.sin(frequency * t * 2 * np.pi)

    # Ensure that highest value is in 16-bit range
    audio = (note) * (2**15 - 1) / np.max(np.abs(note))
    return(audio)

def makeSilence(
    seconds,
    fs = FS
):
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, seconds, round(seconds * fs), False)

    audio = t * 0
    return(audio)


def symbol2Sound(
    symb,
    frequency = FREQ,
    fs = FS,
    dit = DIT
):
    if symb == '.':
        return makeBeep(dit,frequency,fs)
    elif symb == '-':
        return makeBeep(3*dit,frequency,fs)
    elif symb == ' ':
        return makeSilence(dit,fs)
    #TODO raise error for other characters

def checkMorse():
    pass

def morse2Signal(
    morse,
    frequency = FREQ,
    fs = FS,
    dit = DIT
):

    audio_list = [symbol2Sound(s,frequency,fs,dit) for s in morse]
    audio = np.concatenate(audio_list)

    return(audio)
    # Our played note will be 440 Hz
    


if __name__ == "__main__":


    fs = FS


    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-m', action='store', type=str)
    my_parser.add_argument('-t', action='store', type=str)

    args = my_parser.parse_args()


    if args.t is not None:
        text = args.t
        # message = " ".join(args.m)
        message = text2Morse(text)
        print(message)
        audio = morse2Signal(message)

    elif args.m is not None:

        message = args.m
        message = " ".join(message)

        audio = morse2Signal(message)

    else:
        audio = makeBeep(1)

    # Convert to 16-bit data
    audio = audio.astype(np.int16)

    # Start playback
    play_obj = sa.play_buffer(audio, 1, 2, fs)

    # Wait for playback to finish before exiting
    play_obj.wait_done()