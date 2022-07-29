"""Records screen"""
import cv2, sys, argparse, ctypes, os
import numpy as np
import pyautogui
import time
import datetime
from threading import Thread

username = os.environ.get("USERNAME")
user32 = ctypes.windll.user32
w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)  # get size

now = datetime.datetime.now()
parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("-pos", nargs="*", help="x pos", default=[0, 0], type=int)  # start x
parser.add_argument("-fps", help="fps of video", default=120, type=int)  # start x
parser.add_argument("-size", nargs="*", help="width of recorded area", default=["MAX", "MAX"], type=str)  # start width
parser.add_argument("-path", help="Path of output file", default=f"C:\\Users\\{username}\\Pictures\\{now.hour}-{now.minute}-{now.second}-{now.day}-{now.month}-{now.year}.avi", type=str)
args = parser.parse_args()  # arguments
print(args)

error = False

path = args.path
fps = args.fps

pos = args.pos
if len(pos) != 2:
    print("pos must have only value [x, y] length:2")
    error = True

try:
    size = int(args.size[0].replace("MAX", str(w))), int(args.size[1].replace("MAX", str(h)))

except ValueError:
    print("size value must be MAX or a integer value")
    error = True

if error is True:
    quit()

size = int(args.size[0].replace("MAX", str(w))), int(args.size[1].replace("MAX", str(h)))


global run
run = True

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(path, fourcc, 20.0, size)

def record():
    """Record video"""
    global run
    prev = 0
    while run:
        time_elapsed = time.time() - prev

        img = pyautogui.screenshot()

        if 1.0/fps <= time_elapsed:
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

            cv2.waitKey(100)


thread = Thread(target=record)
thread.start()

input("Stop: ")
run = False

thread.join()
cv2.destroyAllWindows()
out.release()
os.system(path)
quit()
