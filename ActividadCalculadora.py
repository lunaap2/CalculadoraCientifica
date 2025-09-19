import tkinter as tk
import math

# Variables de estado para los modos científicos
modo_f2_activo = False  # Modo Científico 1
modo_f3_activo = False  # Modo Científico 2

def factorial(n):
    """Función para calcular el factorial de un número"""
    try:
        n = int(float(n))
        if n < 0:
            raise ValueError("Factorial no definido para números negativos")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    except:
        raise ValueError("Error en factorial")

def parse_expression(expression):
    """Parsea la expresión para convertir funciones personalizadas a Python/math"""
    import re
    
    # Reemplazar constantes
    expression = expression.replace("π", str(math.pi))
    expression = expression.replace("e", str(math.e))
    
    # Reemplazar funciones trigonométricas SIN paréntesis
    # Buscar patrones como "sin 90" y convertir a "math.sin(90)"
    expression = re.sub(r'sin\s+([0-9.]+)', r'math.sin(\1)', expression)
    expression = re.sub(r'cos\s+([0-9.]+)', r'math.cos(\1)', expression)
    expression = re.sub(r'tan\s+([0-9.]+)', r'math.tan(\1)', expression)
    expression = re.sub(r'asin\s+([0-9.]+)', r'math.asin(\1)', expression)
    expression = re.sub(r'acos\s+([0-9.]+)', r'math.acos(\1)', expression)
    expression = re.sub(r'atan\s+([0-9.]+)', r'math.atan(\1)', expression)
    
    # Reemplazar logaritmos SIN paréntesis
    expression = re.sub(r'log\s+([0-9.]+)', r'math.log10(\1)', expression)
    expression = re.sub(r'ln\s+([0-9.]+)', r'math.log(\1)', expression)
    
    # Reemplazar conversiones de ángulos SIN paréntesis
    expression = re.sub(r'rad\s+([0-9.]+)', r'math.radians(\1)', expression)
    expression = re.sub(r'deg\s+([0-9.]+)', r'math.degrees(\1)', expression)
    
    # Reemplazar raíz cuadrada SIN paréntesis
    expression = re.sub(r'√\s*([0-9.]+)', r'math.sqrt(\1)', expression)
    
    # Manejo de raíz cúbica SIN paréntesis
    expression = re.sub(r'∛\s*([0-9.]+)', r'((\1)**(1/3))', expression)
    
    # Manejo de potencia SIN paréntesis - formato "número ^ exponente"
    expression = re.sub(r'([0-9.]+)\s*\^\s*([0-9.]+)', r'pow(\1, \2)', expression)
    
    # Manejo de factorial SIN paréntesis - formato "número !" o "! número"
    expression = re.sub(r'([0-9.]+)\s*!', r'factorial(\1)', expression)
    expression = re.sub(r'!\s+([0-9.]+)', r'factorial(\1)', expression)
    
    return expression

