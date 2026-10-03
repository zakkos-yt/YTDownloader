# YTDownloader

YTDownloader è una semplice applicazione grafica basata su `yt-dlp` e `CustomTkinter` che permette di scaricare contenuti da YouTube in formato **MP3** o **MP4**.

Questo repository è un fork del progetto originale di Kerlooo, modificato per aggiungere:

- supporto al download video in MP4
- gestione di FFmpeg
- compatibilità verificata su Windows 11 e Linux
- alcune correzioni relative all'interfaccia grafica

## Funzioni

- Download audio in MP3
- Download video in MP4
- Scelta della qualità MP3
- Interfaccia grafica semplice
- Cartella di destinazione configurabile
- Supporto multilingua
- Utilizzo di `ffmpeg` e `ffprobe` per conversione e unione dei flussi

---

# Installazione su Linux

Testato su LMDE 7 / Debian 13.

Clonare il repository:

```bash
git clone https://github.com/zakkos-yt/YTDownloader.git
cd YTDownloader
```

Installare i pacchetti di sistema necessari:

```bash
sudo apt update
sudo apt install python3-tk ffmpeg
```

`python3-tk` è necessario per l'interfaccia grafica basata su Tkinter.

`ffmpeg` e `ffprobe` sono necessari per la conversione audio e per l'unione dei flussi video e audio nei download MP4.

Creare un ambiente virtuale:

```bash
python3 -m venv ytvenv
```

Attivarlo:

```bash
source ytvenv/bin/activate
```

Installare le dipendenze Python:

```bash
python -m pip install -r requirements.txt
```

Avviare il programma:

```bash
python app.py
```

## Nota su FFmpeg in Linux

Su Linux FFmpeg viene normalmente installato a livello di sistema:

```text
/usr/bin/ffmpeg
/usr/bin/ffprobe
```

`yt-dlp` può quindi trovarlo automaticamente tramite il `PATH`.
