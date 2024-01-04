from flask import Flask, request, jsonify
from connect_msql import ConnectMySQL  # Asumiendo que tu clase está en connect_mysql.py

app = Flask(__name__)



@app.route('/list_exercises/<int:tipo>', methods=['GET'])
def list_exercises(tipo):
    connector = ConnectMySQL()
    exercises = connector.list_exercises(tipo)
    connector.exit()
    return jsonify(exercises)



@app.route('/insert_series', methods=['POST'])
def insert_series():
    data = request.json
    print(data)
    id_ejercicio = data['id_ejercicio']
    repes = data['repes']
    peso = data['peso']
    connector = ConnectMySQL()
    success = connector.insert_series(id_ejercicio, repes, peso)
    connector.exit()
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(debug=True)
