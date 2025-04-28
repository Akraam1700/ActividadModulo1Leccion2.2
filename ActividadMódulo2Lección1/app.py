from flask import Flask, render_template

app = Flask(__name__)

# Datos dinámicos para las plantillas
productos = [
    {"nombre": "Laptop Lenovo", "precio": 850, "stock": 10},
    {"nombre": "Auriculares Sony", "precio": 150, "stock": 25},
    {"nombre": "Teclado Mecánico", "precio": 100, "stock": 30},
]

empleados = [
    {"nombre": "Juan", "edad": 28, "departamento": "Ventas"},
    {"nombre": "María", "edad": 35, "departamento": "IT"},
    {"nombre": "Luis", "edad": 40, "departamento": "Ventas"},
    {"nombre": "Ana", "edad": 25, "departamento": "Marketing"},
    {"nombre": "Carlos", "edad": 32, "departamento": "IT"},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos_lista():
    return render_template('productos.html', productos=productos)

@app.route('/empleados')
def empleados_lista():
    return render_template('empleados.html', empleados=empleados)

if __name__ == '__main__':
    app.run(debug=True)
