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



#----------------------------------------------------------------------------------------------------------------------------------------------------
#Definizione della funzione per il metodo POST

#La funzione da richiamare dalla route con ritorno del conteggio delle righe per verifica di inserimento correto nel DB
def aggiungiRettile(data):
    #Instaurazione della query per il DB
    query = "INSERT INTO rettili (nome, famiglia, dimensioni, habitat, alimentazione) VALUES (%s, %s, %s, %s, %s)"
    #Estrazione dei valori dal json
    valori = (data['nome'], data['famiglia'], data['dimensioni'], data['habitat'], data['alimentazione'])
    #Esecuzione con il cursore la query attribuendo insieme i valori
    mycursor.execute(query, valori)
    #Commit sul database per confermare le modifiche
    mydb.commit()
    #Ritorno del conteggio delle righe per verifica
    return mycursor.rowcount

#Route per l'aggiunta con il metodo POST
@app.route("/add", methods=["POST"])
def aggiunta():
    #Richiesta del json e salvato nella variabile
    data = request.json
    #Se il file è vuoto
    if not data:
        return jsonify({'message': 'Nessun dato fornito'}), 400

    #Dichiarazione dei campi necessari
    required_fields = ['nome', 'famiglia', 'dimensioni', 'habitat', 'alimentazione']
    #Controllo dell'effettivo inserimento dei campi
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Probabilmente i dati sono mancanti o errati'}), 400

    #Creazione della variabile nella quale immagino il ritorno del risultato della funzione
    rows_inserted = aggiungiRettile(data)
    #Verifica dal controllo ricevuto
    if rows_inserted == 1:
        return jsonify({'message': 'congratulazioni, il rettile e stato inserito con successo'}), 201
    else:
        return jsonify({'message': 'Errore durante l inserimento del rettile'}), 500


#----------------------------------------------------------------------------------------------------------------------------------------------------
#Definizione della funzione per il metodo DELETE

#Creazione delle funzione che sempre con ritorno della variabile per la verifica
def deleteRettile(id):
    #Impostazioned della query per il database
    query = "DELETE FROM rettili WHERE id = %s"
    #Creazione sempre nuovamente del cursore con cui operare nel Database
    mycursor.execute(query, (id,))
    #Commit per rendere effettive le modifiche appena eseguite
    mydb.commit()
    #Ritorno della variabile per la verifica
    return mycursor.rowcount

#Creazione della route per identificare quale id andare poi ad agire
@app.route("/delete/<id>", methods=["DELETE"])
#Creazione della funzione delete
def delete(id):
    #Creazione della variabile nella quale poi si andrà a immaginare la variabile di ritorno
    rows_deleted = deleteRettile(id)
    #Verifica dell'effetiva eliminazione del rettile
    if rows_deleted == 1:
        return jsonify({'message': 'Rettile eliminato con successo'}), 200
    else:
        return jsonify({'message': 'Errore durante l\'eliminazione del rettile o ID del rettile non trovato'}), 404


#----------------------------------------------------------------------------------------------------------------------------------------------------
#Definizione della funzione per il metodo PUT

#Funzione dell'effettiva query al database passando valori di id e dati
def updateRettile(id, data):
    #Instaurazione della query
    query = "UPDATE rettili SET nome = %s, famiglia = %s, dimensioni = %s, habitat = %s, alimentazione = %s WHERE id = %s"
    #Estrazione dei valori dal file json ricevuto
    valori = (data['nome'], data['famiglia'], data['dimensioni'], data['habitat'], data['alimentazione'], id)
    #Esecuzione sul database con il cursore, unendo la query e i valori
    mycursor.execute(query, valori)
    #Commit sul file per rendere effettive le modifiche al database
    mydb.commit()
    #Ritorno della variabile del conteggio delle righe per verifica della correttività
    return mycursor.rowcount


#Route per identificare la richiesta e il percorso inserito dall'utente
@app.route("/update/<id>", methods=["PUT"])
#Funzione eseguita dopo la route
def update(id):
    #Immaginamento del file json nella variabile data
    data = request.json
    #Dichiarazione dei file necessari
    required_fields = ['nome', 'famiglia', 'dimensioni', 'habitat', 'alimentazione']
    #Verifica se tutti i campi son stati inserito in caso contrario un messaggio
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Dati mancanti'}), 400

    #Creazione variabile la quale ricevera la variabile di ritorno della funzione correlata
    rows_updated = updateRettile(id, data)
    #Verifica che l'inserimento sia avvenuto giustamente
    if rows_updated == 1:
        return jsonify({'message': 'Rettile aggiornato con successo'}), 200
    else:
        return jsonify({'message': 'Errore durante l aggiornamento del rettile oppure ID del rettile non trovato'}), 404
