import cv2
import mediapipe as mp
import pyautogui
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0
click_threshold = 40 
right_click_threshold = 50 
def calculate_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
def detect_clicks(hand_landmarks):
    index_finger_tip = hand_landmarks.landmark[8]
    thumb_tip = hand_landmarks.landmark[4]
    middle_finger_tip = hand_landmarks.landmark[12]
    index_x, index_y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)
    thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
    middle_x, middle_y = int(middle_finger_tip.x * screen_width), int(middle_finger_tip.y * screen_height)
    index_thumb_distance = calculate_distance((index_x, index_y), (thumb_x, thumb_y))    
    middle_thumb_distance = calculate_distance((middle_x, middle_y), (thumb_x, thumb_y))
    if index_thumb_distance < click_threshold:
        pyautogui.click()
    elif index_thumb_distance < click_threshold / 2:
        pyautogui.doubleClick()
    elif middle_thumb_distance < right_click_threshold:
        pyautogui.rightClick()
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmarks.landmark[8]
            x = int(index_finger_tip.x * screen_width)
            y = int(index_finger_tip.y * screen_height)
            new_x = prev_x + (x - prev_x) / 5
            new_y = prev_y + (y - prev_y) / 5
            pyautogui.moveTo(new_x, new_y)
            prev_x, prev_y = new_x, new_y
            detect_clicks(hand_landmarks)
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()