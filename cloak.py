import cv2
import numpy as np

cap = cv2.VideoCapture(0)
background = None

print("Press 'b' to capture background once you're out of frame.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    key = cv2.waitKey(1)
    if key == ord('b'):
        background = frame.copy()

        print("✅ Background captured!")

    if background is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 150, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 150, 50])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)

        inverse_mask = cv2.bitwise_not(mask)

        cloak = cv2.bitwise_and(background, background, mask=mask)
        rest = cv2.bitwise_and(frame, frame, mask=inverse_mask)

        final = cv2.addWeighted(cloak, 1, rest, 1, 0)

        cv2.imshow("🧙 Invisible Cloak", final)
    else:
        cv2.imshow("🧙 Invisible Cloak", frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()