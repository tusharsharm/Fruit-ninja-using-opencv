import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = False
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

        self.last_hand = []
        self.lock_frames = 6
        self.frames_since_seen = 0

    def find_hand(self, img, draw=True):
        img = self._enhance(img)

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        hand_landmarks = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                lm_list = []
                h, w, c = img.shape
                for id, lm in enumerate(handLms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((cx, cy))
                hand_landmarks.extend(lm_list)

                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

            self.last_hand = hand_landmarks
            self.frames_since_seen = 0
        else:
            if self.frames_since_seen < self.lock_frames:
                hand_landmarks = self.last_hand
                self.frames_since_seen += 1
            else:
                self.last_hand = []

        return hand_landmarks

    def _enhance(self, img):
        # Auto enhance contrast & brightness
        alpha = 1.8  # Contrast
        beta = 50    # Brightness
        enhanced = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return enhanced
