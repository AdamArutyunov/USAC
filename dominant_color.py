from PIL import Image, ImageDraw
import cv2
import numpy as np


def average(img):
    x, y = img.size
    try:
        img = Image.fromarray(img)
    except TypeError:
        pass
    pixels = img.load()
    x, y = img.size
    r, g, b = 0, 0, 0
    for i in range(x):
        for j in range(y):
            r += pixels[i, j][0]
            g += pixels[i, j][1]
            b += pixels[i, j][2]
    r //= (x * y)
    g //= (x * y)
    b //= (x * y)
    new = Image.new('RGB', (x, y), (r, g, b))
    return cv2.cvtColor(np.array(new), cv2.COLOR_RGB2BGR)



def gradient(color):
    color = color.lower()
    new = Image.new('RGB', (512, 200), (0, 0, 0))
    draw = ImageDraw.Draw(new)
    for i in range(512):
        colors = {'r': (i // 2, 0, 0), 'g': (0, i // 2, 0), 'b': (0, 0, i // 2)}
        draw.line((i, 0) + (i, 200), fill=colors[color], width=1)
    return new


def check_color(img):
    try:
        x, y = img.size
    except TypeError:
        y, x, _ = img.shape
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
    except TypeError:
        pass
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    colors = {i: 0 for i in [red, white, black]}
    for i in range(x):
        for j in range(y):
            pix = img.getpixel((i, j))
            for color in colors:
                total = 0
                for value in range(3):
                    total += abs(color[value] - pix[value])
                colors[color] += total
    colors[(0, 0, 0)] *= 1.75
    colors[(255, 0, 0)] *= 1.5
    colors[(255, 255, 255)] *=.75
    print(colors)
    return min(colors, key=lambda x: colors[x])


def colors_old(img):
    result = {}
    img = np.array(img)
    colors = {'Красный': [np.uint8([0, 93, 0]), np.uint8([41, 255, 255])], 
              'Чёрный': [np.uint8([70, 0, 0]), np.uint8([119, 169, 110])], 
              'Белый': [np.uint8([0, 0, 170]), np.uint8([255, 255, 255])]}
    for i in colors:
        y, x, _ = img.shape
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, *colors[i])
        result[i] = sum(sum(mask))
    return max(result, key=lambda x: result[x])
    

cam = cv2.VideoCapture(0)

while 1:
    
    frame, img = cam.read()
    
    if not frame: print('aoao'); break

    cv2.imshow('', img)
    
    a = cv2.waitKey(1) & 0xFF
    
    if a == 27:
        break
    elif a == ord('t'):
        print(check_color(img))
        
cv2.destroyAllWindows()
cam.release()




'''
cat = Image.open('cat.jpg')
cat = cv2.imread('cat.jpg')
#cat = gradient('R')


all_colors = check_color(cat)
result = min(all_colors, key=lambda x: all_colors[x])


print(result)
print(colors_old(cat))
'''