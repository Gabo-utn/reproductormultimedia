import tkinter as tk
from tkinter import filedialog, messagebox #se agrega messagebox
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
duracion_total = 1.0 #formato 1.0
actualizando_seekbar = False
detener_hilo = False 

# Bandera para indicar si el seekbar está siendo arrastrado por el usuario
dragging_seekbar = False #se agrega esta linea arrastre de barra

# Variable para almacenar la ruta de la canción cargada actualmente en el mixer de Pygame
current_loaded_song = None  #se agrega esta linea se la usa en def reproducir


# #se agrega esta linea Funciones Auxiliares

def format_time(seconds):
    """Formatea segundos a una cadena de tiempo MM:SS."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Funciones

def cargar_canciones(): #agrega if archivo not in 
    global playlist
    archivos = filedialog.askopenfilenames(filetypes=[("Archivos de audio", "*.mp3")])
    if archivos:
        for archivo in archivos: #
            if archivo not in playlist: #
                playlist.append(archivo) #
        
        lista_canciones.delete(0, tk.END)
        for archivo in playlist:
            lista_canciones.insert(tk.END, os.path.basename(archivo))

def reproducir():
    global playing, duracion_total, actualizando_seekbar, current_index, detener_hilo, current_loaded_song #se agrega current_loaded_song
    
    if not playlist:
        return

    detener_hilo = True 
    time.sleep(0.05) #se cambia time sleep de 0.1 a 0.05
    
    pygame.mixer.music.stop()
#se agrega este condicional y try en pygame.mexer.music.load
    if playlist[current_index] != current_loaded_song: #
        try:
            pygame.mixer.music.load(playlist[current_index])
            current_loaded_song = playlist[current_index] #
        except pygame.error as e: #se agrega este messagebox
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo: {os.path.basename(playlist[current_index])}\n{e}")
            if playlist:
                playlist.pop(current_index) 
                if current_index >= len(playlist): current_index = 0
                if playlist:
                    reproducir()
                else:
                    detener_reproduccion_final()
            return

    pygame.mixer.music.play() 
    
    playing = True
    #se agrega un try y messagebox
    try:
        duracion_total = pygame.mixer.Sound(playlist[current_index]).get_length()
    except pygame.error as e:
        messagebox.showerror("Error de Duración", f"No se pudo obtener la duración del archivo: {os.path.basename(playlist[current_index])}\n{e}")
        duracion_total = 1.0
    #se agregan estas lineas    
    tiempo_total_label.config(text=format_time(duracion_total))
    seekbar.set(0) # Resetear la barra al inicio al cargar nueva canción
    tiempo_actual_label.config(text="00:00") # Resetear el tiempo actual

    actualizando_seekbar = True
    actualizar_seekbar() 
    
    lista_canciones.select_clear(0, tk.END)
    lista_canciones.select_set(current_index)
    lista_canciones.activate(current_index)

def pausar():
    global playing
    if playing:#se agrega if 
        pygame.mixer.music.pause()
        playing = False

def continuar():
    global playing #se agrega if not playing
    if not playing and pygame.mixer.music.get_busy() == 0 and current_loaded_song is not None:
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
    else: #se agrega este else
        reproducir()

def detener_reproduccion_final():
    global playing, detener_hilo, current_loaded_song #se agrega current
    playing = False
    detener_hilo = True
    pygame.mixer.music.stop()
    seekbar.set(0)
    tiempo_actual_label.config(text="00:00")#se agregan estas lineas para seekbar#
    tiempo_total_label.config(text="00:00")#
    current_loaded_song = None #

def actualizar_seekbar():
    """
    Función que se ejecuta en un hilo separado para actualizar
    solo el contador de minutos/segundos. La barra de progreso
    solo se mueve manualmente.
    """
    def actualizar():
        global actualizando_seekbar, playing, detener_hilo, dragging_seekbar #seagrega dragging
#cambia el orden de las variables del while
        while actualizando_seekbar and not detener_hilo:
            if not playing: 
                time.sleep(0.1)#cambia el valo de 1 a 0.1
                continue
#se crea variable local mixer_pos_ms
            mixer_pos_ms = pygame.mixer.music.get_pos() #
            
            if mixer_pos_ms == -1: 
                if playing and duracion_total > 0 and tiempo_actual_label.cget("text") != format_time(duracion_total):
                    time.sleep(0.5) 
                    if pygame.mixer.music.get_pos() == -1:
                        ventana.after(0, siguiente_cancion)
                        break 
                elif playing and duracion_total > 0 and tiempo_actual_label.cget("text") == format_time(duracion_total):
                     pass
                else: 
                    time.sleep(0.1)
                    continue

            tiempo_actual = mixer_pos_ms / 1000.0
            
            if duracion_total > 0 and tiempo_actual > duracion_total:
                 tiempo_actual = duracion_total
                 ventana.after(0, siguiente_cancion)
                 break 

            # Solo actualizar la etiqueta del tiempo actual, NO el seekbar si no se está arrastrando
            ventana.after(0, lambda: tiempo_actual_label.config(text=format_time(tiempo_actual)))
            
            time.sleep(0.1) # Esperar 100 milisegundos antes de la próxima actualización

        actualizando_seekbar = False
        detener_hilo = False

    global detener_hilo #se meciona como global
    detener_hilo = False 
    threading.Thread(target=actualizar, daemon=True).start()

def mover_seek(val):
    """Mueve la reproducción a la posición indicada por el seekbar."""
    global actualizando_seekbar, playing, detener_hilo, current_loaded_song #se agrega current
    
    if not playlist:
        return
    #se cambia el lugar y nombre a nuevo tiempo seek
    nuevo_tiempo_seek = float(val) / 100 * duracion_total

    # SI EL USUARIO ESTÁ ARRASTRANDO, SOLO ACTUALIZAMOS LA ETIQUETA TEMPORALMENTE Y LA BARRA
    if dragging_seekbar: 
        tiempo_actual_label.config(text=format_time(nuevo_tiempo_seek))
        # Actualizar la barra visualmente mientras se arrastra
        seekbar.set(val) 
        return

    # Si llegamos aquí, el usuario soltó el seekbar o se llamó desde otro lado.
    #se agrega un if else y try except
    if current_loaded_song != playlist[current_index]:
        try:
            pygame.mixer.music.load(playlist[current_index])
            current_loaded_song = playlist[current_index]
            pygame.mixer.music.play(start=nuevo_tiempo_seek) 
        except pygame.error as e:
            messagebox.showerror("Error", f"No se pudo cargar o buscar en el archivo: {os.path.basename(playlist[current_index])}\n{e}")
            return
    else:
        try:
            pygame.mixer.music.set_pos(nuevo_tiempo_seek) 
        except pygame.error as e:
            print(f"Error al intentar set_pos: {e}. Pygame puede no soportar set_pos para este archivo o sistema. Volviendo a cargar y reproducir...")
            pygame.mixer.music.stop()
            pygame.mixer.music.load(playlist[current_index])
            pygame.mixer.music.play(start=nuevo_tiempo_seek)
    
    if not playing:
        pygame.mixer.music.unpause()
        playing = True
    
    # Después de un seek, actualizamos la barra a la nueva posición
    if duracion_total > 0:
        seekbar.set(nuevo_tiempo_seek / duracion_total * 100)

    if not actualizando_seekbar:
        actualizando_seekbar = True
        actualizar_seekbar()


# --- Eventos para el seekbar de arrastre ---
def on_seekbar_drag_start(event):
    """Función que se llama cuando el usuario empieza a arrastrar el seekbar."""
    global dragging_seekbar
    dragging_seekbar = True

def on_seekbar_drag_end(event):
    """Función que se llama cuando el usuario suelta el seekbar."""
    global dragging_seekbar
    dragging_seekbar = False
    mover_seek(seekbar.get()) 


def actualizar_volumen(val):
    pygame.mixer.music.set_volume(float(val))

# --- Widgets UI ---

etiqueta_pistas = tk.Label(ventana, text="Pistas", bg="#2e2e2e", fg="white", font=("Arial", 12))
etiqueta_pistas.pack(pady=(10, 0))

# --- FRAME PARA LA LISTA DE CANCIONES Y EL SCROLLBAR ---
frame_lista = tk.Frame(ventana, bg="#2e2e2e")
frame_lista.pack(pady=5)

scrollbar = tk.Scrollbar(frame_lista, orient="vertical")
scrollbar.pack(side="right", fill="y") # Empaquetar el scrollbar a la derecha del frame

lista_canciones = tk.Listbox(frame_lista, bg="black", fg="white", width=60, height=8, selectbackground="#a6a6a6", selectforeground="black", yscrollcommand=scrollbar.set)
lista_canciones.pack(side="left", fill="both", expand=True) # El Listbox se expande y se llena
scrollbar.config(command=lista_canciones.yview) # El scrollbar controla la vista del Listbox
lista_canciones.bind("<Double-Button-1>", lambda e: reproducir_seleccionada())
#bind lamda
frame_botones = tk.Frame(ventana, bg="#2e2e2e")
frame_botones.pack(pady=5)

btn_prev = tk.Button(frame_botones, text="⏮", command=anterior_cancion, width=5, bg="#444444", fg="white")
btn_prev.grid(row=0, column=0, padx=5)

btn_play = tk.Button(frame_botones, text="▶", command=reproducir, width=5, bg="#444444", fg="white")
btn_play.grid(row=0, column=1, padx=5)

btn_pause = tk.Button(frame_botones, text="⏸", command=pausar, width=5, bg="#444444", fg="white")
btn_pause.grid(row=0, column=2, padx=5)

btn_continue = tk.Button(frame_botones, text="⏯", command=continuar, width=5, bg="#444444", fg="white")
btn_continue.grid(row=0, column=3, padx=5)

btn_next = tk.Button(frame_botones, text="⏭", command=siguiente_cancion, width=5, bg="#444444", fg="white")
btn_next.grid(row=0, column=4, padx=5)

etiqueta_progreso = tk.Label(ventana, text="Progreso", bg="#2e2e2e", fg="white")
etiqueta_progreso.pack()

seekbar = tk.Scale(ventana, from_=0, to=100, orient="horizontal", length=400, command=mover_seek, bg="#2e2e2e", fg="white", highlightbackground="#2e2e2e", troughcolor="#555555", showvalue=False)
seekbar.pack()
seekbar.bind("<ButtonPress-1>", on_seekbar_drag_start)##
seekbar.bind("<ButtonRelease-1>", on_seekbar_drag_end)##


frame_tiempos = tk.Frame(ventana, bg="#2e2e2e")
frame_tiempos.pack()

tiempo_actual_label = tk.Label(frame_tiempos, text="00:00", bg="#2e2e2e", fg="white")
tiempo_actual_label.pack(side="left", padx=10) ##

tiempo_total_label = tk.Label(frame_tiempos, text="00:00", bg="#2e2e2e", fg="white")
tiempo_total_label.pack(side="right", padx=10)

etiqueta_volumen = tk.Label(ventana, text="Volumen", bg="#2e2e2e", fg="white")
etiqueta_volumen.place(x=480, y=440)

volumen = tk.Scale(ventana, from_=0, to=1, resolution=0.1, orient="horizontal", command=actualizar_volumen, length=100, bg="#2e2e2e", fg="white", highlightbackground="#2e2e2e", troughcolor="#555555")
volumen.set(0.5)
volumen.place(x=480, y=460)

btn_cargar = tk.Button(ventana, text="Cargar canciones", command=cargar_canciones, bg="#444444", fg="white")
btn_cargar.pack(pady=10)

def reproducir_seleccionada(): ##se agrega esta funcion para reproducir haciendo click
    global current_index
    seleccion = lista_canciones.curselection()
    if seleccion:
        new_index = seleccion[0]
        if new_index != current_index:
            current_index = new_index
            reproducir()
        elif not playing:
            reproducir()

ventana.mainloop()