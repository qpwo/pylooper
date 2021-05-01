from argparse import ArgumentParser
import os
from pathlib import Path

import pygame

from getch import getch
from record import record

wav_dir = os.path.join(os.getcwd(), "wav")
parser = ArgumentParser()
parser.add_argument(
    "-d",
    type=Path,
    default=wav_dir,
    help="Path to directory to save and load sound files for the session. Defaults to '/sounds/' in the cwd.",
)
wav_dir = os.path.abspath(str(parser.parse_args().d))
print("Sound directory:", wav_dir)

if not os.path.exists(wav_dir):
    print("Directory does not exist so creating it...")
    os.mkdir(wav_dir)


pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.mixer.init()


class Session:
    def __init__(self):
        self.filepaths = dict()
        self.sounds = dict()
        self.time = 5
        self.modes = {
            "R": self.record,
            "P": self.play,
            "L": self.loop,
            "F": self.recordandloop,
            "S": self.stop,
            "I": self.incvolume,
            "D": self.decvolume,
        }

        self.actions = {
            "?": self.listregisters,
            "+": self.increcordtime,
            "-": self.decrecordtime,
            "{": self.playall,
            "}": self.stopall,
            "|": self.fillsoundsfromfolder,
        }

    def record(self, name):
        filepath = os.path.join(wav_dir, name + ".wav")
        record(filepath, self.time)
        self.filepaths[name] = filepath
        self.sounds[name] = pygame.mixer.Sound(filepath)

    def play(self, name):
        self.sounds[name].play()

    def loop(self, name):
        self.sounds[name].play(loops=-1)

    def recordandloop(self, name):
        self.record(name)
        self.loop(name)

    def stop(self, name):
        self.sounds[name].fadeout(500)

    def incvolume(self, name):
        curvol = self.sounds[name].get_volume()
        newvol = min(1, curvol + 0.1)
        self.sounds[name].set_volume(newvol)

    def decvolume(self, name):
        curvol = self.sounds[name].get_volume()
        newvol = max(0, curvol - 0.1)
        self.sounds[name].set_volume(newvol)

    def listregisters(self):
        print("Registers filled:", ", ".join(self.sounds.keys()))

    def increcordtime(self):
        self.time += 1
        print("new recording length:", self.time)

    def decrecordtime(self):
        self.time = max(1, self.time - 1)
        print("new recording length:", self.time)

    def playall(self):
        for name, sound in self.sounds.iteritems():
            input("hit enter to play next: ")
            print("current sound:", name)
            sound.play()

    def stopall(self):
        pygame.mixer.fadeout(1000)

    def fillsoundsfromfolder(self):
        found = []
        for wav in os.listdir(wav_dir):
            if not wav.endswith(".wav"):
                print(f"skipping {wav} -- ending")
                continue
            if len(wav) != 5:
                print(f"skipping {wav} -- len")
                continue  # unknown wav file
            name = wav[0]
            found.append(name)
            filepath = os.path.join(wav_dir, wav)
            self.filepaths[name] = filepath
            self.sounds[name] = pygame.mixer.Sound(filepath)
        print(f"Registers filled: {', '.join(found)}")

    def run(self):
        mode = self.record
        while True:
            print("\n\nQ to quit.")
            print("\nmodes:")
            pprint(self.modes)
            print("\nactions:")
            pprint(self.actions)
            print("\ncurrent mode:", mode.__name__)
            print("waiting for input")
            thing = getch()
            print(f"you entered {thing!r}")
            if thing == "Q" or thing == "\x03" or thing == "\x04":  # ctrl-c or ctrl-d
                print("quitting...")
                break
            elif thing in self.modes:
                print("MODE!")
                mode = self.modes[thing]
            elif thing in self.actions:
                print("ACTION!")
                self.actions[thing]()
            else:
                print(f"Giving {thing!r} to {mode.__name__!r}...")
                try:
                    mode(thing)
                except Exception as e:
                    print("unkown error occured:", e)


def pprint(dictionary):
    for key, func in dictionary.items():
        print(key, ":", func.__name__)


if __name__ == "__main__":
    session = Session()
    session.run()
