import cv2
import numpy as np
import os
path = 'dataset'

def getdataface(id):
    
    # Khởi tạo thuật toán phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_id = id
    #tạo thư mục dataset
    if not os.path.exists(path):
        os.makedirs(path)

    # Bắt đầu video capture 
    cap = cv2.VideoCapture(0)
    count = 0 
    while True:
        # Đọc frame
        ret, img = cap.read()

        # Chuyển về grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Phát hiện khuôn mặt
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Vẽ hình chữ nhật quanh mỗi khuôn mặt
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) 
            count+= 1
            cv2.imwrite(str(path)+"/User." + str(face_id) + '.' +str(count) + ".jpg",gray[ y:y+h , x:x+w ])
            print("done")

        # Hiển thị
        cv2.imshow('img',img)

        # Thoát nếu nhấn q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        if count >= 100:
            break
        
    # Giải phóng camera
    cap.release()
    cv2.destroyAllWindows()