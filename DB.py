import mysql.connector
from mysql.connector import errors
import config
import random

def conectar():
    """Conectar con la base de datos y devolver un obj conexion."""
    try:
        conn = mysql.connector.connect(**config.credenciales)
    except errors.DatabaseError as err:
        print("Error al conectar.", err)
    else:
        return conn

def getNombresIDRecetas():
    """ Obtener todos los nombres y id de las recetas que esten en la bdd """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, tiempo_preparacion FROM receta")
    resultado = cur.fetchall()
    conn.close()
    return resultado

def get_recetas(tipo="all"):
    """Obtener las recetas segun el tipo.

    Tipo es 'all' (todas), 'done' (completadas) o 'pending' (pendientes)
    La cadena de la consulta se arma dependiendo del valor de tipo.
    Si tipo es 'all', no se incluye la clausula WHERE.
    Si tipo es 'done' se incluye el WHERE, con completadas = true
    Si tipo es 'pending' se incluye el WHERE, con completadas = false
    """
    consulta = """SELECT id, receta, tiempo_preparacion
                    FROM receta {}
                    ORDER BY fecha_creacion DESC"""
    where = "WHERE completada = {}"
    if tipo == "done":
        consulta = consulta.format(where.format("true"))
    elif tipo == "pending":
        consulta = consulta.format(where.format("false"))
    elif tipo == "all":
        consulta = consulta.format("")
    conn = conectar()
    cur = conn.cursor()
    cur.execute(consulta)
    resultado = cur.fetchall()
    conn.close()
    print(resultado)
    return resultado
    
def getIDRandom():
    """Obtener todos los ids en orden descendente para conocer el ultimo"""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id FROM RECETA ORDER BY id desc")
    resultado = cur.fetchall()
    conn.close()
    listaDeIds = []
    for id in resultado:
        listaDeIds.append(int(id[0]))
    return random.choice(listaDeIds)
    
def getReceta(id):
    """ Obtener una receta que esten en la bdd """
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM RECETA WHERE id = %s", (id,))
    resultado = cur.fetchall()
    conn.close()
    return resultado
    
def nueva_receta(data):
    """Insetar nueva receta a la db"""
    tupla = (data["nombre"], data["ingredientes"], data["etiquetas"], data["preparacion"], data["tiempo_preparacion"], data["tiempo_coccion"], data["fav"])
    query= "INSERT INTO receta (nombre, ingredientes, etiquetas, preparacion, tiempo_preparacion, tiempo_coccion, favorita) VALUES (%s,%s,%s,%s,%s,%s, %s)"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, tupla)
    conn.commit()
    conn.close()

def eliminar_receta(id_receta):
    """Eliminar receta id_receta de la base de datos."""
    query = "DELETE FROM receta WHERE id = %s"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (id_receta,))
    conn.commit()
    conn.close()

def create_if_not_exists():
    """Crea la base de datos y la tabla si no existen"""
    
    create_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    create_table = """CREATE TABLE IF NOT EXISTS receta(
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                nombre VARCHAR(100) NOT NULL,
                                ingredientes TEXT NOT NULL,
                                etiquetas TEXT NOT NULL,
                                fecha_creacion DATE DEFAULT (DATE(NOW())),
                                preparacion TEXT NOT NULL,
                                tiempo_preparacion INT NOT NULL,
                                tiempo_coccion INT NOT NULL,
                                favorita BOOLEAN DEFAULT FALSE
                                );"""

    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                        password=config.credenciales["password"],
                                        host="127.0.0.1")
        cur = conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(create_table)
        conn.commit()
        conn.close()
        print("-- Bases de datos creada!")
    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise