from datetime import datetime
# Load environment variables from the .env file
import os
import MySQLdb
import pandas as pd


class ConnectMySQL:
    
    def __init__(self) -> None:
        DATABASE_HOST='gcp.connect.psdb.cloud'
        DATABASE_USERNAME='uue480vr7f5qz4r2a07p'
        DATABASE_PASSWORD='pscale_pw_fJYl35GzlyTWMzMrGEeQTDL1fMfA3pQQdWWxCqfvUSH'
        DATABASE='fitness_notes'

        # Connect to the database
        self.connection = MySQLdb.connect(
        host=DATABASE_HOST,
        user=DATABASE_USERNAME,
        passwd=DATABASE_PASSWORD,
        db=DATABASE,
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
        # to determine the path to your operating systems certificate file.
        #   ssl={ "ca": "" }
        )


    def get_day(self):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        # day en formato lunes, martes, miercoles, jueves, viernes, sabado, domingo
        day = now.strftime("%A")
        days = {'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miercoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sabado', 'Sunday': 'Domingo'}
        df = pd.read_sql(f"SELECT ID_Dia FROM DIM_DIA where Nombre='{days[day]}'", con=self.connection)
        return df.values[0][0]


    #numpy, numpy, python-dateutil, pytz, tzdata, mysqlclient, pandas


    def insert_exercie(self,id_ejercicio, id_usuario = 1):
        # dia de hoy en formato lunes, martes, miercoles, jueves, viernes, sabado, domingo
        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.connection.cursor()
        print(f"INSERT INTO FACT_REGISTRO_EJERCICIOS (ID_Ejercicio, ID_Usuario, Insert_date, ID_Dia) VALUES ({id_ejercicio},{id_usuario},'{date}',{self.get_day()})")
        cursor.execute(f"INSERT INTO FACT_REGISTRO_EJERCICIOS (ID_Ejercicio, ID_Usuario, Insert_date, ID_Dia) VALUES ({id_ejercicio[0]},{id_usuario},'{date}',{self.get_day()})")
        cursor.close()
        
        return pd.read_sql(f"SELECT max(ID_Registro_Ejercicio) FROM FACT_REGISTRO_EJERCICIOS where Insert_date='{date}'", con=self.connection).values[0][0]
    def list_exercises(self,tipo):
        df = pd.read_sql(f"SELECT ID_Ejercicio, Nombre FROM DIM_EJERCICIO where ID_tipoEjercicio={tipo}", con=self.connection)
        dict = df.set_index('Nombre').T.to_dict('list')
        return dict

    def insert_series(self,id_ejercicio,  repes, peso):
        print(id_ejercicio, repes, peso)
        # dia de hoy en formato lunes, martes, miercoles, jueves, viernes, sabado, domingo
        id_registro_ejercicio =  self.insert_exercie([id_ejercicio])
        for i in range(1, len(repes)+1):
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO FACT_SERIES (ID_Registro_Ejercicio, Repeticiones, Serie, Peso) VALUES ({id_registro_ejercicio},{repes[i-1]},{i},{peso[i-1]})")
            cursor.close()
        return True
    def exit(self):
        self.connection.close()
        return True
if __name__ == '__main__':
    connect = ConnectMySQL()
    # connect.insert_exercie(1)
    print(connect.list_exercises(1))
    # connect.insert_series(1,[10,10,10],[40,40,40])