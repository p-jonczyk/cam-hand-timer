import cv2 as cv
import hand_tracking
from fingers_count import get_fingers_rh_list
import time
import random


def get_choice(img, landmarks_list: list, draw=True) -> str:
    """Define showed choice: rock, paper or scissors and display it

    Parameters:

    img -> input video

    landmarks_list (list) -> list of hand landmarks

    draw (bool) -> True for drawing choice onto video"""

    scissors = [0, 1, 1, 0, 0]

    if len(landmarks_list) != 0:
        fingers = get_fingers_rh_list(landmarks_list)
        fingers_count = fingers.count(1)

        if fingers_count == 0:
            choice = "ROCK"
        elif fingers_count == 5:
            choice = "PAPER"
        elif fingers == scissors:
            choice = "SCISSORS"
        else:
            choice = "undefined"
        if draw:
            cv.putText(img, f'YOU: {choice}', (370, 50),
                       cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        return choice


def get_com_choice() -> str:
    """Randomly make computer choice: rock, paper, scissors """

    choices = ['ROCK', 'PAPER', 'SCISSORS']
    choice = random.choice(choices)
    return choice


def get_result(palyer_choice: str, com_choice: str):
    """Gets result of the game"""
    win_res = 'YOU WON !'
    lose_res = 'YOU LOSE !'
    if palyer_choice == com_choice:
        result = "DRAW"
    elif palyer_choice == 'ROCK':
        if com_choice == 'SCISSORS':
            result = win_res
        else:
            result = lose_res
    elif palyer_choice == 'PAPER':
        if com_choice == 'ROCK':
            result = win_res
        else:
            result = lose_res
    elif palyer_choice == 'SCISSORS':
        if com_choice == 'PAPER':
            result = win_res
        else:
            result = lose_res
    return result


def main():

    TIMER = 5
    cap = cv.VideoCapture(0)
    prev_time = 0
    sec = 0

    while(True):
        _, img = cap.read()
        detector = hand_tracking.handDetector()
        img = detector.find_hands(img, draw=False)
        landmarks_list = detector.find_position(img)
        player = get_choice(img, landmarks_list)
        # get timer - how many sec passed from star of running
        curr_time = int(time.time())
        if curr_time - prev_time == 1:
            sec += 1
        prev_time = curr_time

        # show timer
        if sec <= TIMER:
            cv.putText(img, f'{TIMER - sec}', (300, 110),
                       cv.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)

        try:
            if sec == TIMER+1:
                # get comp choice
                com_choice = get_com_choice()
                # remember player choice
                player_choice = player

            elif sec > TIMER+1:
                # show computer choice
                cv.putText(img, f'COM: {com_choice}', (20, 50),
                           cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                # get result of game
                result = get_result(player_choice, com_choice)
                # show result
                cv.putText(img, f'{result}', (180, 120),
                           cv.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 3)
        except UnboundLocalError:
            print("You did not choose anything")
            break

        cv.imshow('Camera', img)

        # press 'q' to quit
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
