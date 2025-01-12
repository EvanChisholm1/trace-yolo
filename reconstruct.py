import cv2
import os
from natsort import natsorted  # Optional, for natural sorting

def images_to_video(image_dir, output_file, frame_rate=30):
    """
    Stitches images from a directory into a video.

    Args:
        image_dir (str): Path to the directory containing images.
        output_file (str): Path for the output video file.
        frame_rate (int): Frames per second for the video.
    """
    # Get all image file paths in the directory
    images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images = natsorted(images)  # Sort the images naturally

    if not images:
        print("No images found in the directory!")
        return

    # Read the first image to get frame dimensions
    first_image = cv2.imread(images[0])
    height, width, _ = first_image.shape

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 format
    video_writer = cv2.VideoWriter(output_file, fourcc, frame_rate, (width, height))

    for img_path in images:
        img = cv2.imread(img_path)

        # Resize the image to match the first frame's dimensions, if needed
        if (img.shape[1], img.shape[0]) != (width, height):
            img = cv2.resize(img, (width, height))

        video_writer.write(img)  # Add the frame to the video

    video_writer.release()
    print(f"Video saved to {output_file}")

# Usage example
if __name__ == "__main__":
    image_directory = "./out"  # Replace with your image directory path
    output_video = "reconstructed.mp4"       # Replace with your desired output video file name
    images_to_video(image_directory, output_video, frame_rate=30)