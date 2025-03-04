from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from email.message import EmailMessage
import ssl
import smtplib

def sendmails():
    email_sender = "aryasagar123456@gmail.com"
    email_password = "ipvs jech njne ubio"
    email_receivers = ["sagarraj10102003@gmail.com",  "bhaisagar03214@gmail.com"]

    subject = 'Crowd is overlimit'
    body = """
    Dear [Recipient's Name],

    I hope this message finds you well. We would like to inform you that our crowd
    monitoring system has detected an excess of people at Phagwara Junction at 10:23 PM.
    This situation requires immediate attention and monitoring.

    Sincerely,
    [Team XYZ]
    """

    for email_receiver in email_receivers:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())


#
# Initialize the video capture from a webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1000)  # 1280
cap.set(4, 720)   # 720
# cap = cv2.VideoCapture("")  # For Video

model = YOLO("yolov8n.pt")

v = 1
output_image_counter = 1

int(0)
start_time=time.time()

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

zone_x1, zone_y1, zone_x2, zone_y2 = 0, 0, 1280, 720  # Adjust dimensions as needed

detected_ids = set()

prev_frame_time = 0
new_frame_time = 0

while True:
    current_time=time.time()-start_time
    new_frame_time = time.time()
    success, img = cap.read()
    people_count = 0

    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            if "person" == classNames[cls]:
                people_count = people_count + 1

    if people_count >=1:
        if current_time>=30 and v==1:
            v = 0
            sendmails()

    else:
        start_time=time.time()
        v=1


    count_text = f'People Count: {people_count}'
    cv2.putText(img, count_text, (zone_x1, zone_y2 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.rectangle(img, (zone_x1, zone_y1), (zone_x2, zone_y2), (0, 0, 255), 2)
    cv2.putText(img, count_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()