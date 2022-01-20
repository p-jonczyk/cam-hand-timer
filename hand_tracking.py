import cv2 as cv
import mediapipe as mp


class handDetector():

    def __init__(self, mode=False, max_hands=2):
        # static mode
        self.mode = mode
        self.max_hands = max_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.mode, self.max_hands)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """Track hands of video"""

        # convert colors to RGB since 'hands' only takes RGB
        img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # get detection
        self.results = self.hands.process(img_rgb)
        # if hands are detected - multi_hand_landmarks output of hands landmarks
        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_landmark, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_number=0):
        """Get list of positions of hand's landmarks"""

        landmark_list = []

        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id, landmark in enumerate(my_hand.landmark):
                height, width, channel = img.shape
                # make it form decimal to int(pixels)
                pos_x, pos_y = int(
                    landmark.x * width), int(landmark.y * height)
                landmark_list.append([id, pos_x, pos_y])
        return landmark_list


def main():

    cap = cv.VideoCapture(0)
    detector = handDetector()

    while True:
        _, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[4])
        cv.imshow('Camera', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
