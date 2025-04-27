
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/info', methods=['GET'])
def get_info():
    """
    This route returns basic information about the application.
    """

    app_info = {
        "application_name": "Mi Servidor Flask Básico",
        "version": "1.0.0",
        "description": "Un servidor simple para la Actividad de la Lección.",
        "endpoints": {
            "/info": "GET - Devuelve esta información.",
            "/mensaje": "POST - Recibe un mensaje JSON y devuelve una respuesta."
        }
    }
   
    return jsonify(app_info)

@app.route('/mensaje', methods=['POST'])
def post_mensaje():
    """
    This route receives a message in JSON format and returns a custom response.
    Expects JSON like: {"message": "Your text here"}
    """

    if not request.is_json:

        return jsonify({"error": "La solicitud debe ser de tipo JSON"}), 400 

    data = request.get_json()


    if 'message' not in data:

        return jsonify({"error": "Falta el campo 'message' en el JSON"}), 400 

    received_message = data['message']

    response_message = {
        "status": "Mensaje recibido con éxito",
        "your_message_was": received_message,
        "reply": f"Gracias por enviar: '{received_message}'"
    }

    return jsonify(response_message), 200 

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
