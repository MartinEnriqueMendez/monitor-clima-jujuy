import sqlite3
def init_db(db_name: str = "clima_agro.db") -> None:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS mediciones(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
                           temperatura REAL,
                           humedad INTEGER,
                           descripcion TEXT
                       )
                       ''')
        conn.commit()

def save_measurement(temp: float, hum: int, desc: str, db_name: str = "clima_agro.db") -> None:
   with sqlite3.connect(db_name) as conn:
       cursor = conn.cursor()
       cursor.execute(
           "INSERT INTO mediciones (temperatura, humedad, descripcion) VALUES (?, ?, ?)",
       (temp, hum, desc)
       ) 
       conn.commit()