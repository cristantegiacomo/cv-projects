# Eye Tracker

Un sistema di tracciamento oculare in tempo reale che permette di muovere il cursore del mouse con gli occhi ed effettuare il click tramite l'ammiccamento delle palpebre. Sviluppato in Python utilizzando OpenCV, PyAutoGUI e la Tasks API di MediaPipe.

## Come funziona

Lo script analizza il flusso video della webcam per tracciare in tempo reale i dettagli del volto:
* **Movimento cursore:** Traccia i landmark dell'iride e ne mappa la posizione in modo proporzionale alla risoluzione dello schermo.
* **Click del mouse:** Calcola la distanza verticale tra la palpebra superiore e quella inferiore. Quando le palpebre si avvicinano, viene attivato il click sinistro.

## Installazione

Installa le librerie necessarie:
   ```bash
   pip install opencv-python mediapipe pyautogui