import cv2
import os

def main():
    # Open the video file
    video_path = input("Please enter the path for your video(Ensure that you replace \ with double \ or /): ")

    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"Error: The file does not exist at the specified path: {video_path}")
        return
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return

    # Get the frame width, height, and frames per second (fps) from the video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'processed_video.avi')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Read the first frame
    ret, frame1 = cap.read()
    if not ret:
        print("Error: Could not read frame from video.")
        return

    # Convert the first frame to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    
    # Loop to read frames from the video
    while True:
        ret, frame2 = cap.read()
        if not ret:
            break
        
        # Convert the frame to grayscale
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
        
        # Compute the absolute difference between the current frame and the previous frame
        diff = cv2.absdiff(gray1, gray2)
        
        # Apply a binary threshold to the difference image
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        
        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw bounding boxes around the detected contours
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Write the frame with bounding boxes to the output video
        out.write(frame2)
        
        # Display the frame with bounding boxes
        cv2.imshow('Movement Detection', frame2)
        
        # Update the previous frame
        gray1 = gray2.copy()
        
        # Break the loop if the 'q' key is pressed
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    # Release the video capture and writer objects, and close all OpenCV windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Processed video saved to {output_path}")

if __name__ == "__main__":
    main()
