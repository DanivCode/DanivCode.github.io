from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def calcular_movimiento_parabolico(angle, velocity, initial_x, initial_y):
    try:
        # Cálculo del movimiento parabólico
        g = 9.81  # Aceleración debido a la gravedad
        t = np.linspace(0, (2 * velocity * np.sin(np.radians(angle))) / g, 100)
        x = initial_x + velocity * np.cos(np.radians(angle)) * t
        y = initial_y + velocity * np.sin(np.radians(angle)) * t - (0.5 * g * t ** 2)
        
        # Encontrar el tiempo final, la posición final en X y la altura máxima
        tiempo_final = round(t[-1], 3)
        posicion_final_x = round(x[-1], 3)
        altura_maxima = round(max(y), 3)
        
        # Crear la gráfica
        plt.figure(figsize=(8, 6))
        plt.plot(x, y)
        plt.title("Movimiento Parabólico")
        plt.xlabel("Distancia (X)")
        plt.ylabel("Altura (Y)")
        plt.grid(True)
        plt.savefig("static/parabolic_plot.png")  # Guardar la gráfica en un archivo

        return tiempo_final, posicion_final_x, altura_maxima
    except ValueError:
        return None, None, None

@app.route("/parabolico", methods=["GET", "POST"])
def graficar_parabolico():
    if request.method == "POST":
        try:
            angle = float(request.form["angle"])
            velocity = float(request.form["velocity"])
            initial_x = float(request.form["initial_x"])
            initial_y = float(request.form["initial_y"])
            
            tiempo_final, posicion_final_x, altura_maxima = calcular_movimiento_parabolico(angle, velocity, initial_x, initial_y)

            if tiempo_final is not None:
                return render_template("index_parabolico.html", plot=True, tiempo_final=tiempo_final, posicion_final_x=posicion_final_x, altura_maxima=altura_maxima)
            else:
                error_message = "Por favor, ingresa valores numéricos válidos."
                return render_template("index_parabolico.html", error=error_message)
        except ValueError:
            error_message = "Por favor, ingresa valores numéricos válidos."
            return render_template("index_parabolico.html", error=error_message)

    return render_template("index_parabolico.html", plot=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["submit_button"] == "Movimiento Parabólico":
            return redirect(url_for("graficar_parabolico"))
        elif request.form["submit_button"] == "Movimiento Circular":
            return redirect(url_for("graficar_circular"))

    return render_template("index.html")

def calcular_movimiento_circular(radio, velocidad_angular):
    try:
        # Crear listas para almacenar los datos de posición en X e Y
        x_data = []
        y_data = []
        velocidad_tangencial_data = []  # Lista para almacenar la velocidad tangencial
        aceleracion_radial_data = []    # Lista para almacenar la aceleración radial
        
        # Calcular el movimiento circular con intervalos de 0.01 segundos
        tiempo_final = 10.0  # Cambia esto según tus necesidades
        tiempo_intervalo = 0.01
        tiempo_actual = 0.0
        
        while tiempo_actual <= tiempo_final:
            x = radio * np.cos(velocidad_angular * tiempo_actual)
            y = radio * np.sin(velocidad_angular * tiempo_actual)
            x_data.append(x)
            y_data.append(y)
            
            # Calcular velocidad tangencial y aceleración radial en cada punto
            velocidad_tangencial = radio * velocidad_angular  # V = R * ω
            velocidad_tangencial_data.append(velocidad_tangencial)
            
            aceleracion_radial = radio * (velocidad_angular ** 2)  # a = R * ω^2
            aceleracion_radial_data.append(aceleracion_radial)
            
            tiempo_actual += tiempo_intervalo
        
        # Crear la gráfica
        plt.figure(figsize=(8, 6))
        plt.plot(x_data, y_data)
        plt.title("Movimiento Circular")
        plt.xlabel("Posición en X")
        plt.ylabel("Posición en Y")
        plt.grid(True)
        plt.savefig("static/circular_plot.png")  # Guardar la gráfica en un archivo

        # Calcular el diámetro
        diametro = 2 * radio
        
        # Calcular la velocidad lineal
        velocidad_lineal = radio * velocidad_angular  # V = R * ω
        
        # Calcular el período
        periodo = 2 * np.pi / velocidad_angular
        
        # Calcular la frecuencia
        frecuencia = 1 / periodo
        
        return diametro, velocidad_lineal, periodo, frecuencia, velocidad_tangencial_data, aceleracion_radial_data
    except ValueError:
        return None, None, None, None, None, None

@app.route("/circular", methods=["GET", "POST"])
def graficar_circular():
    if request.method == "POST":
        try:
            # Obtener datos para el movimiento circular
            radio = float(request.form["radio"])
            velocidad_angular = float(request.form["velocidad_angular"])
            
            (diametro, velocidad_lineal, periodo, frecuencia,
            velocidad_tangencial_data, aceleracion_radial_data) = calcular_movimiento_circular(radio, velocidad_angular)

            if diametro is not None:
                return render_template("index_circular.html", plot=True, 
                                    diametro=diametro, velocidad_lineal=velocidad_lineal,
                                    periodo=periodo, frecuencia=frecuencia,
                                    velocidad_tangencial=velocidad_tangencial_data,
                                    aceleracion=aceleracion_radial_data,
                                    velocidad_angular=velocidad_angular)
            else:
                error_message = "Por favor, ingresa valores numéricos válidos."
                return render_template("index_circular.html", error=error_message)
        except ValueError:
            error_message = "Por favor, ingresa valores numéricos válidos."
            return render_template("index_circular.html", error=error_message)

    return render_template("index_circular.html", plot=False)

if __name__ == "__main__":
    app.run(debug=True)
