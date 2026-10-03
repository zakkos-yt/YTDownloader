# YTDownloader

YTDownloader è una semplice applicazione grafica basata su `yt-dlp` e `CustomTkinter` che permette di scaricare contenuti da YouTube in formato **MP3** o **MP4**.

Questo repository è un fork del progetto originale di Kerlooo, modificato per aggiungere:

- supporto al download video in MP4;
- gestione automatica di FFmpeg su Windows e Linux;
- compatibilità verificata su Windows 11 e LMDE 7 / Debian 13;
- correzioni relative all'interfaccia grafica.

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

Testato su **LMDE 7 / Debian 13**.

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

## FFmpeg su Linux

Su Linux FFmpeg viene normalmente installato a livello di sistema, ad esempio:

```text
/usr/bin/ffmpeg
/usr/bin/ffprobe
```

La versione attuale di `app.py` rileva automaticamente FFmpeg tramite il `PATH` di sistema. Non è quindi necessario modificare o commentare manualmente alcuna riga del codice.

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

È consigliato utilizzare `python -m pip` invece del semplice comando `pip`, perché alcune configurazioni di sicurezza di Windows possono bloccare direttamente `pip.exe`.

Avviare il programma:

```powershell
python app.py
```

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

Esempio:

```text
YTDownloader/
├── app.py
├── ffmpeg.exe
├── ffprobe.exe
├── settings.py
├── settings.json
└── ...
```

La versione attuale di `app.py` gestisce FFmpeg automaticamente:

1. cerca prima `ffmpeg` nel `PATH` di sistema;
2. se non lo trova e il sistema è Windows, cerca `ffmpeg.exe` nella stessa cartella di `app.py`.

Non è quindi necessario modificare il codice passando da Windows a Linux o viceversa.

Windows può mostrare un avviso di sicurezza per `ffmpeg.exe` o `ffprobe.exe`.

Se i file sono stati scaricati dalla fonte indicata sopra, possono essere sbloccati dalle proprietà del file oppure tramite PowerShell:

```powershell
Unblock-File .\ffmpeg.exe
Unblock-File .\ffprobe.exe
```

---

# Come viene rilevato FFmpeg

Il programma usa `shutil.which("ffmpeg")` per cercare automaticamente FFmpeg nel `PATH`.

Se viene trovato, utilizza la cartella dell'eseguibile rilevato.

Su Linux questo normalmente porta a:

```text
/usr/bin
```

Su Windows, se FFmpeg non è presente nel `PATH`, il programma verifica se esiste:

```text
ffmpeg.exe
```

nella stessa cartella di `app.py` e, in quel caso, usa direttamente quella directory.

Questo permette di mantenere **un solo `app.py` cross-platform**, senza dover usare versioni separate per Windows e Linux.

---

# Note

I file:

```text
ffmpeg.exe
ffprobe.exe
```

non sono inclusi nel repository GitHub e devono essere scaricati separatamente su Windows, salvo che FFmpeg sia già installato e disponibile nel `PATH`.

Su Linux è sufficiente installare il pacchetto `ffmpeg` tramite il gestore pacchetti della distribuzione.

L'applicazione utilizza `yt-dlp` come motore di download e FFmpeg per le operazioni di conversione e muxing.

---

# Crediti

Questo progetto è un fork di:

**Kerlooo/YTDownloader**

Modifiche principali di questo fork:

- supporto MP4;
- correzioni per Windows;
- compatibilità Linux;
- rilevamento automatico di FFmpeg;
- documentazione aggiornata.
