from codigo_trabajofinal import *
import mysql.connector
from pymongo import MongoClient

client= MongoClient('localhost', 27017)
db= client.Informatica1_PF

imagenesmedicas= db.imagenes
reportesmedicos= db.reportes
import bcrypt

# Función de inicio de sesión
def login():
    print(" Inicio de Sesión ")
    username = input(" Usuario: ").strip()
    password = input(" Contraseña: ").strip()

  
    conexion = mysql.connector.connect(
        user='informatica1',
        password='info20242',
        host='127.0.0.1',
        database='Informatica1_PF'
        )
    cursor = conexion.cursor()
    sql = "SELECT role FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    resultado = cursor.fetchone()

    if resultado:
        role = resultado[0]
        conexion.commit()
        print(f" Bienvenido {role} ")
        return role
    else:
        print("Usuario o contraseña incorrectos.")


import bcrypt


# Función principal
def main():
    while True:
        print("\nSistema de Gestión de Diagnósticos Asistidos por Imágenes Médicas")
        print("1. Iniciar sesión")
        print("2. Salir")
        opcion_principal = input("Seleccione una opción: ").strip()

        if opcion_principal == "1":
            role = login()  # Realiza el login y obtiene el rol del usuario
            if not role:
                print("No se pudo autenticar. Intente nuevamente.")
                continue

            # Menú según el rol
            while True:
                print("\nMenú principal:")
                if role == "Administrador":
                    print("1. Ingresar imagenes")
                    print("2. Ingresar reportes")
                    print("3. editar imagenes")
                    print("4. editar reportes")
                    print("5. ver imagenes")
                    print("6. ver reportes")
                    print("7. buscar imagenes")
                    print("8. buscar reportes")
                    print("9. eliminar imagen")
                    print("10. eliminar reportes")
                    print("11. mover una imagen")
                    print("12. añadir usuario")
                    print("13. eliminar usuario")
                    print("14. actualizar usuario")
                    print("15. mostrar usuario")
                    print("16. agregar paciente")
                    print("17. actualizar paciente")
                    print("18. mostrar paciente")
                    print("19. buscar paciente")
                    print("20. agregar diagnostico")
                    print("21. mostrar diagnostico")
                    print("22. buscar diagnostico")
                    print("23. actualizar diagnostico")
                    print("24. salir")
                elif role == "Médico":
                    print("1. añadir usuario")
                    print("2. eliminar usuario")
                    print("3. actualizar usuario")
                    print("4. mostrar usuario")
                    print("5. agregar paciente")
                    print("6. actualizar paciente")
                    print("7. mostrar paciente")
                    print("8. buscar paciente")
                    print("9. agregar diagnostico")
                    print("10. mostrar diagnostico")
                    print("11. buscar diagnostico")
                    print("12. actualizar diagnostico")
                    print("13. buscar reportes")
                    print("14. Ingresar reportes")
                    print("15. editar reportes")
                    print("16. ver reportes")
                    print("17. eliminar reportes")
                    print("18. salir")
                elif role == "Técnico":
                    print("1. Ingresar imágenes médicas")
                    print("2. editar imagenes medica")
                    print("3. ver imagenes")
                    print("4. buscar imagenes")
                    print("5. eliminar imagenes")
                    print("6. mover una imagen")
                    print("7. salir")
                else:
                    print("Rol no reconocido. Contacte al administrador.")
                    break

                opcion_rol = input("Seleccione una opción: ").strip()

                if role == "Administrador":
                    if opcion_rol == "1":
                        print("Ingresar imagenes")
                        ingresar_imagenes(db)
                    elif opcion_rol == "2":
                        print("Ingresar reportes")
                        ingresar_reportes_medicos(db)
                    elif opcion_rol == "3":
                        print("editar imagenes")
                        editar_imagenes(db)
                    elif opcion_rol == "4":
                        print("editar reportes")
                        editar_reportes(db)
                    elif opcion_rol == "5":
                        print("ver imagenes")
                        ver_imagenes(db)
                    elif opcion_rol == "6":
                        print("ver reportes")
                        ver_reportes(db)
                    elif opcion_rol == "7":
                        print("buscar imagenes")
                        buscar_imagen_por_id(db)
                    elif opcion_rol == "8":
                        print("buscar reportes")
                        buscar_reportes(db)
                    elif opcion_rol == "9":
                        print("eliminar imagen ")
                        eliminar_imagen(db)
                    elif opcion_rol == "10":
                        print("eliminar reporte")
                        eliminar_reporte(db)
                    elif opcion_rol == "11":
                        print("mover una imagen")
                        mover_una_imagen(db)
                    elif opcion_rol == "12":
                        print("añadir usuario")
                        añadir_usuario()
                    elif opcion_rol == "13":
                        print("eliminar usuario")
                        eliminar_usuario()
                    elif opcion_rol == "14":
                        print("Actualizar usuario")
                        actualizar_usuario()
                    elif opcion_rol == "15":
                        print("Mostrar usuario")
                        mostrar_usuarios()
                    elif opcion_rol == "16":
                        print("Agregar paciente")
                        agregar_paciente()
                    elif opcion_rol == "17":
                        print("Actualizar paciente")
                        actualizar_paciente()
                    elif opcion_rol == "18":
                        print("Mostar paciente")
                        mostrar_pacientes()
                    elif opcion_rol == "19":
                        print("Buscar paciente")
                        buscar_paciente()
                    elif opcion_rol=="20":
                        print("Agregar diagnostico")
                        agregar_diagnostico()
                    elif opcion_rol == "21":
                        print("mostrar Diagnóstico")
                        mostrar_diagnosticos()
                    elif opcion_rol == "22":
                        print("Buscar diagnositico")
                        buscar_diagnostico()
                    elif opcion_rol == "23":
                        print("Actualizar diagnostico")
                        actualizar_diagnostico()
                    elif opcion_rol == "24":
                        print("Cerrando sesión...")
                        break
                    else:
                        print("Opción inválida. Intente de nuevo.")
                elif role == "Médico":
                    if opcion_rol == "1":
                        print("añadir usuario")
                        añadir_usuario()
                    elif opcion_rol == "2":
                        print("eliminar usuario")
                        eliminar_usuario()
                    elif opcion_rol == "3":
                        print("Actualizar usuario")
                        actualizar_usuario
                    elif opcion_rol == "4":
                        print("Mostrar usuario")
                        mostrar_usuarios()
                    elif opcion_rol == "5":
                        print("Agregar paciente")
                        agregar_paciente()
                    elif opcion_rol == "6":
                        print("Actualizar paciente")
                        actualizar_paciente()
                    elif opcion_rol == "7":
                        print("Mostar paciente")
                        mostrar_pacientes()
                    elif opcion_rol == "8":
                        print("Buscar paciente")
                        buscar_paciente()
                    elif opcion_rol=="9":
                        print("Agregar diagnostico")
                        agregar_diagnostico()
                    elif opcion_rol == "10":
                        print("mostrar Diagnóstico")
                        mostrar_diagnosticos()
                    elif opcion_rol == "11":
                        print("Buscar diagnositico")
                        buscar_diagnostico()
                    elif opcion_rol == "12":
                        print("Actualizar diagnostico")
                        actualizar_diagnostico()
                    elif opcion_rol == "13":
                        print("buscar reportes")
                        buscar_reportes(db)
                    elif opcion_rol == "14":
                        print("Ingresar reportes")
                        ingresar_reportes_medicos(db)
                    elif opcion_rol == "15":
                        print("editar reportes")
                    elif opcion_rol == "16":
                        print("ver reportes")
                        ver_reportes(db)
                    elif opcion_rol == "17":
                        print("eliminar reporte")
                        eliminar_reporte(db)
                    elif opcion_rol == "18":
                        print("Cerrando sesión...")
                        break
                    else:
                        print("Opción inválida. Intente de nuevo.")
                elif role == "Técnico":
                    if opcion_rol == "1":
                        print("Ingresar imagenes")
                        ingresar_imagenes(db)
                    elif opcion_rol == "2":
                        print("editar imagenes")
                    elif opcion_rol == "3":
                        print("ver imagenes")
                        ver_imagenes(db)
                    elif opcion_rol == "4":
                        print("buscar imagenes")
                    elif opcion_rol == "5":
                        print("eliminar imagen ")
                        eliminar_imagen(db)
                    elif opcion_rol == "6":
                        print("mover una imagen")
                    elif opcion_rol == "7":
                        print("saliendo del sistema...")
        elif opcion_principal == "2":
            print("Saliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
