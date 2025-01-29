import cv2
from ultralytics import YOLO
import argparse

# import os
# os.environ['QT_QPA_PLATFORM'] = 'xcb'

def predict(camera_id=0):

    # Load the model 
    model = YOLO("ncnn_model", task='segment')

    # Open video stream
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print("Error: No Camera Found. Please Change the Camera ID")
        exit()

    # w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    # print(f"Camera: Width={w}, Height={h}, FPS={fps}")

    frame_skip_interval = 30
    frame_counter = 0

    # Real-time detection
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        if frame_counter % frame_skip_interval != 0:
            frame_counter += 1
            continue

        # Run prediction on the frame
        results = model.predict(source=frame, show=False, save=False, conf=0.5)

        # Visualize the predictions on the frame
        annotated_frame = results[0].plot()  

        # Resize Frame For Visualization
        width = 1000
        aspect_ratio = frame.shape[1] / frame.shape[0]  # width / height
        new_height = int(width / aspect_ratio)
        resized_frame = cv2.resize(annotated_frame, (width, new_height))
        cv2.imshow("Component Identification Detection", resized_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Component Identification")
    parser.add_argument('--camera_id', type=int, default=0, help="ID of the Camera")

    # Parse the arguments
    args = parser.parse_args()
    predict(camera_id=args.camera_id)
