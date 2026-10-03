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

Se in `app.py` è presente questa riga:

```python
"ffmpeg_location": BASE_DIR,
```

su Linux va commentata o rimossa.

In caso contrario `yt-dlp` cercherà `ffmpeg` nella cartella del programma invece di utilizzare quello installato nel sistema.

---

# Installazione su Windows 11

Installare Python dal sito ufficiale:

https://www.python.org/downloads/windows/

Durante l'installazione è consigliato selezionare:

```text
Add Python to PATH
```

Clonare il repository:

```powershell
git clone https://github.com/zakkos-yt/YTDownloader.git
cd YTDownloader
```

Creare l'ambiente virtuale:

```powershell
py -m venv myenv
```

Se PowerShell impedisce l'attivazione dell'ambiente virtuale:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

Attivare il virtual environment:

```powershell
.\myenv\Scripts\Activate.ps1
```

Installare le dipendenze:

```powershell
python -m pip install -r requirements.txt
```

È consigliato utilizzare:

```powershell
python -m pip
```

invece del semplice comando `pip`, perché alcune configurazioni di sicurezza di Windows possono bloccare direttamente `pip.exe`.

---

# FFmpeg su Windows

Scaricare una build Windows di FFmpeg da:

https://www.gyan.dev/ffmpeg/builds/

La versione `ffmpeg-release-essentials.zip` è sufficiente.

Estrarre:

```text
ffmpeg.exe
ffprobe.exe
```

e copiarli nella cartella principale del programma, accanto ad `app.py`.

La struttura sarà quindi simile a questa:

```text
YTDownloader/
├── app.py
├── ffmpeg.exe
├── ffprobe.exe
├── settings.py
├── settings.json
└── ...
```

Su Windows può essere utilizzata questa impostazione in `app.py`:

```python
"ffmpeg_location": BASE_DIR,
```

In questo modo `yt-dlp` cercherà `ffmpeg.exe` e `ffprobe.exe` direttamente nella cartella del programma.

Windows può mostrare un avviso di sicurezza per `ffmpeg.exe` o `ffprobe.exe`.

Se i file sono stati scaricati dalla fonte indicata sopra, possono essere sbloccati dalle proprietà del file oppure tramite PowerShell:

```powershell
Unblock-File .\ffmpeg.exe
Unblock-File .\ffprobe.exe
```

Avviare quindi il programma:

```powershell
python app.py
```

---

# Differenze tra Windows e Linux

## Linux

FFmpeg è normalmente installato a livello di sistema:

```text
/usr/bin/ffmpeg
/usr/bin/ffprobe
```

Non è quindi necessario specificare:

```python
"ffmpeg_location": BASE_DIR,
```

## Windows

FFmpeg può essere copiato direttamente nella cartella del programma:

```text
ffmpeg.exe
ffprobe.exe
```

In questo caso può essere utilizzato:

```python
"ffmpeg_location": BASE_DIR,
```

---

# Note

I file:

```text
ffmpeg.exe
ffprobe.exe
```

non sono inclusi nel repository GitHub e devono essere scaricati separatamente.

L'applicazione utilizza `yt-dlp` come motore di download e FFmpeg per le operazioni di conversione e muxing.

---

# Crediti

Questo progetto è un fork di:

Kerlooo/YTDownloader

Modifiche principali di questo fork:

- supporto MP4
- correzioni per Windows
- compatibilità Linux
- gestione FFmpeg
- documentazione aggiornata
