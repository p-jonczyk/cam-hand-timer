import cv2 as cv
import hand_tracking


def get_fingers_rh_list(landmarks_list: list) -> list:
    """"Creates list of fingers of right hand and returns it

    1/0 - shown/not shown """
    finger_ids = [4, 8, 12, 16, 20]

    if len(landmarks_list) != 0:
        fingers = []

        # Thumb
        if landmarks_list[finger_ids[0]][1] > landmarks_list[finger_ids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # four fingers
        for id in range(1, 5):
            if landmarks_list[finger_ids[id]][2] < landmarks_list[finger_ids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def count_fingers(img, landmarks_list: list) -> None:
    """Count and display number of shown fingers

    Parameters:

    img -> input video

    landmarks_list -> list of hand landmarks"""

    fingers = get_fingers_rh_list(landmarks_list)
    if fingers:
        finger_count = fingers.count(1)

        cv.putText(img, f'{finger_count}', (600, 50),
                   cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)


def main():
    cap = cv.VideoCapture(0)
    while(True):
        _, img = cap.read()
        detector = hand_tracking.handDetector()

        img = detector.find_hands(img)
        landmarks_list = detector.find_position(img)
        count_fingers(img, landmarks_list)
        cv.imshow('Camera', img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
