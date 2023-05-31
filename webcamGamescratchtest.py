import cv2
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import random

model = MobileNetV2(weights='imagenet')


def run_image_recognition(image):
     # Calculate the center coordinates of the image
    height, width = image.shape[:2]
    center_x = width // 2
    center_y = height // 2
    
    # Define the size of the cropped region
    crop_size = int(min(center_x, center_y) * 1.2)
    
    # Calculate the coordinates for cropping
    start_x = center_x - crop_size // 2
    end_x = center_x + crop_size // 2
    start_y = center_y - crop_size // 2
    end_y = center_y + crop_size // 2
    
    # Crop the image to the defined region
    cropped_image = image[start_y:end_y, start_x:end_x]
    
    # Preprocess the cropped image
    preprocessed_image = preprocess_input(cropped_image)
    resized_image = cv2.resize(preprocessed_image, (224, 224))
    batched_image = np.expand_dims(resized_image, axis=0)
    
    # Make predictions on the cropped image
    predictions = model.predict(batched_image, verbose=0) #here is the print
    decoded_predictions = decode_predictions(predictions, top=1)[0]

    # Filter predictions based on confidence threshold
    filtered_predictions = [pred for pred in decoded_predictions if pred[2] > 0.55]
    
    # Prepare text for display
    label_texts = [f'{label}: {probability:.2f}' for _, label, probability in filtered_predictions]
    
    # Draw bounding box and labels on the original frame
    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    y_start = start_y - 10 if start_y > 20 else start_y + 30
    for label_text in label_texts:
        cv2.putText(image, label_text, (start_x, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
        y_start += 30
    
    if label_texts.__len__() > 0:
        return label_texts[0]
    else : return "none"
    

def stream_webcam():
    cap = cv2.VideoCapture(0)
    prev = ""
    random_labels = ['oxygen_mask', 'jersey', 'sweatshirt', 'water_bottle', 'pill_bottle', 'teddy', 'harmonica']
    active_ = 0
    label_to_find = ""
    score = 0
    while True:
        ret, frame = cap.read()
        str = run_image_recognition(frame)
        str = str[:-6]
        if (str != prev and str !=""):
            prev = str
            print(str)
            if(str == label_to_find):
                    print("Correct!")
                    active_ = 0
                    score += 1
                    print("Current score is", score)
                    prev = ""
            else:
                print("Incorrect!")

        #game code
        if (active_ == 0):
            active_ = 1
            label_to_find = random.choice(random_labels)
            print("------------Find " + label_to_find + " ------------")
                

        cv2.imshow('Webcam Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

stream_webcam()