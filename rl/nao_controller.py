from __future__ import print_function
import argparse
import motion
import time
import almath
from naoqi import ALProxy
from util import readMotion
import msvcrt


class Nao:

    def __init__(self, robotIP, PORT=9559):
        self.motionProxy  = ALProxy("ALMotion", robotIP, PORT)
        self.postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
        self.loadMotionFiles()
        self.currentlyPlaying = None

    # load motion files
    def loadMotionFiles(self):
        self.handWave = readMotion('./motions/HandWave.motion')
        self.forwards = readMotion('./motions/Forwards.motion')
        self.backwards = readMotion('./motions/Backwards.motion')
        self.sideStepLeft = readMotion('./motions/SideStepLeft.motion')
        self.sideStepRight = readMotion('./motions/SideStepRight.motion')
        self.turnLeft60 = readMotion('./motions/TurnLeft60.motion')
        self.turnRight60 = readMotion('./motions/TurnRight60.motion')
        self.shoot = readMotion('./motions/Shoot.motion')

    def startMotion(self, motion):
        # interrupt current motion
        # TODO: Currently this is not working
        # as the makeMove calls are blocking
        if self.currentlyPlaying:
            self.currentlyPlaying = None
            self.motionProxy.stopMove()

        # start new motion
        self.makeMoves(motion)
        self.currentlyPlaying = motion

    def makeMoves(self, motion):
        # TODO: make this non blocking
        JointNames = motion.JointNames
        Poses = motion.Poses

        pFractionMaxSpeed = 0.3

        for pose in Poses:
            self.motionProxy.angleInterpolationWithSpeed(JointNames, pose, pFractionMaxSpeed)

    def run(self):
        self.motionProxy.wakeUp()
        self.postureProxy.goToPosture("StandInit", 0.5)

        self.motionProxy.setMoveArmsEnabled(True, True)
        self.motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

        self.motionProxy.moveInit()

        key = -1
        """
        TODO: Use an event based key control scheme
        TODO: Use move() to keep robot movinf while the key is pressed.
        """
        while True:
            if msvcrt.kbhit():
                # TODO: Unbuffered IO
                key = msvcrt.getch()
            else:
                key = -1
                #self.motionProxy.move(0.0, 0.0, 0.0)

            if key == 'a':
                #self.motionProxy.post.moveTo(0.0, 0.1, 0.0)
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.0,  0.1,  0.0)
            elif key == 'd':
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.0, -0.1,  0.0)
            elif key == 'w':
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.1,  0.0,  0.0)
            elif key == 'W':
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.3,  0.0,  0.0)
            elif key == 's':
                self.motionProxy.move(0.0, 0.0, 0.0)
                #self.startMotion(self.backwards)
                self.motionProxy.move(-0.1, 0.0, 0.0)
            elif key == 'A':
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.0, 0.0, 10 * motion.TO_RAD)
            elif key == 'D':
                self.motionProxy.move(0.0, 0.0, 0.0)
                self.motionProxy.move(0.0, 0.0, -10 * motion.TO_RAD)
            elif key == 'x':
                self.motionProxy.move(0.0, 0.0, 0.0)
                #self.startMotion(self.shoot)
            elif key == 'q' or key == 'Q':
                break

            #self.motionProxy.waitUntilMoveIsFinished()
        
        #self.motionProxy.waitUntilMoveIsFinished()
        self.motionProxy.rest()


def main(robotIP, PORT=9559):

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    print("Waking up")
    motionProxy.wakeUp()

    # Send robot to Stand
    print("Stand up")
    postureProxy.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Motion algorithm
    #####################
    motionProxy.setMoveArmsEnabled(True, True)
    # motionProxy.setMoveArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #print("Move arms cartesian")
    #userArmsCartesian(motionProxy)
    #time.sleep(2.0)

    #print("Move Arms")
    #userArmArticular(motionProxy)
    #time.sleep(2.0)

    print("Make moves")
    makeMoves(motionProxy)
    time.sleep(2.0)

    print("Wait to finish")
    motionProxy.waitUntilMoveIsFinished()

    # Go to rest position
    print("rest")
    motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    bot = Nao(args.ip, args.port)
    bot.run()
    #main(args.ip, args.port)