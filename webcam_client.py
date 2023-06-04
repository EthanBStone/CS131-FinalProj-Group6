import cv2
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import requests
import time
import threading

model = MobileNetV2(weights='imagenet')


tag = "1"
active_ = True
prev = ""
new_label = False

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
    

def getUpdate():
    #globals
    global tag
    global active_
    #globals
    s = tag
    while (active_ == True):
        time.sleep(1.5)
        r = requests.get(f"http://{ip}:5000/playerUpdate?data={s}")
        if (r.text != ""): print(f"Response: {r.text}")


def sendLabel():
    #globals
    global tag
    global active_
    global prev
    global new_label
    while (active_ == True):
        time.sleep(1.5)
        if (new_label):
            s = tag + prev
            r = requests.get(f"http://{ip}:5000/playerInput?data={s}")
            new_label = False
            if (r.text != ""): print(f"Response: {r.text}")


if __name__ == "__main__":
    #Get ip address
    ip = input("Select what network you are connecting to\n1)Local\n2)Online\n")
    if ip == "1" :
        ip = "127.0.0.1"
    else :
        ip = input("input the ip address you are connecting to ie 127.0.0.1")        
    tag = input("Enter your player number, 1 or 2\n")
    temp = tag + "here"
    requests.get(f"http://{ip}:5000/playerInput?data={temp}")
    t1 = threading.Thread(target=getUpdate)
    t1.start()
    t2 = threading.Thread(target=sendLabel)
    t2.start()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        str = run_image_recognition(frame)
        str = str[:-6]
        if (str != prev and str !=""):
            prev = str
            new_label = True
            print("Object you found is: " + str)

        cv2.imshow('Webcam Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    active_ = False
    t1.join()
    t2.join()
    requests.get(f"http://{ip}:5000/playerInput?data={temp}")
    cap.release()
    cv2.destroyAllWindows()
