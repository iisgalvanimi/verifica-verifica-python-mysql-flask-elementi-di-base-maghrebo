import mysql.connector

def Creazione_DB():

    #Connessione al database locale con le credenziali di root
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password=""
    )

    #Creazione del cursore con cui agire sul database
    mycursor = mydb.cursor()

    #Qua creiamo il database rettili nel pc locale in remoto
    mycursor.execute("CREATE DATABASE IF NOT EXISTS rettili")


#-----------------------------------------------------------------------

def Creazione_Tabella():

    #Effettuiamo una ricconessione al database rettili
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="rettili"
    )

    #Ricreazione del cursore con cui agire sul database
    mycursor = mydb.cursor()

    #Qua facciamo la creazione della tabella sottostante nel database rettili
    mycursor.execute("CREATE TABLE IF NOT EXISTS rettili (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, nome VARCHAR(255), famiglia VARCHAR(255), dimensioni VARCHAR(255), habitat VARCHAR(255), alimentazione VARCHAR(255))")


#-----------------------------------------------------------------------


def Popolazione_Tabella():

    #Connessione al database locale proprio su quello in cui stiamo lavorando sempre rettili
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="rettili"
    )

    #Ricreazione del cursore con cui agire sul database
    mycursor = mydb.cursor()

    #Impostazione della query
    sql = "INSERT INTO rettili (nome, famiglia, dimensioni, habitat, alimentazione) VALUES (%s, %s, %s, %s, %s)"

    #Impostazione dei valori dei vari rettili
    rettili = [
        ("Camaleonte comune", "Chamaeleonidae", "20-30 cm", "Foreste tropicali", "Insetti"),
        ("Iguana verde", "Iguanidae", "1-2 m", "Foreste pluviali", "Foglie, fiori"),
        ("Cobra reale", "Elapidae", "3-5 m", "Foreste, zone umide", "Uccelli, piccoli mammiferi"),
        ("Tartaruga marina", "Cheloniidae", "1-2 m", "Oceani", "Meduse, crostacei"),
        ("Caimano nero", "Alligatoridae", "3-5 m", "Fiumi, paludi", "Pesci, mammiferi"),
        ("Geko tokay", "Gekkonidae", "20-30 cm", "Foreste tropicali", "Insetti"),
        ("Tartarughe delle Galapagos", "Testudinidae", "1-1.5 m", "Isole Galapagos", "Vegetali"),
        ("Pitone reale", "Pythonidae", "1-3 m", "Foreste tropicali", "Uccelli, mammiferi"),
        ("Basilisco", "Corytophanidae", "30-60 cm", "Foreste tropicali", "Insetti"),
        ("Lucertola dei muri", "Lacertidae", "15-20 cm", "Muri, rocce", "Insetti")  
        ]

    #Esecuzione della query insieme ai valori
    mycursor.executemany(sql, rettili)

    mydb.commit()
    #Output della buon riuscita dell'inserimento dei dati
    print(mycursor.rowcount, "tutti i dati sono stati inseriti nella tabella rettili")


#-----------------------------------------------------------------------

#Richiamo delle funzioni in ordine da eseguire per la creazione sia del database, che della tabella che la popolazione con i dati
Creazione_DB()
Creazione_Tabella()
Popolazione_Tabella()