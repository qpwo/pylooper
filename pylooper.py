import pygame
import os
from record import record
from getch import getch

workingdir = os.getcwd() + "/"

pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.mixer.init()


class Session:
    def __init__(self):
        self.filepaths = dict()
        self.sounds = dict()
        self.time = 5
        self.modes = {
            "E": self.edit,
            "P": self.play,
            "L": self.loop,
            "F": self.editandloop,
            "S": self.stop,
            "I": self.incvolume,
            "D": self.decvolume,
        }

        self.actions = {
            "+": self.increcordtime,
            "-": self.decrecordtime,
            "{": self.playall,
            "}": self.stopall,
            "|": self.fillsoundsfromfolder,
        }

    def edit(self, name):
        filepath = workingdir + "s/" + name + ".wav"
        record(filepath, self.time)
        self.filepaths[name] = filepath
        self.sounds[name] = pygame.mixer.Sound(filepath)

    def play(self, name):
        self.sounds[name].play()

    def loop(self, name):
        self.sounds[name].play(loops=-1)

    def editandloop(self, name):
        self.edit(name)
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

    def increcordtime(self):
        self.time += 1

    def decrecordtime(self):
        self.time -= 1

    def playall(self):
        for name, sound in self.sounds.iteritems():
            input("hit enter to play next: ")
            print("current sound:", name)
            sound.play()

    def stopall(self):
        pygame.mixer.fadeout(1000)

    def fillsoundsfromfolder(self):
        for wav in os.listdir(workingdir + "s"):
            if ".wav" not in wav:
                continue
            name = wav[: wav.find(".")]
            filepath = workingdir + "s/" + name + ".wav"
            self.filepaths[name] = filepath
            self.sounds[name] = pygame.mixer.Sound(filepath)

    def run(self):
        mode = self.edit
        while True:
            print("\n\nmodes:")
            pprint(self.modes)
            print("\nactions:")
            pprint(self.actions)
            print("\ncurrent mode:", mode.__name__)
            print("waiting for input")
            thing = getch()
            print("you entered", thing)
            if thing == "Q":
                print("quitting...")
                break
            elif thing in self.modes:
                print("MODE!")
                mode = self.modes[thing]
            elif thing in self.actions:
                print("ACTION!")
                self.actions[thing]()
            else:
                try:
                    mode(thing)
                except Exception as e:
                    print("error occured:", e)


def pprint(dictt):
    for key, func in dictt.items():
        print(key, ":", func.__name__)


if __name__ == "__main__":
    session = Session()
    session.run()
