import cv2
import numpy as np


def calculate_quality(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    sharpness = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    score = min(
        round(sharpness / 100, 1),
        10
    )

    return max(score, 1)