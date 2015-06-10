# Luke Miles, December 2014
import pygame
import os
from record import record
from getch import getch

workingdir = "/home/jane/python/sound/"

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()

filepaths = dict()
sounds = dict()
time = 5

def edit(name):
    global filepaths, sounds
    filepath = workingdir + "s/" + name + ".wav"
    record(filepath, time)
    filepaths[name] = filepath
    sounds[name] = pygame.mixer.Sound(filepath)


def play(name):
    sounds[name].play()

def loop(name):
    sounds[name].play(loops=-1)

def editandloop(name):
    global filepaths, sounds
    edit(name)
    loop(name)

def stop(name):
    sounds[name].fadeout(500)

def incvolume(name):
    curvol = sounds[name].get_volume()
    newvol = min(1, curvol + 0.1)
    sounds[name].set_volume(newvol)

def decvolume(name):
    curvol = sounds[name].get_volume()
    newvol = max(0, curvol - 0.1)
    sounds[name].set_volume(newvol)

def increcordtime():
    global time
    time += 1

def decrecordtime():
    global time
    time -= 1

def playall():
    for name, sound in sounds.iteritems():
        raw_input("hit enter to play next: ")
        print "current sound:", name
        sound.play()

def stopall():
    pygame.mixer.fadeout(1000)

def fillfilepathsfromfolder():
    for wav in os.listdir(workingdir + "s"):
        if ".wav" not in wav:
            continue
        name = wav[:wav.find('.')]
        filepaths[name] = workingdir + "s/" + name + ".wav"

def updatesounds():
    for (name, filepath) in filepaths.iteritems():
        sounds[name] = pygame.mixer.Sound(filepath)

modes =   {'E' : edit,
           'P' : play,
           'L' : loop,
           'F' : editandloop,
           'S' : stop,
           'I' : incvolume,
           'D' : decvolume}

actions = {'+' : increcordtime,
           '-' : decrecordtime,
           '{' : playall,
           '}' : stopall,
           '|' : fillfilepathsfromfolder,
           '<' : updatesounds}

def pprint(dictt):
    for key, func in dictt.iteritems():
        print key, ':', func.__name__

def main():
    mode = edit
    while True:
        print "\n\nmodes:"
        pprint(modes)
        print "\nactions:"
        pprint(actions)
        print "\ncurrent mode:", mode.__name__
        print "waiting for input"
        thing = getch()
        print "you entered", thing
        if thing == 'Q':
            print "quitting..."
            break
        elif thing in modes:
            print "MODE!"
            mode = modes[thing]
        elif thing in actions:
            print "ACTION!"
            actions[thing]()
        else:
            try:
                mode(thing)
            except:
                print "oops!"

if __name__ == "__main__":
    main()
