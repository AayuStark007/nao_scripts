from __future__ import print_function
import os
import msvcrt
import curses
import time

class Motion:
    def __init__(self, data):
        self.JointNames = []
        self.Poses = [[]]
        self.Times = []
        self.makePose(data)
    
    def makePose(self, data):
        if len(data) <= 0:
            return
        self.JointNames = self.getJointNames(data[0])
        self.Poses = self.getPoses(data[1:])
        self.Times = self.getTimings(data[1:])
    
    def getJointNames(self, line):
        res = line.split(',')
        return res[2:]

    def getPoses(self,data):
        poses = []
        ref = ['0.0','0.0','0.0']

        for line in data:
            pose = line.split(',')[2:]

            for i, elem in enumerate(pose):
                if elem == '*':
                    pose[i] = ref[i]
            
            ref = pose
            pose = map(float, pose)
            poses.append(pose)

        return poses
    
    def getTimings(self, data):
        timings = []

        for line in data:
            times = line.split(',')[0].split(':')
            mm, ss, ms = times[0], times[1], times[2]
            timings.append(mm+ss+ms)
        
        return timings

            


def readMotion(filename="HandWave.motion"):
    full_path = os.path.join(os.path.abspath(os.path.curdir), "motions", filename)
    #print(full_path)
    lines = []
    with open(full_path, 'r') as f:
        lines = f.readlines()
    
    lines = [line.rstrip('\n') for line in lines]
    motion = Motion(lines)
    return motion

def debug(motion):
    #print(motion.JointNames)
    #for pose in motion.Poses:
    #    print(pose)
    for times in motion.Times:
        print(times)

def main(stdscr):
    stdscr.nodelay(1)
    while True:
        time.sleep(0.005)
        c = stdscr.getch()
        if c == ord('q'):
            break
        if c != -1:
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            stdscr.move(0,0)
        else:
            stdscr.addstr('nil')
            stdscr.refresh()
            stdscr.move(0,0)



#motion = readMotion()
#debug(motion)
print("starting...")
while True:
    if msvcrt.kbhit():
        print(msvcrt.getch())

#curses.wrapper(main)
