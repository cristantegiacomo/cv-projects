import cv2

CASCADE_FILE = 'haarcascade_frontalface_default.xml'

SCALE_FACTOR = 1.5
MIN_NEIGHBORS = 4

RECT_COLOR = (0, 0, 255)  # Rosso BGR
RECT_THICKNESS = 9

ESC_KEY = 27

# Carica in RAM il file XML: database addestrato contenente le regole per riconoscere visi frontali
face_cascade = cv2.CascadeClassifier(CASCADE_FILE)

# Apre lo stream hardware della fotocamera. Lo 0 indica la webcam predefinita del sistema
webcam = cv2.VideoCapture(0)

while True:
    # Cattura il singolo frame istantaneo:
    # ret: booleano, indica se la lettura hardware è andata a buon fine; img: matrice dell'immagine
    ret , img = webcam.read()
    if not ret:
        print("Errore: impossibile leggere dal webcam")
        break

    # Converte il frame in scala di grigi. Lavorare su 1 canale colore invece di 3 velocizza enormemente il calcolo
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    
    # Ricerca i volti ridimensionando l'immagine finché non combaciano con il filtro di ricerca (Piramide delle Immagini)
    # - 1.5 (Scale Factor): rimpicciolisce la foto del 50% a ogni ciclo (molto veloce, ma rischia di "saltare" la misura corretta)
    # - 4 (Min Neighbors): richiede almeno 4 risultati sovrapposti per confermare la faccia (evita falsi positivi)
    # faces è un array contenente coordinate di len(faces) volti
    faces = face_cascade.detectMultiScale(gray, SCALE_FACTOR, MIN_NEIGHBORS)
    
    # NB: l'origine (0,0) è in alto a sinistra e l'asse Y cresce verso il BASSO
    for (x,y,w,h) in faces:
        # - (x,y): angolo in alto a sinistra
        # - (x+w, y+h): angolo in basso a destra
        # cv2.rectangle() modifica img sovrapponendo i rispettivi pixel con quelli del rettangolo
        cv2.rectangle(img, (x,y), (x+w, y+h), RECT_COLOR, RECT_THICKNESS)
    cv2.imshow("Face detection", img)

    key = cv2.waitKey(10)
    if key == ESC_KEY: break

webcam.release()
cv2.destroyAllWindows()