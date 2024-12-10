"""
Autores: [Samuel Zuluaga Valencia, Maria Camila Restrepo Cepeda]
Descripción: Sistema de Gestión de Diagnósticos Asistidos por Imágenes Médicas
"""
import mysql.connector
from pymongo import MongoClient
import bcrypt
from datetime import datetime
from mysql.connector import Error



# Configuración de MySQL
def setup_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="informatica1",
            password="info20242",
        )
        print(connection.is_connected())
        cursor = connection.cursor()

        # Crear base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS Informatica1_PF;")
        cursor.execute("USE Informatica1_PF;")

        # Crear tablas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('Administrador', 'Médico', 'Técnico') NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            edad INT NOT NULL,
            genero ENUM('Masculino', 'Femenino') NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_paciente INT NOT NULL,
            tipo_imagen VARCHAR(50) NOT NULL,
            resultado_ia VARCHAR(50) NOT NULL,
            fecha_diagnostico DATE NOT NULL,
            estado ENUM('Revisado', 'Pendiente') NOT NULL,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id)
        );
        """)

        print("Base de datos y tablas en MySQL creadas exitosamente.")

    except Exception as e:
        print(f"Error al configurar MySQL: {e}")

    finally:
        connection.close()
        cursor.close()

def insert_usuarios():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="informatica1",
            password="info20242",
            database="Informatica1_PF"
        )
        cursor = connection.cursor()

        # Contraseñas cifradas
        admin_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        medico_password = bcrypt.hashpw("medico123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        tecnico_password = bcrypt.hashpw("tecnico123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insertar usuarios
        cursor.execute("""
            INSERT INTO usuarios (username, password, role)
            VALUES 
            ('admin', %s, 'Administrador'),
            ('medico1', %s, 'Médico'),
            ('tecnico1', %s, 'Técnico')
            ON DUPLICATE KEY UPDATE password = VALUES(password), role = VALUES(role);
        """, (admin_password, medico_password, tecnico_password))

        connection.commit()
        print("Datos de prueba insertados correctamente en la base de datos.")

    except Exception as e:
        print(f"Error al insertar datos en MySQL: {e}")
    finally:
        connection.close()
# Insertar datos de prueba en MySQL

def insert_pacientes ():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="informatica1",
            password="info20242",
            database="Informatica1_PF"
        )
        cursor = connection.cursor()

        # Insertar pacientes
        cursor.execute("""
        INSERT INTO pacientes (nombre, edad, genero)
        VALUES 
        ('Juan Perez', 45, 'Masculino'),
        ('Maria Lopez', 37, 'Femenino')
        ('sol rivera', 27,'Femenino');
        """)

        # Insertar diagnósticos
        cursor.execute("""
        INSERT INTO diagnosticos (id_paciente, tipo_imagen, resultado_ia, fecha_diagnostico, estado)
        VALUES 
        (1, 'MRI', '85%', '2024-11-01', 'Revisado'),
        (2, 'CT', '75%', '2024-11-15', 'Pendiente'),
        (3,'Rayos X', '77%','2021-11-29', 'Pendiente');
        """)

        connection.commit()
        print("Datos de prueba insertados en MySQL.")

    except Exception as e:
        print(f"Error al insertar datos en MySQL: {e}")

    finally:
        connection.close()

client= MongoClient('localhost', 27017)
db= client.Informatica1_PF

        # Crear colecciones
imagenes=db.imagenes
reportes=db.reportes
# Configuración de MongoDB
def setup_mongodb():
    try:
        # Insertar datos en la colección 'imagenes'
        imagenes.insert_many([
            {
                "id_imagen": "img123",
                "id_paciente": 1,
                "tipo": "MRI",
                "fecha": datetime.strptime("2024-11-01", "%Y-%m-%d"),
                "notas_tecnicas": "Captura con contraste.",
                "zona_estudio": "Cerebro"
            },
            {
                "id_imagen": "img124",
                "id_paciente": 2,
                "tipo": "CT",
                "fecha": datetime.strptime("2024-11-15", "%Y-%m-%d"),
                "notas_tecnicas": "Sin contraste.",
                "zona_estudio": "Abdomen"
            },
            {
                "id_imagen": "img125",
                "id_paciente": 3,
                "tipo": "Rayos X",
                "fecha": datetime.strptime("2024-11-29", "%Y-%m-%d"),
                "notas_tecnicas": "Sin contraste.",
                "zona_estudio": "utero"
            }
        ])
        
        # Insertar datos en la colección 'reportes'
        reportes.insert_many([
            {
                "id_imagen": "img123",
                "id_paciente": 1,
                "fecha": "2024-11-20",
                "tipo": "MRI",
                "zona_estudio": "cerebro",
                "ruta": "/imagenes/mri/2024/11/20/img123_mri_cerebro.jpg",
                "analisis_IA": {
                    "condicion_sugerida": "Glioblastoma multiforme",
                    "prob": 85,
                    "notas": "Tamaño estimado: 2.5 x 3.0 cm, Realce heterogéneo de la lesión tras la administración de contraste intravenoso."
                },
                "notas_tecnicas": [
                    { 
                        "id_tecnica": "tech789", 
                        "fecha_nota": "2024-05-14", 
                        "texto": "Imagen capturada correctamente con contraste. No se reportaron problemas en la captura."
                    }
                ]
            },
            {
                "id_imagen": "img124",
                "id_paciente": 2,
                "fecha": "2024-11-15",
                "tipo": "CT",
                "zona_estudio": "abdomen",
                "ruta": "/imagenes/ct/2024/11/21/img124_ct_abdomen.jpg",
                "analisis_IA": {
                    "condicion_sugerida": "Masa hepática sospechosa",
                    "prob": 75,
                    "notas": "Masa de 4.5 cm en el lóbulo derecho del hígado, con bordes irregulares y captación de contraste en fase arterial."
                },
                "notas_tecnicas": [
                    { 
                        "id_tecnica": "tech790", 
                        "fecha_nota": "2024-11-21", 
                        "texto": "Imagen capturada con buena calidad técnica. No se observaron artefactos."
                    }
                ]
            },
            {
                "id_imagen": "img125",
                "id_paciente": 3, 
                "fecha": "2024-11-29",
                "tipo": "Rayos X",
                "zona_estudio": "útero",  # Corregido el error de sintaxis en la clave 'zona_estduio'
                "ruta": "/imagenes/rayosx/2024/12/07/img125_rayosx_utero.jpg",
                "analisis_IA": {
                    "condicion_sugerida": "Obstrucción de las trompas de Falopio",
                    "prob": 77,
                    "notas": "Presencia de cicatriz en las paredes de las trompas."
                },
                "notas_tecnicas": [
                    { 
                        "id_tecnica": "tech791", 
                        "fecha_nota": "2024-12-07", 
                        "texto": "Imagen capturada con buena calidad técnica."
                    }
                ]
            }
        ])

        # Mensaje de éxito
        print("Base de datos y colecciones en MongoDB creadas exitosamente.")

    except Exception as c:
        # Captura de errores
        print(f"Error al configurar MongoDB: {c}")

# Función de inicio de sesión


def validar_numero(msj):
    while True:
        valor = input(f"Ingrese {msj}: ")
        try:
            if "." in valor or "e" in valor.lower():
                numero = float(valor)  
            else:
                numero = int(valor)  
            return numero
        except ValueError:
            print("Solo se pueden ingresar números. Intentelo nuevamente.")

def validar_porcentaje():
    porcentaje = validar_numero()
    if 0 <= porcentaje <= 100:
        return porcentaje
    else:
        raise ValueError()

def validar_genero():
    while True:
        genero = input("Ingresa tu género (masculino/femenino): ").strip().lower()
        if genero in ["femenino", "masculino"]:
            return genero.capitalize()  
        else:
            print("Debes ingresar 'masculino' o 'femenino'. Inténtalo nuevamente.")

def validar_rol(rol):
    while True: 
        rol=input("Ingrese su rol: ").strip().capitalize
        roles = ["Administrador", "Medico", "Tecnico"]
        if rol in roles: 
            return rol
        else:
            print("Ingrese un rol permitido.")

def validar_letras(campo):
    while True:
        valor = input(f"Ingrese el valor para '{campo}': ").strip()
        if valor.isalpha():
            return valor
        else:
            print("solo debe contener letras. Inténtelo de nuevo.")

def validar_edad():
    while True:
        edad = input("Ingrese la edad en números: ").strip()
        if edad.isdigit() and 0 <= int(edad) <= 120:
            return int(edad) 
        else:
            print("La edad debe ser un número entre 0 y 120. Inténtelo de nuevo.")

#funciones para usuarios 
        
def añadir_usuario():

    usuario=input("Ingrese su nombre de Usuario: ")
    contraseña= input("Ingrese su contraseña: ")
    rol= input("Ingrese su rol: ")

    if not validar_rol(rol):
        return

    conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )
    if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "INSERT INTO Usuarios (user_id, username, password, role) VALUES (NULL, %s, %s, %s)"
            cursor.execute(sql, (usuario, contraseña, rol))
            conexion.commit()

            print(f"El usuario '{usuario}' fue agregado exitosamente a la base de datos.")
    
def  eliminar_usuario(): 
    try:
        id = validar_numero("el ID del usuario a eliminar: ")

        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql_select = "SELECT * FROM Usuarios WHERE user_id = %s"
            cursor.execute(sql_select, (id,))
            resultado = cursor.fetchone()

            if resultado:
                sql_delete = "DELETE FROM Usuarios WHERE user_id = %s"
                cursor.execute(sql_delete, (id,))
                conexion.commit()
                print(f"El usuario con ID '{id}' ha sido eliminado.")
            else:
                print(f"No se encontró un usuario con ID '{id}' en la base de datos.")

    except Error as c:
        print(f"Error al interactuar con la base de datos: {c}")
    except Exception as c:
        print(f"Error inesperado: {c}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass  

def actualizar_usuario(): 
    try:
        id = validar_numero("el ID del usuario a actualizar: ")

        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql_select = "SELECT * FROM Usuarios WHERE user_id = %s"
            cursor.execute(sql_select, (id,))
            resultado = cursor.fetchone()

            if resultado:
                nuevo_username = input("Ingrese el nuevo username: ")
                nueva_password = validar_numero("la nueva contraseña: ")
                nuevo_role = validar_rol(input("Ingrese el nuevo rol (Administrador, Medico, Tecnico): "))
                sql_update = """
                    UPDATE Usuarios 
                    SET username = %s, password = %s, role = %s 
                    WHERE user_id = %s
                """
                cursor.execute(sql_update, (nuevo_username, nueva_password, nuevo_role, id))
                conexion.commit()

                print(f"Usuario con ID '{id}' actualizado con éxito.")
            else:
                print(f"No se encontró un usuario con ID '{id}' en la base de datos.")

    except Error as c:
        print(f"Error al interactuar con la base de datos: {c}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass 

def mostrar_usuarios():
    try:
        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Usuarios")
            resultados = cursor.fetchall()

            if resultados:
                print("Lista de usuarios:")
                for row in resultados:
                    print(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}, Role: {row[3]}")
            else:
                print("No se encontraron usuarios en la base de datos.")
    except Error as c:
        print(f"Error al interactuar con la base de datos: {c}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass

#funciones para la tabla de pacientes 

def agregar_paciente(): 

    id = validar_numero("Ingrese el ID del paciente: ")
    nombre = validar_letras("Ingrese el nombre del paciente: ")
    edad = validar_edad()
    genero = validar_genero()
    historia = input("Ingrese el historial de diagnósticos del paciente (si tiene): ")

    conexion = mysql.connector.connect(user='informatica1', password='info20242', host='127.0.0.1', database='Informatica1_PF')
    cursor = conexion.cursor()

    sql = "INSERT INTO Pacientes (paciente_id, nombre, edad, genero, historial_diagnosticos) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (id, nombre, edad, genero, historia))

    conexion.commit()
    print(f"Paciente '{nombre}' agregado con éxito.")
    cursor.close()
    conexion.close()

def actualizar_paciente():
    try:
        paciente_id = validar_numero("Ingrese el ID del paciente a actualizar: ")
        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql_check = "SELECT * FROM Pacientes WHERE paciente_id = %s"
            cursor.execute(sql_check, (paciente_id,))
            resultado = cursor.fetchone()

            if resultado:
                nuevo_nombre = validar_letras(input("Ingrese el nuevo nombre del paciente: "), "Nuevo Nombre")
                nueva_edad = validar_edad()
                nuevo_genero = validar_genero()
                nueva_historia = input("Ingrese el nuevo historial de diagnósticos del paciente: ")

                sql_update = '''
                    UPDATE Pacientes 
                    SET nombre = %s, edad = %s, genero = %s, historial_diagnosticos = %s 
                    WHERE paciente_id = %s
                '''
                cursor.execute(sql_update, (nuevo_nombre, nueva_edad, nuevo_genero, nueva_historia, paciente_id))

                conexion.commit()
                print(f"Paciente '{paciente_id}' actualizado con éxito.")
            else:
                print(f"No se encontró un paciente con ID '{paciente_id}' en la base de datos.")
    
    except Error as e:
        print(f"Error al interactuar con la base de datos: {e}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass  

def mostrar_pacientes():
    conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF')
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM Pacientes")
    resultados = cursor.fetchall()
    if resultados:
        for row in resultados:
            print(f"ID: {row[0]}, Nombre: {row[1]}, Edad: {row[2]}, Género: {row[3]}")
    else:
        print("No fue posible encontrar pacientes en la base de datos.")
    
    cursor.close()
    conexion.close()


def buscar_paciente():
    try:
        id = validar_numero("Ingrese el ID del paciente a buscar: ")
        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "SELECT * FROM Pacientes WHERE paciente_id = %s"
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()
            if resultado:
                print(f"El paciente fue encontrado:")
                print(f"   ID: {resultado[0]}")
                print(f"   Nombre: {resultado[1]}")
                print(f"   Edad: {resultado[2]}")
                print(f"   Género: {resultado[3]}")
                print(f"   Historial: {resultado[4]}")
            else:
                print(f"No fue posible encontrar un paciente con ID '{id}' en la base de datos.")

    except Error as c:
        print(f"Error al interactuar con la base de datos: {c}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass 

#funciones tablas de diagnosticos 
def agregar_diagnostico():
    try:
        paciente_id = validar_numero("Ingrese el ID del paciente: ")
        tipo_imagen = validar_letras("Ingrese el tipo de imagen (MRI, CT, Rayos X): ")
        resultado_IA = validar_numero("Ingrese el resultado de IA (en %): ")
        fecha_diagnostico = input("Ingrese la fecha del diagnóstico (YYYY-MM-DD): ")
        fecha_toma_imagen = input("Ingrese la fecha de la toma de la imagen (YYYY-MM-DD): ")
        estado_revision = validar_letras("Ingrese el estado de revisión (Revisado/Pendiente): ")
        conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = '''INSERT INTO Diagnosticos (paciente_id, tipo_imagen, resultado_IA, fecha_diagnostico, fecha_toma_imagen, estado_revision)
                     VALUES (%s, %s, %s, %s, %s, %s)'''
            
            cursor.execute(sql, (paciente_id, tipo_imagen, resultado_IA, fecha_diagnostico, fecha_toma_imagen, estado_revision))
            conexion.commit()

            print(f" El diagnóstico para el paciente con ID '{paciente_id}' fue agregado con éxito.")

    except Error as c:
        print(f"Error al interactuar con la base de datos: {c}")
   
    finally:
        try:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()
        except NameError:
            pass  

def mostrar_diagnosticos():
    conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Diagnosticos")
    resultados = cursor.fetchall()
    if resultados:
        for row in resultados:
            print(f"Paciente ID: {row[0]}, Imagen: {row[1]}, Resultado IA: {row[2]}%, Fecha del diagnóstico: {row[3]}, Fecha de la toma de la imagen: {row[4]}, Revisión: {row[5]}")
    else:
        print("No se encontraron diagnósticos en la base de datos.")

def buscar_diagnostico():
    id = validar_numero("Ingrese el ID del paciente para buscar su diagnóstico: ")
    conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )
    cursor = conexion.cursor()
    
    sql = "SELECT * FROM Diagnosticos WHERE paciente_id = %s"
    cursor.execute(sql, (id,))
    resultado = cursor.fetchone()
    if resultado:
        print(f"Paciente ID: {resultado[0]}, Imagen: {resultado[1]}, Resultado IA: {resultado[2]}%, Fecha toma imagen: {resultado[3]}, Fecha diagnóstico: {resultado[4]}, Revisión: {resultado[5]}")
    else:
        print(f"No se encontró ningún diagnóstico para el paciente con ID {id}.")
    cursor.close()
    conexion.close()

def actualizar_diagnostico():
   
    id = validar_numero("Ingrese el ID del paciente para actualizar su diagnóstico: ")
    tipo_imagen = validar_letras("Ingrese el nuevo tipo de imagen (MRI, CT, Rayos X): ")
    resultado_IA = validar_numero("Ingrese el nuevo resultado de IA (en %): ")
    fecha_diagnostico = input("Ingrese la nueva fecha del diagnóstico (YYYY-MM-DD): ")
    fecha_toma_imagen = input("Ingrese la nueva fecha de la toma de la imagen (YYYY-MM-DD): ")
    estado_revision = validar_letras("Ingrese el nuevo estado de revisión (Revisado/Pendiente): ")
    conexion = mysql.connector.connect(
            user='informatica1',
            password='info20242',
            host='127.0.0.1',
            database='Informatica1_PF'
        )
    cursor = conexion.cursor()
    sql = "SELECT * FROM Diagnosticos WHERE paciente_id = %s"
    cursor.execute(sql, (id,))
    resultado = cursor.fetchone()
    if resultado:
        sql_update = '''UPDATE Diagnosticos SET tipo_imagen = %s, resultado_IA = %s, fecha_diagnostico = %s,
                        fecha_toma_imagen = %s, estado_revision = %s WHERE paciente_id = %s'''
        cursor.execute(sql_update, (tipo_imagen, resultado_IA, fecha_diagnostico, fecha_toma_imagen, estado_revision, id))

        conexion.commit()
        print(f" El diagnóstico para el paciente con ID '{id}'  fue actualizado con éxito.")
    else:
        print(f"No se encontró un diagnóstico para el paciente con ID '{id}'.")
    cursor.close()
    conexion.close()

#funiciones de mongoDB

def ingresar_imagenes(db):
    while True:
        try:
            print(" Ingresar una nueva imagen médica ")
            id_imagen = input("Ingrese el ID de la imagen: ").strip()
            id_paciente = validar_numero("Ingrese el ID del paciente: ")
            fecha = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
            tipo = validar_letras("Ingrese el tipo de imagen: ")
            zona_estudio= validar_letras("Ingrese la parte del cuerpo: ") 
            preliminar = validar_numero("Ingrese el resultado preliminar del análisis por IA en %: ")
            ruta = input("Ingrese la ruta del archivo de imagen: ").strip()

            nueva_imagen = {
                "id_imagen": id_imagen,
                "id_paciente": id_paciente,
                "fecha": fecha,
                "tipo": tipo,
                "zona_estudio": zona_estudio,
                "preliminar": preliminar,
                "ruta": ruta
            }

            imagenes.insert_one(nueva_imagen)
            print(" La imagen fue agregada correctamente.")
            break  

        except ValueError as c:
            print(f"Error de validación: {c}. Por favor, ingrese los datos nuevamente.")

def ingresar_reportes_medicos(db):
    try:
       
        id_imagen = input("Ingrese el ID de la imagen: ").strip()
        id_paciente = validar_numero("Ingrese el ID del paciente: ")
        fecha = input("Ingrese la fecha del reporte (YYYY-MM-DD): ").strip()
        tipo = validar_letras("Ingrese el tipo de imagen:" )
        zona_estudio = validar_letras("Ingrese la parte del cuerpo: ")
        ruta = input("Ingrese la ruta del archivo de imagen: ")
        condicion_sugerida = validar_letras("Ingrese la condición sugerida por la IA: ")
        prob= validar_numero("Ingrese la probabilidad de la condición sugerida (%): ")
        notas_ia = validar_letras("Ingrese las notas del análisis de IA: ")
        id_tecnica = input("Ingrese el ID de la técnica: ").strip()
        fecha_nota_tecnica = input("Ingrese la fecha de la nota técnica (YYYY-MM-DD): ").strip()
        texto_nota_tecnica = validar_letras("Ingrese el texto de la nota técnica: ")
        
        notas_tecnicas = {
            "id_tecnica": id_tecnica,
            "fecha_nota": fecha_nota_tecnica,
            "texto": texto_nota_tecnica
        }
        reporte_nuevo = {
            "id_imagen": id_imagen,
            "id_paciente": id_paciente,
            "fecha": fecha,
            "tipo_imagen": tipo,
            "zona_estudio": zona_estudio,
            "ruta": ruta,
            "analisis_IA": {
                "condicion_sugerida": condicion_sugerida,
                "probabilidad_%": prob,
                "notas": notas_ia
            },
            "notas_tecnicas": notas_tecnicas
        }

        reportes.insert_one(reporte_nuevo)
        print("Reporte médico agregado correctamente.")

    except ValueError as c:
        print(f"Error de validación: {c}. Por favor, ingrese los datos correctamente.")

def editar_imagenes(db):
    try:
        # Pedimos al usuario el ID de la imagen que quiere editar
        id_imagen = input("Ingrese el ID de la imagen que desea editar: ").strip()

        # Buscar la imagen en la base de datos usando el ID
        imagen = imagenes.find_one({"id_imagen": id_imagen})

        if not imagen:
            print(f"No se encontró ninguna imagen con ID '{id_imagen}'.")
            return  # Si no se encuentra la imagen, termina la función

        print(f"Imagen encontrada: {imagen}")
        print("Ingrese los nuevos valores (deje en blanco para no cambiar).")

        # Solicitar nuevos datos
        nueva_fecha = input(f"Fecha actual: {imagen['fecha']} - Nueva fecha (YYYY-MM-DD): ").strip() or imagen['fecha']
        nueva_tipo = input(f"Tipo actual: {imagen['tipo']} - Nuevo tipo de imagen: ").strip() or imagen['tipo']
        nueva_zona = input(f"Zona de estudio actual: {imagen['zona_estudio']} - Nueva zona de estudio: ").strip() or imagen['zona_estudio']
        nueva_preliminar = input(f"Resultado preliminar actual: {imagen['preliminar']}% - Nuevo resultado preliminar (0-100): ").strip()
        nueva_ruta = input(f"Ruta actual: {imagen['ruta']} - Nueva ruta: ").strip() or imagen['ruta']

        # Validar el nuevo valor de preliminar (si fue proporcionado)
        if nueva_preliminar:
            try:
                nueva_preliminar = int(nueva_preliminar)
                if nueva_preliminar < 0 or nueva_preliminar > 100:
                    raise ValueError("El valor debe estar entre 0 y 100.")
            except ValueError as e:
                print(f"Error en el resultado preliminar: {e}")
                return

        # Crear un diccionario con los datos actualizados
        imagen_actualizada = {
            "fecha": nueva_fecha,
            "tipo": nueva_tipo,
            "zona_estudio": nueva_zona,
            "preliminar": nueva_preliminar if nueva_preliminar is not None else imagen['preliminar'],
            "ruta": nueva_ruta
        }

        # Actualizar la imagen en MongoDB
        db.imagenes.update_one({"id_imagen": id_imagen}, {"$set": imagen_actualizada})
        print("La imagen se ha actualizado correctamente.")

    except Exception as e:
        print(f"Error al editar la imagen: {e}")


def ver_imagenes(db):
    imagenes_cursor= imagenes.find()
    if not imagenes_cursor:
        print("No hay imágenes registradas en la base de datos.")
        return

    print("Imágenes: ")
    
    for imagen in imagenes_cursor:
        print(f"ID Imagen: {imagen.get('id_imagen')}")
        print(f"ID Paciente: {imagen.get('id_paciente')}")
        print(f"Fecha: {imagen.get('fecha')}")
        print(f"Tipo: {imagen.get('tipo')}")
        print(f"Zona de Estudio: {imagen.get('zona_estudio')}")
        print(f"Resultado IA (%): {imagen.get('preliminar')}")
        print(f"Notas Técnicas: {imagen.get('notas', 'No disponible')}")
        print(f"Ruta: {imagen.get('ruta')}")

def buscar_imagen_por_id(db):
    try:
        id_imagen = input("Ingrese el ID de la imagen: ").strip()
        imagen = db.imagenes.find_one({"id_imagen": id_imagen})

        if not imagen:
            print(f"No fue posible encontrar ninguna imagen con ID '{id_imagen}'.")
            return

        print(" Detalles de Imagen")
        print(f"ID Imagen: {imagen.get('id_imagen')}")
        print(f"ID Paciente: {imagen.get('id_paciente')}")
        print(f"Fecha: {imagen.get('fecha')}")
        print(f"Tipo: {imagen.get('tipo')}")
        print(f"zona_estudio: {imagen.get('zona_estudio')}")
        print(f"Resultado IA (%): {imagen.get('preliminar')}")
        print(f"Notas Técnicas: {imagen.get('notas')}")
        print(f"Ruta : {imagen.get('ruta')}")
    except Exception as c:
        print(f"Error al buscar la imagen: {c}")

def buscar_reportes(db):
    try: 
        id_paciente=input("Ingrese el ID del paciente: ")
        reporte=reportes.find_one({"id_paciente": id_paciente})

        if not reporte:
            print(f"No fue posible encontrar un reporte con el ID {id_paciente}")

        print(f"ID Reporte: {reporte.get('id_reporte')}")
        print(f"Fecha del Reporte: {reporte.get('fecha')}")
        print(f"Tipo: {reporte.get('tipo')}")
        print(f"Parte del Cuerpo: {reporte.get('zona_estudio')}")
        print(f"Ruta: {reporte.get('ruta')}")
        print(f"Condición Sugerida: {reporte.get('condicion_sugerida')}")
        print(f"Probabilidad (%): {reporte.get('probabilidad')}")
        print(f"Notas de la IA: {reporte.get('notas_ia')}")
        print("\n--- Notas Técnicas ---")
        notas_tecnicas = reporte.get('notas_tecnicas', {})
        print(f"ID Técnica: {notas_tecnicas.get('id_tecnica')}")
        print(f"Fecha Nota Técnica: {notas_tecnicas.get('fecha_nota')}")
        print(f"Texto Nota Técnica: {notas_tecnicas.get('texto')}")
    
    except Exception as c:
        print(f"Error al buscar la imagen: {c}")

def eliminar_imagen(db): 
    while True:
        print("Eliminar Imagen Médica")
        
        id_paciente = input("Ingrese el ID del paciente al que le desea eliminar la imagen: ").strip()
    
        imagen = imagenes.find_one({"id_paciente": id_paciente})
        
        if imagen:
            
            imagenes.delete_one({"id_paciente": id_paciente})
            print(f"La imagen con ID de paciente {id_paciente} ha sido eliminada exitosamente.")
            break  # Terminar la función después de eliminar la imagen
        else:
            print(f"No se encontró una imagen con ID de paciente {id_paciente}. Por favor ingrese el ID nuevamente.")


def mover_una_imagen(db):
    imagen1= input("Ingrese el ID de la imagen que desea buscar: ")

    imagen2 = imagenes.find_one({"id_imagen": imagen1})
    if not imagen2:
            print(" No se encontró ninguna imagen.")
            return
    if imagen2:
        n_path= input("Ingrese el nuevo enlace al que desea mover la imagen: ")
        imagenes.update_one(
                    {"id_imagen": imagen1},
                    {"$set": {"image_path": n_path}})
        print("La imagen se ha movido con éxito.")

def editar_reportes(db):
    try:
    
        id_paciente = input("Ingrese el ID del paciente cuyo reporte desea editar: ").strip()

     
        reporte = db.reportes.find_one({"id_paciente": id_paciente})  

       
        if not reporte:
            print(f"No se encontró ningún reporte para el paciente con ID {id_paciente}.")
            return

        nuevo_reporte = {
            "id_imagen": input("Ingrese el nuevo ID de la imagen: ").strip(),
            "fecha": input("Ingrese la nueva fecha (YYYY-MM-DD): ").strip(),
            "tipo": validar_letras("Ingrese el nuevo tipo de reporte: "), 
            "zona_estudio": validar_letras("Ingrese la nueva zona de estudio: "), 
            "ruta": input("Ingrese la nueva ruta del archivo: ").strip(),
            "prob": validar_porcentaje("Ingrese la nueva probabilidad (%): "),  
            "condicion_sugerida": validar_letras("Ingrese la nueva condición sugerida: "),  
            "notas_ia": validar_letras("Ingrese las nuevas notas del análisis de IA: "),
            "fecha_nota": input("Ingrese la nueva fecha de la nota técnica (YYYY-MM-DD): ").strip(),
            "texto_nota": validar_letras("Ingrese el nuevo texto de la nota técnica: ")
        }

        # Actualizar el reporte en la base de datos usando el ID del paciente
        db.reportes.update_one({"id_paciente": id_paciente}, {"$set": nuevo_reporte})  # Buscamos por id_paciente

        print("Reporte actualizado con éxito.")

    except Exception as c:
        print(f"Error al editar el reporte: {c}")

def ver_reportes(db):
    try:
        reportes1 = db["reportes"]
        reportes2 = reportes1.find()

        print(" Reportes Médicos ")
        reportes_encontrados = False

        for reporte in reportes2:
            reportes_encontrados = True
            print(f"\nID Reporte: {reporte.get('id_reporte', 'No disponible')}")
            print(f"ID Paciente: {reporte.get('id_paciente', 'No disponible')}")
            print(f"Fecha del Reporte: {reporte.get('fecha', 'No disponible')}")
            print(f"Tipo : {reporte.get('tipo', 'No disponible')}")
            print(f"zona estudio : {reporte.get('zona_estudio', 'No disponible')}")
            print(f"Ruta: {reporte.get('ruta', 'No disponible')}")
            print(f"Condición Sugerida: {reporte.get('condicion_sugerida', 'No disponible')}")
            print(f"Probabilidad (%): {reporte.get('prob', 'No disponible')}")
            print(f"Notas de la IA: {reporte.get('notas_ia', 'No disponible')}")
            notas_tecnicas = reporte.get('notas_tecnicas', {})
            print(f"ID Técnica: {notas_tecnicas.get('id_tecnica', 'No disponible')}")
            print(f"Fecha Nota Técnica: {notas_tecnicas.get('fecha_nota', 'No disponible')}")
            print(f"Texto Nota Técnica: {notas_tecnicas.get('texto', 'No disponible')}")

        if not reportes_encontrados:
            print(" No se encontraron reportes médicos en la base de datos.")

    except Exception as C:
        print(f"Ocurrió un error al mostrar los reportes médicos: {C}")

def eliminar_reporte(db):
  while True:
    print("Eliminar Reporte Médico")
    id_paciente1 = input("Ingrese el ID del paciente al que desea eliminar el reporte medico: ")

    reporte = reportes.find_one({"id_reporte": id_paciente1})
    if reporte:
        reportes.delete_one({"id_reporte": id_paciente1})
        print(f"El reporte con ID {id_paciente1} ha sido eliminado exitosamente.")
        break
    else:
        print(f"No se encontró un reporte con ID {id_paciente1}, por favor ingrese el ID de nuevo.")

