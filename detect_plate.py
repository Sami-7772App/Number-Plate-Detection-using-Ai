import cv2
import torch
import easyocr
import matplotlib.pyplot as plt

# Load YOLOv5 model (ensure yolov5 folder is in project root)
model = torch.hub.load('yolov5', 'yolov5s', source='local')

# Load image
image_path = 'car.jpg'
img = cv2.imread(image_path)
results = model(img)

# Show detection
results.print()
results.show()

# Extract and read plates
reader = easyocr.Reader(['en'])
cords = results.xyxy[0]  # xyxy format

for box in cords:
    x1, y1, x2, y2, conf, cls = box
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    plate = img[y1:y2, x1:x2]
    plt.imshow(cv2.cvtColor(plate, cv2.COLOR_BGR2RGB))
    plt.title("Detected Plate")
    plt.axis("off")
    plt.show()

    # OCR
    result = reader.readtext(plate)
    for (bbox, text, prob) in result:
        print(f"Detected Text: {text}, Confidence: {prob:.2f}")
