import cv2
import numpy as np
import NFC
import fb
import time
import os
from PIL import Image


class ColorChecker:  
    def check_color(self, img):
        try:
            x, y = img.size
        except TypeError:
            y, x, _ = img.shape
        try:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
        except TypeError:
            pass
        img = img.crop((int(x*.3), int(y*.3), int(x*.7), int(y*.7)))
        x, y = img.size
        red = (200, 0, 0)
        black = (0, 0, 0)
        white = (255, 255, 255)
        colors = {i: 0 for i in [red, white, black]}
        for i in range(x):
            for j in range(y):
                pix = img.getpixel((i, j))
                max_point = 1000**100
                max_color = red
                for color in colors:
                    total = 0
                    for value in range(3):
                        total += abs(color[value] - pix[value])
                    if total < max_point:
                        max_color = color
                        max_point = total
                colors[max_color] += 1
        colors_name = {red: 'красный', black: 'чёрный', white: 'белый'}
        return colors_name[max(colors, key=lambda x: colors[x])]



def take_snapshot(camera_port=0):
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)
    return_value, image = camera.read()
    del camera
    return image

nfc_module = NFC.NFCAnalyzer('/dev/ttyACM0', 9600)
color_checker = ColorChecker()
db, app, cent = fb.firebase_connection()
out = fb.parse_results(db)

while True:
    while True:
        res = nfc_module.getUid()
        if res:
            res = NFC.pallet_accordance(res)
            for o in out:
                if o['pallet'] == res:
                    img = take_snapshot(os.getcwd() + '/color_check_photo.jpg')
                    if color_checker.check_color(take_snapshot(2)) == o['color']:
                        o['status'] = 'Покрашено'
                        o['pallet'] = None
                        db.collection('today_details').document(o['id_num']).set(o)
        time.sleep(1)
    time.sleep(5)
