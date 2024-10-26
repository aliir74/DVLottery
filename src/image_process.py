import io
import logging
import os

import cv2
import dlib
import numpy as np
from PIL import Image

from consts import PROJECT_ROOT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def crop_image(image_path):
    # Load the face detector and shape predictor
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor(
        os.path.join(PROJECT_ROOT, "models", "shape_predictor_68_face_landmarks.dat")
    )

    # Read the image using OpenCV
    img = cv2.imread(image_path)
    good_image = True
    try:
        check_image_requirements(img, face_detector)
    except ValueError as e:
        if "Image background" in str(e):
            logger.warning(f"{image_path}: Image does not meet requirements. {str(e)}")
            good_image = False
        else:
            return None, False
    # Check initial resolution and resize if necessary
    max_dimension = 1200
    height, width = img.shape[:2]
    if max(height, width) > max_dimension:
        scale = max_dimension / max(height, width)
        img = cv2.resize(img, (int(width * scale), int(height * scale)))

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_detector(gray)

    if len(faces) == 0:
        logger.warning("No face detected in the image.")
        return None, False

    # Assume the largest face is the main subject
    face = max(faces, key=lambda rect: rect.width() * rect.height())

    # Get facial landmarks
    shape = shape_predictor(gray, face)
    landmarks = np.array([(p.x, p.y) for p in shape.parts()])

    # Calculate head height based on facial landmarks
    face_height = (
        landmarks[8, 1] - landmarks[27, 1]
    )  # Distance from chin to nose bridge
    head_height = int(face_height / 0.5)  # Estimate full head height (increased ratio)

    # Ensure head height is within allowed range (1 inch to 1 3/8 inches at 300 DPI)
    min_head_height, max_head_height = 300, 413
    head_height = max(min(head_height, max_head_height), min_head_height)

    # Calculate crop dimensions
    crop_height = int(
        head_height / 0.55
    )  # Head should be 65% of image height (decreased from 75%)
    crop_width = crop_height  # Square crop

    # Calculate crop coordinates
    center_x = (
        landmarks[0, 0] + landmarks[16, 0]
    ) // 2  # Midpoint between leftmost and rightmost facial landmarks
    center_y = (
        landmarks[27, 1] + (landmarks[8, 1] - landmarks[27, 1]) // 2
    )  # Midpoint between nose bridge and chin

    start_x = max(center_x - crop_width // 2, 0)
    start_y = max(center_y - crop_height // 2, 0)

    # Adjust crop coordinates if they exceed image boundaries
    start_x = min(start_x, img.shape[1] - crop_width)
    start_y = min(start_y, img.shape[0] - crop_height)

    # Crop the image
    cropped_img = img[start_y : start_y + crop_height, start_x : start_x + crop_width]

    # Resize the image if necessary
    height, width = cropped_img.shape[:2]
    if height < 600 or width < 600:
        resized_img = cv2.resize(cropped_img, (600, 600))
    elif height > 1200 or width > 1200:
        resized_img = cv2.resize(cropped_img, (1200, 1200))
    else:
        resized_img = cropped_img

    logger.info(
        f"{image_path}: Image cropped to {crop_width}x{crop_height} and resized to {resized_img.shape[1]}x{resized_img.shape[0]}"
    )

    # Convert back to PIL Image
    return Image.fromarray(cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)), good_image


def reduce_size(pil_image):
    max_size = 240 * 1024  # 240 KB in bytes
    quality = 95
    while True:
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=quality)
        if buffer.tell() <= max_size:
            break
        quality -= 5
        if quality < 30:
            logger.warning(
                "Unable to reduce image size below 240KB while maintaining acceptable quality."
            )
            break
    return pil_image


def check_image_requirements(img, face_detector):
    """
    Check if the image meets the requirements:
    1. Only one face in the image
    2. White background
    """
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_detector(gray)

    # Check for number of faces
    if len(faces) == 0:
        raise ValueError("No face detected in the image.")
    elif len(faces) > 1:
        raise ValueError("Multiple faces detected in the image.")

    # Check for white background
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range for white color in HSV
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # Create a mask for white pixels
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Calculate the percentage of white pixels
    white_pixel_count = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]
    white_percentage = (white_pixel_count / total_pixels) * 100

    if white_percentage < 50:  # Adjust this threshold as needed
        raise ValueError("Image background is not predominantly white.")

    return True


def start_process_image(image_path):
    new_image, good_image = crop_image(image_path)
    if not new_image:
        return None, False
    if not good_image:
        logger.warning(f"{image_path}: Image might not meet requirements.")
    new_image = reduce_size(new_image)
    return new_image, good_image
