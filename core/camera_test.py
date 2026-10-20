import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("StoneAI Camera", frame)

    key = cv2.waitKey(1)

    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()