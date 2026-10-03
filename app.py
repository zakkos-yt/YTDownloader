import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
import yt_dlp
import threading
import json
import os
import shutil
from settings import open_settings
from translations import t, DEFAULT_LANG

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Rilevamento automatico di FFmpeg:
# - Linux/macOS: usa l'eseguibile disponibile nel PATH di sistema.
# - Windows: se FFmpeg non è nel PATH, prova a usare ffmpeg.exe e ffprobe.exe
#   presenti nella stessa cartella di app.py.
ffmpeg_executable = shutil.which("ffmpeg")

if ffmpeg_executable:
    FFMPEG_DIR = os.path.dirname(ffmpeg_executable)
elif os.name == "nt" and os.path.exists(os.path.join(BASE_DIR, "ffmpeg.exe")):
    FFMPEG_DIR = BASE_DIR
else:
    FFMPEG_DIR = None

with open(os.path.join(BASE_DIR, "settings.json"), "r") as settings_file:
    settings = json.load(settings_file)


def download(app, lang, link, quality, file_format, progress_hook, on_success, on_error):

    with open(os.path.join(BASE_DIR, "settings.json"), "r") as settings_file:
        current_settings = json.load(settings_file)

    output_path = current_settings["output_folder"]

    if not os.path.isabs(output_path):
        output_path = os.path.join(BASE_DIR, output_path)

    try:
        os.makedirs(output_path, exist_ok=True)
    except OSError:
        app.after(
            0,
            lambda: on_error(
                t(lang, "error_folder", path=output_path)
            ),
        )
        return

    # ---------------------------------------------------------
    # MP3
    # ---------------------------------------------------------

    if file_format == "MP3":

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(
                output_path,
                "%(title)s.%(ext)s"
            ),
            "progress_hooks": [progress_hook],

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                }
            ],
        }

        if FFMPEG_DIR:
            ydl_opts["ffmpeg_location"] = FFMPEG_DIR

    # ---------------------------------------------------------
    # MP4
    # ---------------------------------------------------------

    else:

        ydl_opts = {
            # Video MP4 migliore + audio M4A migliore.
            # Se non disponibili insieme, prova un MP4 completo.
            "format":
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]"
                "/best[ext=mp4]"
                "/best",

            "merge_output_format": "mp4",

            "outtmpl": os.path.join(
                output_path,
                "%(title)s.%(ext)s"
            ),

            "progress_hooks": [progress_hook],

        }

        if FFMPEG_DIR:
            ydl_opts["ffmpeg_location"] = FFMPEG_DIR

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        app.after(0, on_success)

    except Exception as e:

        app.after(
            0,
            lambda e=e: on_error(str(e))
        )


def on_download(
    app,
    lang,
    link_input,
    quality_var,
    format_var,
    download_btn,
    progress_frame,
    progress_bar,
    status_label,
):

    link = link_input.get()
    quality = quality_var.get()
    file_format = format_var.get()

    if link == "":
        CTkMessagebox(
            title=t(lang, "warning_title"),
            message=t(lang, "warning_no_link"),
            icon="warning",
        )
        return

    download_btn.configure(state="disabled")

    progress_bar.set(0)

    status_label.configure(
        text=t(lang, "status_start")
    )

    progress_frame.grid()

    def progress_hook(d):

        if d["status"] == "downloading":

            total = (
                d.get("total_bytes")
                or d.get("total_bytes_estimate")
            )

            done = d.get("downloaded_bytes", 0)

            frac = done / total if total else 0

            app.after(
                0,
                lambda f=frac: (
                    progress_bar.set(f),
                    status_label.configure(
                        text=t(
                            lang,
                            "status_downloading",
                            pct=int(f * 100),
                        )
                    ),
                ),
            )

        elif d["status"] == "finished":

            app.after(
                0,
                lambda: (
                    progress_bar.set(1),
                    status_label.configure(
                        text=t(lang, "status_converting")
                    ),
                ),
            )

    def reset_ui():

        download_btn.configure(state="normal")
        status_label.configure(text="")
        progress_frame.grid_remove()

    def on_success():

        reset_ui()

        CTkMessagebox(
            title=t(lang, "done_title"),
            message=t(lang, "done_msg"),
            icon="check",
            width=400,
        )

    def on_error(msg):

        reset_ui()

        CTkMessagebox(
            title=t(lang, "error_title"),
            message=t(lang, "error_msg", msg=msg),
            icon="cancel",
            width=400,
        )

    thread = threading.Thread(
        target=download,
        args=(
            app,
            lang,
            link,
            quality,
            file_format,
            progress_hook,
            on_success,
            on_error,
        ),
        daemon=True,
    )

    thread.start()


