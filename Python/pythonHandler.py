import os
import time
import glob
import subprocess
import sys
import numpy as np
import cv2
import json
from PIL import Image, ImageFilter
from mss import mss 
path = "C:\\FinalYearProject\\Python\\TwitchToddler-Python\\Python\\Output\\"
visu = f"{path}\\visualisations\\*"

def RunFootPrints(count, amount):
    if count >= 1:
        return
    subprocess.call("conda activate Python_footprints && python -m footprints.predict_simple --image C:\\FinalYearProject\\Python\\TwitchToddler-Python\\Python\\Input\\ --model kitti --save_dir C:\FinalYearProject\Python\TwitchToddler-Python\Python\Output", shell = True)

    #while len(glob.glob(visu)) < amount:
        #time.sleep(0.5)
        #print((glob.glob(visu)))
    if len(glob.glob(visu)) == amount:    
        RunEdges()
    return

def RunEdges():
    files = glob.glob(visu)
    index = 0
    for file in files:
        font = cv2.FONT_HERSHEY_COMPLEX
        img2 = cv2.imread(file, cv2.IMREAD_COLOR)
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        _, threshold = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
        contours, _= cv2.findContours(threshold, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
        h, w = img.shape
        coords = [{'x': str(w), 
                    'y': str(h)}]
        coordscount = 0
        
        for cnt in contours :
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
            cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)
            n = approx.ravel() 
            i = 0
            for j in n :
                if(i % 2 == 0):
                    x = n[i]
                    y = n[i + 1]
                    string = str(x) + " " + str(y) 
                    coords.append(
                      {'x': str(x),
                      'y': str(y)}
                    )
                    coordscount +=1
  
                    if(i == 0):
                        cv2.putText(img2, "Arrow tip", (x, y),
                                font, 0.5, (255, 0, 0)) 
                    else:
                        cv2.putText(img2, string, (x, y), 
                          font, 0.5, (0, 255, 0)) 
                i = i + 1

        cv2.imwrite(f"{path}edges\\edge{str(index)}.jpg", img2)
        out_file = open(f"{path}json\\coords{str(index)}.json", "w+")
        json.dump(coords, out_file)
        out_file.close()
        index += 1


files = glob.glob("./Input/*")
files += glob.glob("./Output/visualisations/*")
files += glob.glob("./Output/outputs/*")
files += glob.glob("./Output/edges/*")
files += glob.glob("./Output/json/*")
count = 0

for file in files:
    os.remove(file)

try:
    amount = int(sys.argv[1])
except:
    sys.exit(0)

with mss() as sct:
    for x in range(amount):
        filename = sct.shot(mon=1, output=f"Input/screenshot{str(x)}.png")


os.chdir("C:\\Users\\Claire\\Documents\\GitHub\\footprints")
RunFootPrints(count, amount)
