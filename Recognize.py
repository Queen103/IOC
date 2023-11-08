import cv2 
import numpy as np 
import os
import datetime
import requests
import credentials as cr

def recognizerUser():
    
    output_directory = 'history'
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read("trainer/trainer.yml")
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX 

    id = 0
    cam = cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)

    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    count = 0
    while True:
        response = requests.get('http://127.0.0.1:5000/check_loop')
        ret,img = cam.read()
        #img = cv2.flip(img,-1)

        gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors=5,
            minSize=(int(minW),int(minH)),
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(img , (x,y) , (x+w,y+h) , (255,0,0) , 2)
            id, confidence = recognizer.predict(gray[y:y+h , x: x+w])

            if(confidence < 50  ):
                count+=1
                id = id
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknow"
                confidence = "  {0}%".format(round(100 - confidence))
            
            print(confidence)
        
        cv2.imshow("nhan dien khuon mat", img)
        # Thoát nếu nhấn q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 
        if count > 10 :
            current_time = datetime.datetime.now()
            date = str(current_time)[:-7].replace(" ","-")
            # print(f"{id}.{date}.jpg")
            date1 = date.replace(":","")
            date1 = date1.replace("-","")
            save = f"{id}.{date1}.jpg"
            image_path = os.path.join(output_directory,save)
            cv2.imwrite(image_path, img)
            break 
        if response.status_code == 200 and response.json().get('should_stop'):
            break  # Dừng vòng lặp nếu API trả về trạng thái 'should_stop' là True

    print("\n[INFO] Thoat")
    cam.release()
    cv2.destroyAllWindows()
    return id,save,date 

def visit(id):
    # Tên thư mục để lưu ảnh
    output_directory = 'visitdata'

    # Tạo thư mục nếu nó chưa tồn tại
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Khởi tạo camera
    cap = cv2.VideoCapture(0)  # Sử dụng camera mặc định (0) hoặc chỉ định camera cụ thể

    # Khởi tạo bộ phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    save = ""
    date = ""
    while True:
        # Đọc một khung hình từ camera
        ret, frame = cap.read()

        if ret:
            # Chuyển khung hình sang độ sáng xám (grayscale) để cải thiện việc nhận diện
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Sử dụng bộ phát hiện khuôn mặt để nhận diện khuôn mặt trong khung hình
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            count=0
            # Vẽ hộp xung quanh khuôn mặt và lưu ảnh
            for (x, y, w, h) in faces:
                
                count=1
                current_time = datetime.datetime.now()
                date = str(current_time)[:-7].replace(" ","-")
                # print(f"{id}.{date}.jpg")
                date1 = date.replace(":","")
                date1 = date1.replace("-","")
                save = f"{id}.{date1}.jpg"
                image_path = os.path.join(output_directory,save)
                cv2.imwrite(image_path, frame)
                

            # Hiển thị khung hình (không bắt buộc)
            cv2.imshow('Camera', frame)

        # Đợi một phím bất kỳ để thoát
        if count == 1:
            break

    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()
    return save,date




