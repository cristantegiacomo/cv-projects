# Face Detection

Uno script in Python per il rilevamento di volti frontali in tempo reale tramite webcam, sviluppato utilizzando OpenCV e i classificatori a cascata di Haar.

## Come funziona

Lo script analizza il flusso video della webcam in tempo reale:
* **Elaborazione frame:** Converte ogni frame in scala di grigi per ottimizzare le prestazioni della ricerca.
* **Rilevamento volti:** Utilizza il modello `haarcascade_frontalface_default.xml` e la piramide delle immagini per individuare i volti.
* **Visualizzazione:** Disegna un rettangolo rosso attorno a ciascun volto rilevato a schermo.

## Installazione

Installa la libreria necessaria:
   ```bash
    pip install opencv-python