import cv2

import os

# image_path = os.path.join('media/img', 'tank.jpg')




# img = cv2.imread(image_path)

# cv2.imwrite(os.path.join('media/img', 'tank_out.jpg'), img)

# print("Image processed and saved successfully.")


# cv2.imshow('image', img)

# cv2.waitKey(5000)  # wait for input to leave (if 0), if a number is used, show for this about of ms




# video_path = os.path.join('media/vid', 'helicopter.mp4')

# video = cv2.VideoCapture(video_path)

# ret = True
# while ret:
#     ret, frame = video.read()

#     if ret: #mandatory bc when we reach the end of the video, ret becomes false bc there's no value left to read
#         cv2.imshow('frame',frame)
#         cv2.waitKey(40)   #the video is 25fps, which is one frame every 40 milliseconds, so we visualize one frame after the other every 40ms

# video.release()
# cv2.destroyAllWindows()




# webcam = cv2.VideoCapture(0)

# while True:
#     ret, frame = webcam.read()

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(30) & 0xFF == ord('q'):
#         break

# webcam.release()
# cv2.destroyAllWindows()


img = cv2.imread(os.path.join('media/img', 'tank.jpg'))


# resized_img = cv2.resize(img, (300, 132))

print(img.shape)
# print(resized_img.shape)

cv2.imshow('img', img)
# cv2.imshow('resized_img', resized_img)
# cv2.waitKey(0)

cropped_img = img[100:400, 100:365] #height then width
cv2.imshow('cropped_img', cropped_img)
cv2.waitKey(0)