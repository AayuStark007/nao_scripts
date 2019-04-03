import argparse
import sys
import numpy as np
import cv2
import json
import requests
import util
from naoqi import ALProxy


def main(videoDev):
    AL_kTopCamera = 0
    AL_kBottomCamera = 1
    AL_kQVGA = 1
    AL_kVGA = 2
    AL_kBGRColorSpace = 13
    test_url = 'http://localhost:5000/posenet'
    content_type = 'image/jpeg'
    headers = {'content_type': content_type}
    cap = videoDev.subscribeCamera("test2", AL_kBottomCamera, AL_kQVGA, AL_kBGRColorSpace, 25)

    width = 320#640
    height = 240#480
    image = np.zeros((height,width,3), np.uint8)

    while True:
        result = videoDev.getImageRemote(cap)
        if result == None:
            print 'cannot capture.'
        elif result[6] == None:
            print 'no image data string.'
        else:
            values = map(ord, list(result[6]))
            i = 0
            #TODO: find better way to retrieve images
            for y in range(0, height):
                for x in range(0, width):
                    image.itemset((y, x, 0), values[i + 0])
                    image.itemset((y, x, 1), values[i + 1])
                    image.itemset((y, x, 2), values[i + 2])
                    i += 3

            _, img_encoded = cv2.imencode('.jpg', image)

            response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
            result = json.loads(response.text)

            if not result["success"]:
                continue
            
            pose_scores, keypoint_scores, keypoint_coords = np.array(result['pose_scores']), np.array(result['keypoint_scores']), np.array(result['keypoint_coords'])

            overlay_image = util.draw_skel_and_kp(
                image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.15, min_part_score=0.1)

            # show image
            cv2.imshow("nao-top-camera-320x240", overlay_image)
        
        if cv2.waitKey(33) == 27:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    
    videoDev = ALProxy('ALVideoDevice', args.ip, args.port)

    main(videoDev)