def main():

    app = ctk.CTk()

    # NON usare withdraw().
    # Sul tuo sistema impediva alla finestra di apparire.
    # app.withdraw()

    screen_w = app.winfo_screenwidth()
    screen_h = app.winfo_screenheight()

    scale_factor = (
        min(screen_w / 1920, screen_h / 1080)
        if screen_w > 0 and screen_h > 0
        else 1
    )

    scale_factor = max(
        0.6,
        min(scale_factor, 1.6)
    )

    ctk.set_widget_scaling(scale_factor)

    app.title("YT Downloader")

    try:
        app._icon = tk.PhotoImage(
            file=os.path.join(BASE_DIR, "icon.png")
        )
        app.iconphoto(True, app._icon)

    except Exception:
        pass

    state = {
        "lang": settings.get(
            "language",
            DEFAULT_LANG
        )
    }

    title_font = ctk.CTkFont(
        family="Segoe UI",
        size=20,
        weight="bold",
    )

    normal_font = ctk.CTkFont(
        family="Segoe UI",
        size=13,
    )

    app.columnconfigure(0, weight=1)

    app.rowconfigure(0, weight=1)
    app.rowconfigure(7, weight=1)

    # ---------------------------------------------------------
    # Titolo
    # ---------------------------------------------------------

    title_label = ctk.CTkLabel(
        app,
        text="",
        font=title_font,
    )

    title_label.grid(
        row=1,
        column=0,
        pady=(10, 20),
    )

    # ---------------------------------------------------------
    # Link + download
    # ---------------------------------------------------------

    input_frame = ctk.CTkFrame(
        app,
        fg_color="transparent",
    )

    input_frame.grid(
        row=2,
        column=0,
        pady=(0, 15),
    )

    link_input = ctk.CTkEntry(
        input_frame,
        font=normal_font,
        width=360,
    )

    link_input.pack(
        side="left",
        padx=(0, 10),
    )

    # ---------------------------------------------------------
    # Variabili
    # ---------------------------------------------------------

    quality_var = ctk.StringVar(
        value=settings["default_quality"]
    )

    format_var = ctk.StringVar(
        value="MP3"
    )

    # ---------------------------------------------------------
    # Pulsante Download
    # ---------------------------------------------------------

    download_btn = ctk.CTkButton(
        input_frame,
        width=90,
        font=normal_font,
        command=lambda: on_download(
            app,
            state["lang"],
            link_input,
            quality_var,
            format_var,
            download_btn,
            progress_frame,
            progress_bar,
            status_label,
        ),
    )

    download_btn.pack(side="left")

    # ---------------------------------------------------------
    # Formato MP3 / MP4
    # ---------------------------------------------------------

    format_frame = ctk.CTkFrame(
        app,
        fg_color="transparent",
    )

    format_frame.grid(
        row=3,
        column=0,
        pady=(0, 12),
    )

    format_label = ctk.CTkLabel(
        format_frame,
        text="Formato:",
        font=normal_font,
    )

    format_label.pack(
        side="left",
        padx=(0, 8),
    )

    format_menu = ctk.CTkSegmentedButton(
        format_frame,
        values=["MP3", "MP4"],
        variable=format_var,
        font=normal_font,
    )

    format_menu.pack(side="left")

    # ---------------------------------------------------------
    # Qualità MP3
    # ---------------------------------------------------------

    quality_frame = ctk.CTkFrame(
        app,
        fg_color="transparent",
    )

    quality_frame.grid(
        row=4,
        column=0,
        pady=(0, 20),
    )

    quality_label = ctk.CTkLabel(
        quality_frame,
        text="",
        font=normal_font,
    )

    quality_label.pack(
        side="left",
        padx=(0, 8),
    )

    quality_menu = ctk.CTkOptionMenu(
        quality_frame,
        values=[
            "128",
            "192",
            "256",
            "320",
        ],
        variable=quality_var,
        font=normal_font,
        width=90,
    )

    quality_menu.pack(side="left")

    # ---------------------------------------------------------
    # Progresso
    # ---------------------------------------------------------

    progress_frame = ctk.CTkFrame(
        app,
        fg_color="transparent",
    )

    progress_frame.grid(
        row=5,
        column=0,
        pady=(0, 10),
    )

    progress_frame.grid_remove()

    status_label = ctk.CTkLabel(
        progress_frame,
        text="",
        font=normal_font,
    )

    status_label.pack()

    progress_bar = ctk.CTkProgressBar(
        progress_frame,
        width=300,
    )

    progress_bar.set(0)

    progress_bar.pack(
        pady=(5, 0)
    )

    # ---------------------------------------------------------
    # Impostazioni
    # ---------------------------------------------------------

    settings_btn = ctk.CTkButton(
        app,
        width=110,
        font=normal_font,
        fg_color="gray30",
        hover_color="gray20",
        command=lambda: open_settings(
            app,
            on_save=on_settings_saved,
        ),
    )

    settings_btn.grid(
        row=6,
        column=0,
        pady=(0, 10),
    )

    # ---------------------------------------------------------
    # Traduzioni
    # ---------------------------------------------------------

    def apply_translations(lang):

        state["lang"] = lang

        title_label.configure(
            text=t(lang, "app_title")
        )

        link_input.configure(
            placeholder_text=t(
                lang,
                "link_placeholder"
            )
        )

        download_btn.configure(
            text=t(lang, "download_btn")
        )

        quality_label.configure(
            text=t(lang, "quality_label")
        )

        settings_btn.configure(
            text=t(lang, "settings_btn")
        )

    def on_settings_saved(new_settings):

        quality_var.set(
            new_settings["default_quality"]
        )

        apply_translations(
            new_settings["language"]
        )

    apply_translations(
        state["lang"]
    )

    # ---------------------------------------------------------
    # Dimensione e posizione finestra
    # ---------------------------------------------------------

    app.update_idletasks()

    width = (
        app.winfo_reqwidth()
        + int(60 * scale_factor)
    )

    height = (
        app.winfo_reqheight()
        + int(40 * scale_factor)
    )

    x = (screen_w - width) // 2
    y = (screen_h - height) // 2

    app.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    app.resizable(
        False,
        False
    )

    app.mainloop()


if __name__ == "__main__":
    main()