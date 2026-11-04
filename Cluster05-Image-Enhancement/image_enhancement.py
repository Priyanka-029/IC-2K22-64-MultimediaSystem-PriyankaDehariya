
import cv2
import numpy as np

# Load the input image
image = cv2.imread("input.jpg")

if image is None:
    print("Error: Image not found!")
else:
    # Improve brightness and contrast using CLAHE
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    enhanced_l = clahe.apply(l)

    enhanced_lab = cv2.merge((enhanced_l, a, b))
    enhanced = cv2.cvtColor(
        enhanced_lab, cv2.COLOR_LAB2BGR
    )

    # Improve sharpness
    blurred = cv2.GaussianBlur(
        enhanced, (0, 0), 2
    )
    sharpened = cv2.addWeighted(
        enhanced, 1.5, blurred, -0.5, 0
    )

    # Save the enhanced image
    cv2.imwrite("enhanced_image.jpg", sharpened)

    # Display original and enhanced images
    cv2.imshow("Original Image", image)
    cv2.imshow("Enhanced Image", sharpened)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Image enhancement completed!")
