import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
from datetime import datetime
import os
from PIL import ImageGrab

# adjust as needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ["TESSDATA_PREFIX"] = r"models\tesseract"
YOLOV5_PATH = r"models\yolov5\best.onnx"

MODEL_WIDTH = 640
MODEL_HEIGHT = 640
MINIMUM_OBJECT_CONFIDENCE = 0.90
NMS_SCORE_THRESHOLD = 0.45
NMS_THRESHOLD = 0.50

net = cv2.dnn.readNetFromONNX(YOLOV5_PATH)

def image_to_text(np_array):
    image = Image.fromarray(np_array)
    text = pytesseract.image_to_string(image)
    return text

def save_image(image, img_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    data_file_name = f"{timestamp}.png"
    file_path = os.path.join(img_dir, data_file_name)
    cv2.imwrite(file_path, image)
    return file_path

def get_screenshot_np():
    img_pil = ImageGrab.grab()
    img_np = np.array(img_pil)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    return img_np

def get_tooltip(img):
    if img is None:
        raise ValueError("Image not found.")

    # If the image has 4 channels (including alpha), convert from BGRA to BGR.
    if img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Create a square canvas with side length equal to the max dimension of the original image.
    max_dim = max(img.shape[0], img.shape[1])
    resized = np.zeros((max_dim, max_dim, 3), dtype=np.uint8)
    resized[:img.shape[0], :img.shape[1]] = img

    # Create a blob from the resized image.
    blob = cv2.dnn.blobFromImage(
        resized,
        1 / 255.0,
        (MODEL_WIDTH, MODEL_HEIGHT),
        (0, 0, 0),
        swapRB=True,
        crop=False
    )

    # Set the blob as input to the network.
    net.setInput(blob)

    # Run the forward pass.
    outputs = net.forward()

    # --- Post-processing the outputs ---
    if len(outputs.shape) == 3:
        # Extract dimensions.
        dimensions = outputs.shape[1]
        rows = outputs.shape[2]
        
        # Reshape the output to have one detection per row.
        out = outputs.reshape(dimensions, rows).T
    else:
        out = outputs
        rows, dimensions = out.shape

    # Calculate scale factors to map detection coordinates back to the resized image.
    x_scale = resized.shape[1] / MODEL_WIDTH
    y_scale = resized.shape[0] / MODEL_HEIGHT

    # Prepare lists to hold detection results.
    class_ids = []
    confidences = []
    boxes = []

    # Loop over each detection row.
    for i in range(rows):
        detection = out[i]
        
        # The first four values are x, y, width, and height.
        x, y, w, h = detection[:4]
        scores = detection[4:]
        max_class_score = np.max(scores)
        class_id = np.argmax(scores)
        
        if max_class_score > MINIMUM_OBJECT_CONFIDENCE:
            confidences.append(float(max_class_score))
            class_ids.append(class_id)
            
            # Convert center coordinates to top-left corner coordinates.
            left = int((x - 0.5 * w) * x_scale)
            top = int((y - 0.5 * h) * y_scale)
            width = int(w * x_scale)
            height = int(h * y_scale)
            boxes.append([left, top, width, height])


    # Apply non-maximum suppression to remove overlapping boxes.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, NMS_SCORE_THRESHOLD, NMS_THRESHOLD)

    if len(indices) == 0:
        return None
    else:
        indices = indices.flatten() if isinstance(indices, np.ndarray) else indices
        tooltips = [boxes[i] for i in indices]

        # Assuming tooltips is populated and contains bounding boxes after NMS.
        if len(tooltips) > 0:
            first_rect = tooltips[0]
            left, top, width, height = first_rect
            
            # Crop the image using the bounding box coordinates.
            cropped_image = img[top:top + height, left:left + width]
            return cropped_image
        else:
            print("No valid bounding boxes found after NMS.")
            return None