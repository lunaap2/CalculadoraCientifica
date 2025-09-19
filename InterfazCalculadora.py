import tkinter as tk
import math

def on_click(event): #Esta es la función central que maneja todos los eventos de clic en los botones:
    current_text = entry.get() # Obtiene el texto actual en la caja de entrada
    current_text = current_text.replace("√", "math.sqrt(") # Reemplaza "√" por "math.sqrt"
    current_text += ")"
    current_text = current_text.replace("%", "math.fmod(") # Reemplaza "%" por "math.fmod"
    current_text += ")"
    button_text = event.widget.cget("text") # Obtiene el texto del botón clickeado
    


    if button_text == "=": 

        try:

            result = eval(current_text) # Evaluamos la expresión matemática

            entry.delete(0, tk.END) # Borra el contenido actual

            entry.insert(tk.END, str(result)) # Inserta el resultado

        except Exception as e:

            entry.delete(0, tk.END)

            entry.insert(tk.END, "Error, No num or empty") # Maneja errores en la expresión

    elif button_text == "C":  

        entry.delete(0, tk.END) # Borra todo el contenido de la caja de entrada

    else:

        entry.insert(tk.END, button_text) # Añade el carácter del botón al final del texto

# Crear una ventana

root = tk.Tk() # Crea la ventana principal

root.title("Calculadora de Luna Diaz") # Establece el título de la ventana

# Crear una caja de entrada (Entry)

entry = tk.Entry(root, font=("Helvetica", 20)) # Crea un campo de texto con fuente grande

entry.grid(row=0, column=0, columnspan=4) # Posiciona el campo en la fila 0, ocupando 4 columnas

# Lista de botones

buttons = [

    "7", "8", "9", "/",  # Fila 1: números 7-9 y división

    "4", "5", "6", "*",  # Fila 2: números 4-6 y multiplicación

    "1", "2", "3", "-",  # Fila 3: números 1-3 y resta

    "0", ".", "=", "+",  # Fila 4: número 0, punto decimal, igual y suma

    "C", "√", "%", "F3"  # Fila 5: botón de limpiar (centrado)

]

# Crear y colocar los botones en la ventana

row = 1 # Comienza en la fila 1 (la fila 0 es para la caja de entrada)

col = 0

for button_text in buttons:

    button = tk.Button(root, text=button_text, font=("Helvetica", 20), padx=20, pady=20)

    button.grid(row=row, column=col)

    button.bind("<Button-1>", on_click)  # Asocia la función on_click al evento de clic izquierdo

    col += 1

    if col > 3: # Si se excede de la columna 3

        col = 0 # Reinicia a la columna 0

        row += 1 # Y pasa a la siguiente fila

# Ejecutar el bucle principal

root.mainloop() # Inicia el bucle de eventos