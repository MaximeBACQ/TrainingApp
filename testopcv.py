import cv2

import os

image_path = os.path.join('img', 'tank.jpg')

img = cv2.imread(image_path)

cv2.imwrite(os.path.join('img', 'tank_out.jpg'), img)

print("Image processed and saved successfully.")
