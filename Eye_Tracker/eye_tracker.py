import cv2 
import mediapipe as mp # Motore IA per il riconoscimento dei landmark facciali
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
import pyautogui # Controllo del sistema operativo per movimento mouse e clic

IRIS_START_ID = 474
IRIS_END_ID = 478
CURSOR_IRIS_INDEX = 1 
LOWER_EYELID_ID = 145 
UPPER_EYELID_ID = 159     
ESC_KEY = 27            
RED = (0, 0, 255)  
YELLOW = (0, 255, 255) 

# Inizializza il detector caricando il modello in memoria
# Imposta la modalità su IMAGE (più adatta per l'analisi frame-by-frame isolata) e limita la ricerca a 1 volto
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='face_landmarker.task'),
    running_mode=RunningMode.IMAGE,
    num_faces=1
)
landmarker = FaceLandmarker.create_from_options(options)

cam = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size() # Estrae le dimensioni totali in pixel del tuo monitor tramite call SO

while True:
    ret, image = cam.read()
    if not ret:
        break
    image = cv2.flip(image, 1) # Specchia orizzontalmente l'immagine
    window_h, window_w, _ = image.shape 
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converte l'immagine da BGR (OpenCV) a RGB (MediaPipe)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)   # Conversione immagine nel formato strutturato richiesto da mediapipe
    
    result = landmarker.detect(mp_image)    # result contiene coordinate del volto

    if result.face_landmarks:   # Se è stato trovato un volto
        one_face_landmarks = result.face_landmarks[0] # Isola i punti del primo e unico volto

        # I landmark dal 474 al 477 descrivono il contorno dell'iride
        for id, landmark_point in enumerate(one_face_landmarks[IRIS_START_ID : IRIS_END_ID]):
            x = int(landmark_point.x * window_w)
            y = int(landmark_point.y * window_h)
            
            if id == 1:   # Utilizza uno dei punti specifici dell'iride (il secondo dell'array, id == 1) per il puntatore
                mouse_x = int(screen_w / window_w * x) # Proporzione: scala la X dalla webcam allo schermo
                mouse_y = int(screen_h / window_h * y) # Proporzione: scala la Y dalla webcam allo schermo
                pyautogui.moveTo(mouse_x, mouse_y) 
            
            cv2.circle(image, (x, y), 3, RED)

        # I punti 145 e 159 corrispondono rispettivamente alla palpebra inferiore e superiore dell'occhio sinistro
        left_eye = [one_face_landmarks[LOWER_EYELID_ID], one_face_landmarks[UPPER_EYELID_ID]]
        for landmark_point in left_eye:
            x = int(landmark_point.x * window_w)
            y = int(landmark_point.y * window_h)
            cv2.circle(image, (x, y), 3, YELLOW)

        dist = left_eye[0].y - left_eye[1].y
        if (dist < 0.02):
            pyautogui.click()
            pyautogui.sleep(2) # Ferma l'esecuzione per 2 secondi per evitare raffiche di clic involontari
            print('mouse clicked')

    cv2.imshow("Eye controlled mouse", image)
    key = cv2.waitKey(100)
    if key == ESC_KEY:
        break

cam.release()
cv2.destroyAllWindows()