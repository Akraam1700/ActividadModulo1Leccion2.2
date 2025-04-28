from flask import Flask, request, jsonify

app = Flask(__name__)


usuarios = []


@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "sistema": "Gestion de usuarios",
        "version": "1.0",
        "desarrollador": "Yandereck Roman"
    })


@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    datos = request.get_json()
    
    if not datos:
        return jsonify({"error": "No se envió ningún dato"}), 400

    nombre = datos.get('nombre')
    correo = datos.get('correo')

    if not nombre or not correo:
        return jsonify({"error": "Faltan datos: nombre y correo son obligatorios."}), 400
    
    usuario = {
        "nombre": nombre,
        "correo": correo
    }
    usuarios.append(usuario)
    
    return jsonify({"mensaje": "Usuario creado exitosamente", "usuario": usuario}), 201


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})

if __name__ == '__main__':
    app.run(debug=True)
