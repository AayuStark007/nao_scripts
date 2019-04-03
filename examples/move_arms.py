from __future__ import print_function
import argparse
import motion
import time
import almath
from naoqi import ALProxy
from util import readMotion

def userArmsCartesian(motionProxy):
    effector   = ["LArm", "RArm"]
    frame      = motion.FRAME_TORSO
    useSensorValues = False

    # just control position
    axisMask   = [motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL]

    # LArm path
    pathLArm = []
    initTf   = almath.Transform(motionProxy.getTransform("LArm", frame, useSensorValues))
    targetTf = almath.Transform(motionProxy.getTransform("LArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 -= 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))
    pathLArm.append(list(targetTf.toVector()))
    pathLArm.append(list(initTf.toVector()))

    # RArm path
    pathRArm = []
    initTf   = almath.Transform(motionProxy.getTransform("RArm", frame, useSensorValues))
    targetTf = almath.Transform(motionProxy.getTransform("RArm", frame, useSensorValues))
    targetTf.r1_c4 += 0.04 # x
    targetTf.r2_c4 += 0.10 # y
    targetTf.r3_c4 += 0.10 # z
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))
    pathRArm.append(list(targetTf.toVector()))
    pathRArm.append(list(initTf.toVector()))

    pathList = []
    pathList.append(pathLArm)
    pathList.append(pathRArm)

    # Go to the target and back again
    timesList = [[1.0, 2.0, 3.0, 4.0],
                 [1.0, 2.0, 3.0, 4.0]] # seconds

    motionProxy.transformInterpolations(effector, frame, pathList,
                                       axisMask, timesList)


def userArmArticular(motionProxy):
    # Arms motion from user have always the priority than walk arms motion
    JointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    Arm1 = [-40,  25, 0, -40]
    Arm1 = [ x * motion.TO_RAD for x in Arm1]

    Arm2 = [-40,  50, 0, -80]
    Arm2 = [ x * motion.TO_RAD for x in Arm2]

    print("Arm1: ", Arm1)
    print("Arm2: ", Arm2)

    pFractionMaxSpeed = 0.6

    motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm2, pFractionMaxSpeed)
    motionProxy.angleInterpolationWithSpeed(JointNames, Arm1, pFractionMaxSpeed)

def makeMoves(motionProxy):
    """
    JointNames = ["RShoulderPitch", "RShoulderRoll", "LShoulderPitch"]
    Poses = [
        [-1.5,0,1.49797],
        [-1.5,0.1,1.49797],
        [-1.5,0.2,1.49797],
        [-1.5,0.3,1.49797],
        [-1.5,0.2,1.49797],
        [-1.5,0.1,1.49797],
        [-1.5,0,1.49797],
        [-1.5,-0.1,1.49797],
        [-1.5,-0.2,1.49797],
        [-1.5,-0.3,1.49797],
        [-1.5,-0.4,1.49797],
        [-1.5,-0.5,1.49797],
        [-1.5,-0.5,1.49797],
        [-1.5,-0.4,1.49797],
        [-1.5,-0.3,1.49797],
        [-1.5,-0.2,1.49797],
        [-1.5,-0.1,1.49797],
        [-1.5,0,1.49797],
        [-1.5,0.1,1.49797],
        [-1.5,0.2,1.49797],
        [-1.5,0.2,1.49797],
        [-1.5,0.1,1.49797],
        [-1.5,0,1.49797],
        [-1.5,-0.1,1.49797],
        [-1.5,-0.2,1.49797],
        [-1.5,-0.3,1.49797],
        [-1.5,-0.4,1.49797],
        [-1.5,-0.5,1.49797],
        [-1.5,-0.4,1.49797],
        [-1.5,-0.3,1.49797],
        [-1.5,-0.2,1.49797],
        [-1.5,-0.1,1.49797],
        [-1.5,0,1.49797],
        [-1.5,0,1.49797],
        [-1.5,0,1.49797],
        [1.4,0,1.49797],
        [1.4,0,1.49797]
    ]
    """
    motion = readMotion("./motions/Forwards.motion")
    JointNames = motion.JointNames
    Poses = motion.Poses

    pFractionMaxSpeed = 0.6

    for pose in Poses:
        motionProxy.angleInterpolationWithSpeed(JointNames, pose, pFractionMaxSpeed)


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
    #motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

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
    main(args.ip, args.port)