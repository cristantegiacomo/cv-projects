import cv2
import mediapipe as mp # AI per riconoscere le mani
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions # vision contiene il "motore" per trovare la mano (coordinate,...)
import pyautogui # Permette a Python di muovere il mouse e click

ESC_KEY = 27
INDEX_FINGER_ID = 8
THUMB_ID = 4
CLICK_THRESHOLD = 50
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

base_options = BaseOptions(model_asset_path='hand_landmarker.task') # Indica il percorso del file con le istruzioni per riconoscere le mani
options = HandLandmarkerOptions(base_options=base_options, num_hands=1) # Limita la ricerca a una sola mano
detector = HandLandmarker.create_from_options(options) # Avvia il motore di ricerca delle mani utilizzando le opzioni impostate

screen_width, screen_height = pyautogui.size() # Rileva dimensioni dello schermo del computer tramite call con SO
camera = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 = 0 # Variabili a zero per memorizzare la posizione delle dita

while True:
    ret, image = camera.read()
    if not ret:
        break
        
    image_height, image_width, _ = image.shape  # Rileva altezza e larghezza del video della webcam
    image = cv2.flip(image, 1)     # Ribalta l'immagine a specchio per coordinare i movimenti del mouse
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)     # Converte i colori dell'immagine nel formato richiesto da mediapipe
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)     # Preparazione immagine nel formato specifico richiesto da mediapipe
    
    detection_result = detector.detect(mp_image)     # Analizza l'immagine per cercare la presenza di una mano
    
    if detection_result.hand_landmarks:     # Procede solo se viene effettivamente rilevata almeno una mano
        for hand_landmarks in detection_result.hand_landmarks:         # Analizza i dati della mano trovata (ciclo viene eseguito 1 volta perché num_hands=1)
            
            # Disegna dei punti verdi sulle articolazioni della mano
            for landmark in hand_landmarks:
                x_lm = int(landmark.x * image_width)
                y_lm = int(landmark.y * image_height)
                cv2.circle(image, (x_lm, y_lm), 2, GREEN, -1)   # radius: 2; #fill_circle (not empty): -1

            # Analizza tutti i 21 punti della mano [0,20]
            for id, lm in enumerate(hand_landmarks):
                # Calcola il pixel esatto del video in cui si trova il punto
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                
                if id == INDEX_FINGER_ID:     # Verifica se il punto analizzato è la punta dell'INDICE (ID 8)
                    # Calcola le coordinate proporzionate per lo schermo intero
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, YELLOW, -1)
                    pyautogui.moveTo(mouse_x, mouse_y)  # Sposta fisicamente il cursore del mouse sul monitor

                    # Memorizza la posizione dell'indice per il calcolo del click
                    x1 = x
                    y1 = y
                    
                if id == THUMB_ID:     # Verifica se il punto analizzato è la punta del POLLICE (ID 4)
                    # Memorizza la posizione del pollice
                    x2 = x
                    y2 = y
                    cv2.circle(image, (x, y), 10, YELLOW, -1)
            
            dist = y2 - y1
            if dist < CLICK_THRESHOLD:
                pyautogui.click()
                
    cv2.imshow("Hand movement video capture", image)
    
    key = cv2.waitKey(10) 
    if key == ESC_KEY: 
        break

camera.release()
cv2.destroyAllWindows()