🧠 Bibliotecas utilizadas
Biblioteca	Uso principal

tkinter	Crear la interfaz gráfica (ventanas, botones, sliders, listas, etc.).
filedialog	Permite abrir un explorador de archivos para que el usuario cargue canciones.
pygame	Manejar la reproducción de música (reproducir, pausar, cambiar volumen, etc.).
os	Permite trabajar con archivos, como obtener solo el nombre del archivo.
threading	Permite ejecutar tareas en segundo plano sin bloquear la interfaz.
time	Sirve para hacer pausas (ej: actualizar barra cada segundo).
random	Se usa para animar las "ondas de sonido" de forma aleatoria.

⚙️ Funciones del programa
Función	¿Qué hace?

cargar_canciones()	Abre un explorador de archivos para seleccionar canciones MP3. Agrega los nombres a la lista.
reproducir()	Reproduce la canción actual en la lista, inicia la animación y la barra de progreso.
pausar()	Pausa la reproducción de música.
continuar()	Reanuda la reproducción pausada.
siguiente()	Avanza a la siguiente canción en la lista (si hay más).
actualizar_volumen(val)	Cambia el volumen con el valor del slider.
actualizar_animacion()	Genera líneas aleatorias en un canvas para simular una onda de sonido. Se actualiza cada 200 milisegundos.
actualizar_seekbar()	Cada segundo actualiza la posición actual de la canción en la barra de progreso.
mover_seek(val)	Permite adelantar o retroceder en la canción desde la barra de progreso.

🔁 Variables importantes

Variable	¿Para qué sirve?
playlist	Lista con las rutas de las canciones seleccionadas.
current_index	Guarda el número (índice) de la canción que se está reproduciendo.
playing	Indica si hay música en reproducción (True o False).
duracion_total	Guarda la duración total de la canción actual (en segundos).
actualizando_seek	Controla si se está actualizando automáticamente la barra de progreso.
canvas	Área donde se dibujan las "ondas" para animar el reproductor.
seekbar	Barra que muestra el progreso actual de la canción. También permite moverse por ella.
volumen	Barra horizontal que controla el volumen del reproductor.