def on_click(event):
    """Esta es la función central que maneja todos los eventos de clic en los botones"""
    global modo_f2_activo, modo_f3_activo
    
    current_text = entry.get()  # Obtiene el texto actual en la caja de entrada
    button_text = event.widget.cget("text")  # Obtiene el texto del botón clickeado
    
    # Manejo de los botones F2 y F3 (toggle)
    if button_text == "F2":
        modo_f2_activo = not modo_f2_activo
        # Cambiar el color del botón para indicar el estado
        if modo_f2_activo:
            event.widget.config(bg="lightgreen")
        else:
            event.widget.config(bg="SystemButtonFace")
        return
    
    elif button_text == "F3":
        modo_f3_activo = not modo_f3_activo
        # Cambiar el color del botón para indicar el estado
        if modo_f3_activo:
            event.widget.config(bg="lightblue")
        else:
            event.widget.config(bg="SystemButtonFace")
        return
    
    # Manejo del botón igual
    elif button_text == "=":
        try:
            # Verificar que hay contenido
            if not current_text.strip():
                entry.delete(0, tk.END)
                entry.insert(tk.END, "0")
                return
            
            # Parsear y evaluar la expresión
            expression = parse_expression(current_text)
            
            # Debug: imprimir la expresión parseada (opcional, para desarrollo)
            # print(f"Original: {current_text}")
            # print(f"Parseada: {expression}")
            
            result = eval(expression)
            
            # Formatear el resultado
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)  # Reducir decimales para evitar errores de precisión
            
            entry.delete(0, tk.END)  # Borra el contenido actual
            entry.insert(tk.END, str(result))  # Inserta el resultado
            
        except Exception as e:
            # Debug: imprimir el error (opcional, para desarrollo)
            # print(f"Error: {e}")
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")  # Maneja errores en la expresión
    
    # Manejo del botón limpiar
    elif button_text == "C":
        entry.delete(0, tk.END)  # Borra todo el contenido de la caja de entrada
    
    # Manejo de botones numéricos con modos científicos
    elif button_text in "0123456789":
        # Si F2 está activo (Modo Científico 1 tiene prioridad)
        if modo_f2_activo:
            funciones_f2 = {
                "7": "sin ",      # sin (usuario escribe el número)
                "8": "cos ",      # cos (usuario escribe el número)
                "9": "tan ",      # tan (usuario escribe el número)
                "4": "asin ",     # asin (usuario escribe el número)
                "5": "acos ",     # acos (usuario escribe el número)
                "6": "atan ",     # atan (usuario escribe el número)
                "1": "log ",      # log (usuario escribe el número)
                "2": "ln ",       # ln (usuario escribe el número)
                "3": "π",         # Constante π
                "0": "e"          # Constante e
            }
            text_to_insert = funciones_f2.get(button_text, button_text)
        
        # Si F3 está activo y F2 no está activo
        elif modo_f3_activo:
            funciones_f3 = {
                "7": "^ ",        # ^ (usuario escribe el exponente)
                "8": "√",         # √ (usuario escribe el número después)
                "9": "∛",         # ∛ (usuario escribe el número después)
                "4": "! ",        # ! (usuario puede escribir antes el número)
                "5": "rad ",      # rad (usuario escribe el número)
                "6": "deg ",      # deg (usuario escribe el número)
                "1": button_text, # Mantiene función numérica
                "2": button_text, # Mantiene función numérica
                "3": button_text, # Mantiene función numérica
                "0": button_text  # Mantiene función numérica
            }
            text_to_insert = funciones_f3.get(button_text, button_text)
        else:
            # Modo normal, solo insertar el número
            text_to_insert = button_text
        
        entry.insert(tk.END, text_to_insert)  # Añade el texto al final
    
    # Para todos los demás botones (operadores, etc.)
    else:
        # Manejo especial para la raíz cuadrada original
        if button_text == "√":
            entry.insert(tk.END, "√")
        else:
            entry.insert(tk.END, button_text)  # Añade el carácter del botón al final del texto

# Crear una ventana
root = tk.Tk()  # Crea la ventana principal
root.title("Calculadora Científica de Luna Diaz")  # Establece el título de la ventana
root.geometry("400x600")  # Tamaño de la ventana

# Crear una caja de entrada (Entry)
entry = tk.Entry(root, font=("Helvetica", 20), justify='right')  # Campo de texto alineado a la derecha
entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky='ew')  # Posiciona el campo

# Lista de botones ordenados por filas
buttons = [
    ["F2", "F3", "C", "√"],       # Fila 1: Funciones especiales
    ["7", "8", "9", "/"],         # Fila 2: números 7-9 y división
    ["4", "5", "6", "*"],         # Fila 3: números 4-6 y multiplicación
    ["1", "2", "3", "-"],         # Fila 4: números 1-3 y resta
    ["0", ".", "=", "+"],         # Fila 5: número 0, punto decimal, igual y suma
    ["", "", "%", ""]             # Fila 6: módulo y espacios vacíos
]

# Crear y colocar los botones en la ventana
for row_idx, button_row in enumerate(buttons):
    for col_idx, button_text in enumerate(button_row):
        if button_text:  # Solo crear botón si hay texto
            button = tk.Button(
                root, 
                text=button_text, 
                font=("Helvetica", 16), 
                padx=10, 
                pady=10,
                width=5,
                height=2
            )
            button.grid(row=row_idx+1, column=col_idx, padx=2, pady=2, sticky='nsew')
            button.bind("<Button-1>", on_click)  # Asocia la función on_click al evento de clic

# Configurar que las columnas y filas se expandan
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(len(buttons)+1):
    root.grid_rowconfigure(i, weight=1)

# Agregar indicadores de estado en la parte inferior
status_frame = tk.Frame(root)
status_frame.grid(row=len(buttons)+1, column=0, columnspan=4, pady=5)

status_label = tk.Label(status_frame, text="Modos: F2=Trigonométrico, F3=Avanzado", font=("Helvetica", 10))
status_label.pack()

# Ejecutar el bucle principal
root.mainloop()  # Inicia el bucle de eventos