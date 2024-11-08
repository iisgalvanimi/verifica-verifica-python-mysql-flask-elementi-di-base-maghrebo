#Importazioni delle diverse librerie
import mysql.connector
from flask import Flask, jsonify, request

#Connessione al database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="rettili"
)

#Creazione del cursore con cui operare nel database
mycursor = mydb.cursor()

#Creazioned dell'app flask per gestire le richieste HTTP
app = Flask(__name__)



#-----------------------------------------------------------------------------
#Definizione della funzione per il metodo GET

def getAllData():
    mycursor.execute("SELECT * FROM rettili")
    myresult = mycursor.fetchall()
    result = [];
    for x in myresult:
        print(x);
        result.append(x);
    return result


#Indirizzamento delle diverse route che poi richiamano le funzioni correlate
@app.route("/dati")
def stampaDati():
    data = getAllData()
    return jsonify({"La tabella rettili: ": data})


#Creazione della route principale vuota senza errore
@app.route("/")
def homeRoute():
    return "Buongiorno, questa è la route di default. Per avere la lista dei rettili, inserisci come route /dati"



#-----------------------------------------------------------------------------
#Definizione della funzione per il metodo POST

def aggiungiRettile(data):
    query = "INSERT INTO rettili (nome, famiglia, dimensioni, habitat, alimentazione) VALUES (%s, %s, %s, %s, %s)"
    valori = (data['nome'], data['famiglia'], data['dimensioni'], data['habitat'], data['alimentazione'])
    mycursor.execute(query, valori)
    mydb.commit()
    return mycursor.rowcount

@app.route("/add", methods=["POST"])
def aggiunta():
    data = request.json
    if not data:
        return jsonify({'message': 'Nessun dato fornito'}), 400

    required_fields = ['nome', 'famiglia', 'dimensioni', 'habitat', 'alimentazione']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Probabilmente i dati sono mancanti o errati'}), 400

    rows_inserted = aggiungiRettile(data)
    if rows_inserted == 1:
        return jsonify({'message': 'congratulazioni, il rettile e stato inserito con successo'}), 201
    else:
        return jsonify({'message': 'Errore durante l inserimento del rettile'}), 500