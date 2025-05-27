import tkinter as tk
from tkinter import filedialog
import pygame
import os
import threading
import time
import random

pygame.mixer.init()

root = tk.Tk()
root.title("Reproductor de Música")
root.geometry("600x460")
root.configure(bg="#2f2f2f")

playlist = []
current_index = 0
playing = False
duracion_total = 0
actualizando_seek = True

def cargar_canciones():
    global playlist
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for f in files:
        playlist.append(f)
        song_listbox.insert(tk.END, os.path.basename(f))

def reproducir():
    global playing, duracion_total, actualizando_seek
    if playlist:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play()
        playing = True
        actualizando_seek = True
        actualizar_animacion()
        threading.Thread(target=actualizar_seekbar, daemon=True).start()
        try:
            from mutagen.mp3 import MP3
            audio = MP3(playlist[current_index])
            duracion_total = int(audio.info.length)
            seekbar.config(to=duracion_total)
        except:
            duracion_total = 100
            seekbar.config(to=100)

def pausar():
    pygame.mixer.music.pause()

def continuar():
    pygame.mixer.music.unpause()

def siguiente():
    global current_index
    if current_index < len(playlist) - 1:
        current_index += 1
        reproducir()

def actualizar_volumen(val):
    volumen = int(val) / 100
    pygame.mixer.music.set_volume(volumen)

def actualizar_animacion():
    if playing:
        canvas.delete("all")
        for i in range(10):
            x = i * 15 + 5
            h = random.randint(10, 60)
            canvas.create_line(x, 60, x, 60 - h, fill="white", width=2)
        root.after(200, actualizar_animacion)

def actualizar_seekbar():
    global actualizando_seek
    while playing and actualizando_seek:
        try:
            pos = pygame.mixer.music.get_pos() // 1000
            seekbar.set(pos)
        except:
            pass
        time.sleep(1)

def mover_seek(val):
    global actualizando_seek
    actualizando_seek = False
    pygame.mixer.music.play(start=int(val))
    actualizando_seek = True
    threading.Thread(target=actualizar_seekbar, daemon=True).start()

# UI

# Título
tk.Label(root, text="Pistas", font=("Arial", 12, "bold"), bg="#2f2f2f", fg="white").pack(pady=(10, 0))

# Lista de canciones
song_listbox = tk.Listbox(root, bg="#1f1f1f", fg="white", width=60, height=6, font=("Arial", 10), borderwidth=0)
song_listbox.pack(pady=(0, 5))

# Canvas para animación de ondas
canvas = tk.Canvas(root, bg="#2f2f2f", height=60, width=160, highlightthickness=0)
canvas.pack(pady=(0, 5))

# Botones
btn_frame = tk.Frame(root, bg="#2f2f2f")
btn_frame.pack(pady=(0, 10))

tk.Button(btn_frame, text="⏮", command=siguiente, width=5).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="▶", command=reproducir, width=5).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="⏸", command=pausar, width=5).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="⏯", command=continuar, width=5).grid(row=0, column=3, padx=5)

# Barra de progreso
tk.Label(root, text="Progreso", bg="#2f2f2f", fg="white").pack()
seekbar = tk.Scale(root, from_=0, to=100, orient="horizontal", command=mover_seek,
                   length=500, showvalue=0, sliderlength=10)
seekbar.pack()

# Contenedor para volumen y botón de cargar
bottom_frame = tk.Frame(root, bg="#2f2f2f")
bottom_frame.pack(fill="x", pady=10)

# Botón cargar canciones
tk.Button(bottom_frame, text="Cargar canciones", command=cargar_canciones,
          bg="#444", fg="white").pack(side="left", padx=20)

# Volumen
vol_frame = tk.Frame(bottom_frame, bg="#2f2f2f")
vol_frame.pack(side="right", padx=20)

tk.Label(vol_frame, text="Volumen", bg="#2f2f2f", fg="white").pack(anchor="e")
volumen = tk.Scale(vol_frame, from_=0, to=100, orient="horizontal", command=actualizar_volumen,
                   length=100, showvalue=0, sliderlength=10)
volumen.set(70)
volumen.pack(anchor="e")

root.mainloop()


