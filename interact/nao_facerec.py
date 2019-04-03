from __future__ import print_function

import argparse
import time

from naoqi import ALBroker, ALProxy, ALModule
count = 0
class FaceRecModule(ALModule):
    """ Python module to detect faces and match profile"""

    def face_recognized(self, strVarName, value):
        """callback face"""
        try:
            rec = value[1][1]
            if len(rec) > 0:
                if rec[0] == 2 or rec[0] == 3:
                    print(rec[1][0])
        except Exception, e:
            pass
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    

    broker = ALBroker("pythonBroker","127.0.0.1",0,"192.168.0.16",9559)
    faceModule = FaceRecModule("faceModule")
    memProxy = ALProxy('ALMemory')
    
    memProxy.subscribeToEvent("FaceDetected", "faceModule", "face_recognized")

    while True:
        time.sleep(2)

    main(memProxy)