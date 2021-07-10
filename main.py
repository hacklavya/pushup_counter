import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy.signal import savgol_filter

cap = cv2.VideoCapture("skipping.mp4")
# fourcc = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))


_, first_frame = cap.read()
first_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)
hh, ww = first_gray.shape

f2 = open("f2.txt", "w")
f3 = open("f3.txt", "w")
f4 = open("f4.txt", "w")
f5 = open("f5.txt", "w")
f6 = open("f6.txt", "w")

buffer_time = 100
a           = [0 for i in range(buffer_time)]
a_up        = [0 for i in range(buffer_time)]
a_down      = [0 for i in range(buffer_time)]
a_pref_flip = [0 for i in range(buffer_time)]
a_flip      = [0 for i in range(buffer_time)]

a_max = 100
a_min = 100
flip_flag = 150
prev_flip_flag = 150
count = 0
i=1
key = 1
while key != 27:
    print('i: ',i)
    i = i+1
    _, frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.GaussianBlur(frame_gray, (5, 5), 0)
    difference = cv2.absdiff(first_gray, frame_gray)
    _, difference = cv2.threshold(difference, 70, 255, cv2.THRESH_BINARY)
    M = cv2.moments(difference)
    cX = int(M["m10"] / (M["m00"]+0.001))
    cY = int(M["m01"] / (M["m00"]+0.001))
    a.pop(0)
    a.append(cY)
    f2.write(str(a[-1])+'\n')
    
    a_max = 0.5 * a_max + 0.5 * np.max(a)
    a_up.pop(0)
    a_up.append(a_max)
    f3.write(str(a_max)+'\n')

    a_min = 0.5 * a_min + 0.5 * np.min(a)
    a_down.pop(0)
    a_down.append(a_min)
    f4.write(str(a_min)+'\n')

    prev_flip_flag = flip_flag
    a_pref_flip.pop(0)
    a_pref_flip.append(prev_flip_flag)
    f6.write(str(prev_flip_flag)+'\n')

    if cY > 0.9*a_max and flip_flag==150:
        flip_flag = 250
    if cY < 1.111*a_min and flip_flag==250:
        flip_flag = 150
    a_flip.pop(0)
    a_flip.append(flip_flag)
    f5.write(str(flip_flag)+'\n')
    
    if prev_flip_flag > flip_flag:
        count = count + 1

    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(frame, "count = " + str(count), (int(ww*0.6), int(hh*0.4)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("difference", difference)
    #out.write(difference)

    plt.clf()
    plt.plot(a)
    plt.plot(a_up)
    plt.plot(a_down)
    plt.plot(a_pref_flip)
    plt.plot(a_flip)
    plt.pause(0.01)

   
    key = cv2.waitKey(1)
    if key == 27:
        cap.release()
        cv2.destroyAllWindows()
        exit(0)