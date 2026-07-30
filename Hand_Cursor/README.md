# Hand Gesture Mouse Controller

Un controller per mouse basato su computer vision che permette di muovere il cursore e cliccare usando i movimenti della mano. Scritto in Python utilizzando OpenCV e la Tasks API di MediaPipe.

## Come funziona

Lo script analizza il flusso della webcam in tempo reale per tracciare i movimenti della mano:
* **Movimento:** La punta dell'indice controlla la posizione del cursore a schermo.
* **Click:** Avvicinando pollice e indice viene simulato il click sinistro.

## Installazione

Installa le librerie necessarie:
   ```bash
   pip install opencv-python mediapipe pyautogui