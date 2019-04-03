import argparse
from naoqi import ALProxy

def main(robotIP, PORT=9559, pose="StandInit"):

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Init
    postureProxy.goToPosture(pose, 0.5)

    # Go to rest position
    #motionProxy.rest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",      #"192.168.0.11",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--pose", type=str, default="StandInit")

    args = parser.parse_args()
    main(args.ip, args.port, args.pose)
    