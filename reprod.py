import tkinter as tk
from tkinter import filedialog
import pygame
import os
import threading
import time

# Inicializar pygame
pygame.mixer.init()

# Crear la ventana
ventana = tk.Tk()
ventana.title("Reproductor de Música")
ventana.geometry("600x500")
ventana.configure(bg="#2e2e2e")

# Variables globales
playlist = []
current_index = 0
playing = False
duracion_total = 1
actualizando_seekbar = False
detener_hilo = False

# Funciones

def cargar_canciones():
    global playlist
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.mp3")])
    if archivos:
        playlist.extend(archivos)
        lista_canciones.delete(0, tk.END)
        for archivo in playlist:
            lista_canciones.insert(tk.END, os.path.basename(archivo))

def reproducir():
    global playing, duracion_total, actualizando_seekbar, detener_hilo
    if not playlist:
        return
    detener_hilo = True
    time.sleep(0.1)  # Permitir que hilos anteriores terminen
    pygame.mixer.music.stop()
    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play()
    playing = True
    duracion_total = pygame.mixer.Sound(playlist[current_index]).get_length()
    actualizando_seekbar = True
    actualizar_seekbar()
    actualizar_tiempos()
    lista_canciones.select_clear(0, tk.END)
    lista_canciones.select_set(current_index)
    lista_canciones.activate(current_index)

def pausar():
    global playing
    pygame.mixer.music.pause()
    playing = False

def continuar():
    global playing
    pygame.mixer.music.unpause()
    playing = True

def siguiente_cancion():
    global current_index
    if current_index < len(playlist) - 1:
        current_index += 1
        reproducir()
    else:
        detener_reproduccion_final()

def anterior_cancion():
    global current_index
    if current_index > 0:
        current_index -= 1
        reproducir()

def detener_reproduccion_final():
    global playing, detener_hilo
    playing = False
    detener_hilo = True
    pygame.mixer.music.stop()
    seekbar.set(0)
   

def actualizar_seekbar():
    def actualizar():
        global actualizando_seekbar, playing, detener_hilo
        while playing and actualizando_seekbar and not detener_hilo:
            if pygame.mixer.music.get_busy():
                tiempo_actual = pygame.mixer.music.get_pos() / 1000
                if tiempo_actual >= duracion_total:
                    playing = False
                    detener_hilo = True
                    ventana.after(0, siguiente_cancion)
                    break
                seekbar.set(tiempo_actual / duracion_total * 100)
               
            time.sleep(1)
    detener_hilo = False
    threading.Thread(target=actualizar, daemon=True).start()

def mover_seek(val):
    global actualizando_seekbar, playing, detener_hilo
    if not playlist:
        return
    detener_hilo = True
    time.sleep(0.1)
    actualizando_seekbar = False
    nuevo_tiempo = float(val) / 100 * duracion_total
    pygame.mixer.music.stop()
    pygame.mixer.music.load(playlist[current_index])
    pygame.mixer.music.play(start=nuevo_tiempo)
    playing = True
    actualizando_seekbar = True
    actualizar_seekbar()

def actualizar_volumen(val):
    pygame.mixer.music.set_volume(float(val))





# Widgets UI

# Lista de canciones
etiqueta_pistas = tk.Label(ventana, text="Pistas", bg="#2e2e2e", fg="white", font=("Arial", 12))
etiqueta_pistas.pack(pady=(10, 0))

lista_canciones = tk.Listbox(ventana, bg="black", fg="white", width=60, height=6)
lista_canciones.pack(pady=5)

# Botones
frame_botones = tk.Frame(ventana, bg="#2e2e2e")
frame_botones.pack(pady=5)

btn_prev = tk.Button(frame_botones, text="⏮", command=anterior_cancion, width=5)
btn_prev.grid(row=0, column=0, padx=5)

btn_play = tk.Button(frame_botones, text="▶", command=reproducir, width=5)
btn_play.grid(row=0, column=1, padx=5)

btn_pause = tk.Button(frame_botones, text="⏸", command=pausar, width=5)
btn_pause.grid(row=0, column=2, padx=5)

btn_continue = tk.Button(frame_botones, text="⏯", command=continuar, width=5)
btn_continue.grid(row=0, column=3, padx=5)

btn_next = tk.Button(frame_botones, text="⏭", command=siguiente_cancion, width=5)
btn_next.grid(row=0, column=4, padx=5)

# Barra de progreso
etiqueta_progreso = tk.Label(ventana, text="Progreso", bg="#2e2e2e", fg="white")
etiqueta_progreso.pack()
seekbar = tk.Scale(ventana, from_=0, to=100, orient="horizontal", length=400, command=mover_seek)
seekbar.pack()

# Tiempos actuales y totales
frame_tiempos = tk.Frame(ventana, bg="#2e2e2e")
frame_tiempos.pack()

tiempo_total_label = tk.Label(frame_tiempos, text="", bg="#2e2e2e", fg="white")
tiempo_total_label.pack(side="right", padx=10)

# Control de volumen
etiqueta_volumen = tk.Label(ventana, text="Volumen", bg="#2e2e2e", fg="white")
etiqueta_volumen.place(x=480, y=440)

volumen = tk.Scale(ventana, from_=0, to=1, resolution=0.1, orient="horizontal", command=actualizar_volumen, length=100)
volumen.set(0.5)
volumen.place(x=480, y=460)

# Botón para cargar canciones
btn_cargar = tk.Button(ventana, text="Cargar canciones", command=cargar_canciones, bg="#444444", fg="white")
btn_cargar.pack(pady=10)

# Iniciar loop de ventana
ventana.mainloop()

