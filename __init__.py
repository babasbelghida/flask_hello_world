from flask import Flask, render_template, jsonify, request, redirect, url_for

import sqlite3
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
@app.route("/fr/")
def monfr():
    return "<h2>Bonjour tout le monde !</h2>"

from flask import Flask, jsonify
from urllib.request import urlopen
import json

app = Flask(__name__)

@app.route('/paris/')
def meteo():
    api_key = 'bd5e378503939ddaee76f12ad7a97608'
    url = 'https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=' + api_key

    try:
        response = urlopen(url)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))

        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('temp', {}).get('day') - 273.15  # Conversion de Kelvin en °C 
            results.append({'Jour': dt_value, 'temp': temp_day_value})

        return jsonify(results=results)

    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()

    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/recherche_fiche_client/<string:name>')
def Readfichesearch(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Utilisation du nom du paramètre correct dans la requête SQL
    param = "%" + name + "%"
    cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', (param,))
    data = cursor.fetchall()
    conn.close()

    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/ajouter_client/', methods=['GET', 'POST'])
def ajouter_client():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']

        # Insérer les données dans la base de données
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, adresse))
        conn.commit()
        conn.close()

        # Rediriger vers la page de consultation des clients après l'ajout
        return redirect(url_for('ReadBDD'))

    # Si la méthode est GET, simplement rendre le template du formulaire
    return render_template('ajouter_client.html')

if __name__ == "__main__":
    app.run(debug=True)
