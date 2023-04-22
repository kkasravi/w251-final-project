from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os

HOME = os.getcwd()
#print(HOME)

img_name = 'test.png'

img = HOME + '/static/images/'+img_name
txt_file = HOME + '/static/images/preds.txt'
conf_threshold = 0.5

# Create a new YOLO model from scratch
#model = YOLO('yolov8n.yaml')
#load(weights='yolov8n.pt') 

# Pretrained YOLO model placeholder pending training
model = YOLO('yolov8n.pt')
results = model.predict(
    source=img,
    show=False,
    save_txt=False,
    save=False,
    conf=conf_threshold
)

predictions = []

for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
#    masks = result.masks  # Masks object for segmenation masks outputs
    probs = result.probs  # Class probabilities
#    print(result.names)
    
    for box in boxes:
        x,y,width,height = box.xywh.tolist()[0]
        class_name = result.names[box.cls.tolist()[0]]
        conf = box.conf.tolist()[0]
        print(f'Class Name: {class_name}, Confidence Interval: {conf:.4f} \n' \
            'BB: x: {x}, y: {y}, width: {width}, height: {height} \n')
        
        
        
#   print(masks)
#   print('Probs', probs)
#   print('Conf', boxes.conf)

"""
{
  "predictions": [
    {
      "x": 495.0,
      "y": 372.0,
      "width": 86.0,
      "height": 66.0,
      "confidence": 0.9075967073440552,
      "class": "onion",
      "image_path": "test.jpg",
      "prediction_type": "ObjectDetectionModel"
    }
  "image": {
    "width": "640",
    "height": "640"
  }
}
"""
#boxes = results[0].boxes
#box = boxes[0]  # returns one box
#print(box.xyxy,box.xywh) print box bounds and box w-h

# For cloud optimized model export back to edge

#model.export(format='onnx', dynamic=True)

# Perform object detection on an image using the model
#results = model('https://ultralytics.com/images/bus.jpg')

# Export the model to ONNX format
#success = model.export(format='onnx')
