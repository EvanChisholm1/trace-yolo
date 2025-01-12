import cv2
import os
from datetime import datetime

def extract_frames(video_path, output_folder=None, frame_interval=1):
    """
    Extract frames from a video file.
    
    Args:
        video_path (str): Path to the video file
        output_folder (str): Directory to save the frames (default: creates a new folder)
        frame_interval (int): Extract every nth frame (default: 1 = extract all frames)
    
    Returns:
        str: Path to the output folder
    """
    # Create output folder if not specified
    if output_folder is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder = f"frames_{timestamp}"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Initialize frame counter
    count = 0
    saved_count = 0
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {frame_count}")
    
    while True:
        # Read the next frame
        success, frame = video.read()
        
        if not success:
            break
        
        # Save frame if it matches the interval
        if count % frame_interval == 0:
            frame_path = os.path.join(output_folder, f"frame_{saved_count:06d}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1
            
        count += 1
        
        # Print progress every 100 frames
        if count % 100 == 0:
            print(f"Processed {count}/{frame_count} frames")
    
    # Clean up
    video.release()
    
    print(f"\nExtraction complete!")
    print(f"Saved {saved_count} frames to: {output_folder}")
    
    return output_folder

# Example usage
if __name__ == "__main__":
    video_path = "me.mp4"  # Replace with your video path
    output_folder = extract_frames(
        video_path,
        output_folder="./imgs",
        frame_interval=1  # Extract one frame every second (assuming 30fps video)
    )