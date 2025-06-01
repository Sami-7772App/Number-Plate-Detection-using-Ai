import cv2
import easyocr
import torch
import numpy as np

# Load YOLOv5 model (you must be connected to the internet the first time)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Start webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv5 model on the frame
    results = model(frame)

    # Get results in (x1, y1, x2, y2, confidence, class) format
    detections = results.xyxy[0].numpy()

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        cropped_plate = frame[y1:y2, x1:x2]

        # OCR on the cropped plate
        result = reader.readtext(cropped_plate)
        for (bbox, text, prob) in result:
            # Draw rectangle and text on the original frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Show frame
    cv2.imshow("Number Plate Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
