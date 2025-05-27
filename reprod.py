import tkinter as tk
from tkinter import filedialog
import pygame
import os
import threading
import random

# Inicializar pygame
pygame.mixer.init()

# Ventana principal
root = tk.Tk()
root.title("Reproductor de Música")
root.geometry("600x400")
root.configure(bg="#2f2f2f")

# Variables
playlist = []
current_index = 0
playing = False

# Funciones
def cargar_canciones():
    global playlist
    files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
    for f in files:
        playlist.append(f)
        song_listbox.insert(tk.END, os.path.basename(f))

def reproducir():
    global playing
    if playlist:
        pygame.mixer.music.load(playlist[current_index])
        pygame.mixer.music.play()
        playing = True
        actualizar_animacion()

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

# UI

# Lista de canciones
song_listbox = tk.Listbox(root, bg="#1f1f1f", fg="white", width=40, height=8, font=("Arial", 10))
song_listbox.pack(pady=10)

# Canvas para animación de ondas
canvas = tk.Canvas(root, bg="#2f2f2f", height=60, width=160, highlightthickness=0)
canvas.pack()

# Botones
btn_frame = tk.Frame(root, bg="#2f2f2f")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="⏮", command=siguiente, width=5).grid(row=0, column=0)
tk.Button(btn_frame, text="▶", command=reproducir, width=5).grid(row=0, column=1)
tk.Button(btn_frame, text="⏸", command=pausar, width=5).grid(row=0, column=2)
tk.Button(btn_frame, text="⏯", command=continuar, width=5).grid(row=0, column=3)

# Barra de volumen (más pequeña)
tk.Label(root, text="Volumen", bg="#2f2f2f", fg="white").pack()
volumen = tk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_volumen,
                   length=150, showvalue=0, sliderlength=10)
volumen.set(70)
volumen.pack()

# Botón para cargar canciones
tk.Button(root, text="Cargar canciones", command=cargar_canciones, bg="#444", fg="white").pack(pady=5)

root.mainloop()



