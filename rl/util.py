from __future__ import print_function
import os

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
        return []



def readMotion(filename="./motions/HandWave.motion"):
    full_path = os.path.join(os.path.abspath(os.path.curdir), filename)
    #print(full_path)
    lines = []
    with open(full_path, 'r') as f:
        lines = f.readlines()
    
    lines = [line.rstrip('\n') for line in lines]
    motion = Motion(lines)
    return motion