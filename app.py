import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp

def download_video(resolution):
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please paste a YouTube link.")
        return
    if "youtube.com" not in url and "youtu.be" not in url:
        messagebox.showerror("Error", "Invalid YouTube URL.")
        return
    
    folder = filedialog.askdirectory()
    if not folder:
        messagebox.showerror("Error", "Please select a folder.")
        return

    try:
        ydl_opts = {'outtmpl': f"{folder}/%(title)s.%(ext)s"}
        if resolution == "high":
            ydl_opts['format'] = 'best'
        elif resolution == "low":
            ydl_opts['format'] = 'worst'
        elif resolution == "audio":
            ydl_opts = {
                'format': 'bestaudio',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
                'outtmpl': f"{folder}/%(title)s.%(ext)s",
            }
        
        def progress_hook(d):
            if d['status'] == 'finished':
                messagebox.showinfo("Info", "Download finished, processing file...")
            elif d['status'] == 'downloading':
                print(f"Downloading: {d['_percent_str']} completed")

        ydl_opts['progress_hooks'] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", f"{resolution.capitalize()} download complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("YouTube Downloader with yt-dlp")
root.geometry("400x300")

tk.Label(root, text="Paste Link Here:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

tk.Button(root, text="High Resolution", command=lambda: download_video("high")).pack(pady=5)
tk.Button(root, text="Low Resolution", command=lambda: download_video("low")).pack(pady=5)
tk.Button(root, text="Audio Only", command=lambda: download_video("audio")).pack(pady=5)

root.mainloop()
