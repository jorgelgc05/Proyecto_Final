import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para calcular el IMC
def calcular_imc(peso, altura):
    return peso / altura ** 2

# Función para determinar el estado de la persona según su IMC
def determinar_estado(imc):
    if imc < 18.5:
        return 'Bajo peso'
    elif imc < 25:
        return 'Normal'
    elif imc < 30:
        return 'Sobrepeso'
    else:
        return 'Obesidad'

# Función para dibujar el medidor del IMC
def dibujar_medidor(imc, frame):
    # Datos
    label = ["Bajo Peso", "Normal", "Sobrepeso", "Obesidad"]
    val = [18.5, 24.9-18.5, 29.9-24.9, 40-29.9]
    colors = ['lightblue', 'lightgreen', 'yellow', 'pink']

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100, subplot_kw=dict(aspect="equal"))

    wedges, texts = ax.pie(val, wedgeprops=dict(width=0.3, edgecolor='w'), labels=label, colors=colors, startangle=-40)

    # Añadir una aguja
    angle = (imc / 40) * 360 - 40
    ax.annotate('', xy=(np.cos(np.radians(angle)), np.sin(np.radians(angle))), 
                xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='red', lw=2))

    # Añadir un círculo en el centro
    centre_circle = plt.Circle((0, 0), 0.7, fc='white', edgecolor='black')
    fig.gca().add_artist(centre_circle)

    plt.title('Distribución del IMC')

    # Incrustar el gráfico en el frame de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Función para calcular el IMC desde la interfaz
def calcular_imc_interfaz():
    try:
        pesoInput = float(entradaPeso.get())
        alturaInput = float(entradaAltura.get())
        
        if pesoInput <= 0 or alturaInput < 0:
            raise ValueError("Los valores deben ser mayores a 0")
        
        resultado = calcular_imc(pesoInput, alturaInput)
        estado = determinar_estado(resultado)
        recomendaciones = {
            'Bajo peso': 'Se recomienda una dieta rica en calorías y nutrientes.',
            'Normal': 'Mantenga una dieta balanceada y ejercicio regular.',
            'Sobrepeso': 'Se recomienda una dieta baja en calorías y aumentar la actividad física.',
            'Obesidad': 'Consulte a un profesional de salud para un plan adecuado.'
        }
        
        labelResultado.config(text=f"Su IMC es de {resultado:.1f} ({estado})\n{recomendaciones[estado]}")
        
        # Limpiar el gráfico anterior
        for widget in frameGrafico.winfo_children():
            widget.destroy()
        
        dibujar_medidor(resultado, frameGrafico)  # Llamar a la función para dibujar el medidor
    
    # Excepciones para manejar valores incorrectos
    except ValueError as e:
        if "could not convert string to float" in str(e):
            labelResultado.config(text="Error: Por favor, ingrese números válidos")
        elif "Los valores deben ser positivos" in str(e):
            labelResultado.config(text=f"Error: {e}")
        else:
            labelResultado.config(text=f"Error: {e}")
    except ZeroDivisionError:
        labelResultado.config(text="Error: La altura no puede ser 0")

# Función para establecer placeholder en el campo de entrada
def set_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, placeholder))
    entry.bind("<FocusOut>", lambda event: add_placeholder(event, placeholder))

# Función para limpiar el placeholder si el campo está seleccionado
def clear_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg='black')

# Función para añadir el placeholder si el campo está vacío
def add_placeholder(event, placeholder):
    if not event.widget.get():
        event.widget.insert(0, placeholder)
        event.widget.config(fg='grey')

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de IMC")
ventana.geometry("900x600")
ventana.configure(bg="lightblue")

# Frame para los campos de entrada
frameInputs = tk.Frame(ventana, bg="lightblue")
frameInputs.pack(pady=20)

# Label y campo de entrada para el peso
labelPeso = tk.Label(frameInputs, 
    text="Peso(kg)",
    font=("Arial", 18, "bold"),
    fg="Black",
    bg="lightblue"
)
labelPeso.grid(row=0, column=0, padx=20, pady=10, sticky="w")

entradaPeso = tk.Entry(frameInputs, font=("Arial", 12), width=15, fg='grey')
entradaPeso.grid(row=1, column=0, padx=20, pady=10, sticky="w")
set_placeholder(entradaPeso, "ej: 70")

# Label y campo de entrada para la altura
labelAltura = tk.Label(frameInputs, 
    text="Altura(mts)",
    font=("Arial", 18, "bold"),
    fg="Black",
    bg="lightblue"
)
labelAltura.grid(row=0, column=1, padx=(40, 10), pady=10, sticky="e")

entradaAltura = tk.Entry(frameInputs, font=("Arial", 12), width=15, fg='grey')
entradaAltura.grid(row=1, column=1, padx=10, pady=10, sticky="e")
set_placeholder(entradaAltura, "ej: 1.75")

# Botón para calcular el IMC
botonIMC = tk.Button(ventana, text="Calcular Indice de Masa Corporal (IMC)", command=calcular_imc_interfaz, 
                     font=("Arial", 14, "bold"), bg="Black", fg="white")
botonIMC.pack(pady=20)

# Label para mostrar los resultados
labelResultado = tk.Label(ventana, 
    text="",
    font=("Arial", 18, "bold"),
    fg="Green",
    bg="lightblue"
)
labelResultado.pack(pady=20)

# Frame para el gráfico
frameGrafico = tk.Frame(ventana, bg="lightblue")
frameGrafico.pack(pady=20)

# Iniciar el bucle principal de la interfaz
ventana.mainloop()

