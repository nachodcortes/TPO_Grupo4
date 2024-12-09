# Programa para una agencia de venta de paquetes turisticos, el que lo usa es el empleado de la agencia

import time
import json

# Funcion de convertir numeros a palabras con recursion
def numero_a_palabras(numero):
    unidades = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
    especiales = ["diez", "once", "doce", "trece", "catorce", "quince", "dieciseis", "diecisiete", "dieciocho", "diecinueve"]
    decenas = ["", "", "", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    centenas = ["", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]
    
    if numero < 10:
        return unidades[numero]
    elif 10 <= numero < 20:
        return especiales[numero - 10]
    elif 20 <= numero < 30:
        if numero == 20:
            return "veinte"
        else:
            return "veinti" + unidades[numero % 10]
    elif 30 <= numero < 100:
        if numero % 10 == 0:
            return decenas[numero // 10]
        else:
            return decenas[numero // 10] + " y " + unidades[numero % 10]
    elif numero < 1000:
        if numero == 100:
            return "cien"
        if numero % 100 == 0:
            return centenas[numero // 100]
        else:
            return centenas[numero // 100] + " " + numero_a_palabras(numero % 100)
    elif numero < 1000000:
        if numero // 1000 == 1:
            miles = "mil"
        else:
            miles = numero_a_palabras(numero // 1000) + " mil"
        if numero % 1000 == 0:
            return miles
        else:
            return miles + " " + numero_a_palabras(numero % 1000)
        
# Funcion que valida que el numero sea positivo
def validar_numero_positivo(mensaje_entrada, mensaje_error):
    while True:
        try:
            valor = int(input(mensaje_entrada))
            assert 0 < valor < 10000 , mensaje_error
            break
        except AssertionError as mensaje:
            print("Error en los datos ingresados:", mensaje)
        except ValueError:
            print("Dato invalido, ingrese un numero")
    return valor

# Funcion de verificar si un año es bisiesto
def es_bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

# Función de validar la fecha
def validar_fecha(viaje_anio, viaje_mes, viaje_dia, anio_actual, mes_actual, dia_actual):
    try:
        assert 1 <= viaje_mes <= 12, "Mes no válido"
        assert 1 <= viaje_dia <= 31, "Día no válido"
        assert not (viaje_mes in [4, 6, 9, 11] and viaje_dia > 30), "Día no válido para el mes dado"
        assert not (viaje_mes == 2 and es_bisiesto(viaje_anio) and viaje_dia > 29), "Día no válido para febrero en un año bisiesto"
        assert not (viaje_mes == 2 and not es_bisiesto(viaje_anio) and viaje_dia > 28), "Día no válido para febrero en un año no bisiesto"
        assert not (
            viaje_anio < anio_actual or
            (viaje_anio == anio_actual and viaje_mes < mes_actual) or
            (viaje_anio == anio_actual and viaje_mes == mes_actual and viaje_dia < dia_actual)
            ), "Error: Ha ingresado una fecha anterior a la actual. Pruebe nuevamente."
        assert viaje_anio < MAX_FECHA, f"Fecha tiene que ser menor a {MAX_FECHA}."
        return False
    
    except AssertionError as mensaje:
        print(mensaje)
        print("Por favor, intente nuevamente.")
        return True

# Funcion para agregar paquetes al archivo paquetes
def agregar_paquete(archivo, destino, continente, dias, transporte, hotel, regimen_comidas, precio):
    try:
        archivo.write(f"{destino},{continente},{dias},{transporte},{hotel},{regimen_comidas},{precio}\n")
    except OSError as mensaje:
        print("Error del sistema al intentar acceder al archivo:", mensaje)
        
# Funcion generar numero de reserva
def generar_numero_reserva(nuevo_numero):
    nuevo_numero += 1
    return nuevo_numero
        
# Función para mostrar los paquetes (pueden ser todos o algunos dependiendo la busqueda)
def mostrar_paquetes(disponibles):
    num_paquete = 1
    if disponibles:
        print("")
        print("Paquetes disponibles: ")
        print("")
        print(f"{' ':<2} | {'Destino':<18} | {'Continente':<10} | {'Días':<4} | {'Aerolinea':<22} | {'Hotel':<32} | {'Régimen de Comidas':<18} | {'Precio':<7}") 
        print("-" * 134)
        for linea in disponibles:
            paquete = linea.strip().split(",")
            print(f"{num_paquete:>2} | {paquete[0]:<18} | {paquete[1]:<10} | {paquete[2]:<4} | {paquete[3]:<22} | {paquete[4]:<32} | {paquete[5]:<18} | {paquete[6]:>6}$")
            num_paquete += 1
    else:
        print("No se encontraron paquetes disponibles.")
        
# Funcion generar factura
def generar_factura(paquete, clientes, cantidad_personas, fecha_viaje, numero_reserva):
    print()
    print("-" * 90)
    print("Agencia de Viajes 'Destinos Splinter'".center(90))
    print()
    print("Numero de reserva: ", str(numero_reserva).zfill(8))
    print()

    print(f"Destino: {paquete[0]}".ljust(45, '.'), end="")
    print(f"Fecha del viaje: {str(fecha_viaje).capitalize()}".rjust(45, '.')) 

    print(f"Aerolinea: {paquete[3]}".ljust(45, '.'), end="")
    print(f"Dias: {paquete[2]}".rjust(45, '.'))

    print(f"Hotel: {paquete[4]}".ljust(45, '.'), end="")
    print(f"Regimen de comidas: {paquete[5]}".rjust(45, '.'))
    
    print(f"Cantidad de personas: {cantidad_personas}".ljust(45, '.'), end="")
    print(f"Precio por persona: {paquete[6]}$".rjust(45, '.'))
    
    total_a_pagar = int(paquete[6]) * cantidad_personas
    print(f"TOTAL A PAGAR: {total_a_pagar}$ ({str(numero_a_palabras(total_a_pagar)).capitalize()}$)".rjust(90, '.'))
    
    print()
    print("PASAJEROS: ")
    
    for i in range(len(clientes)):
        cliente = clientes[i]
        print(f"Pasajero {i+1}: {cliente['nombre']}, DNI: {cliente['dni']}")
    
    print("-" * 90)
        
def mostrar_reservas():
    arch = None
    try:
        arch = open("reservas.json", "r")
        print("RESERVAS ALMACENADAS:")
        print("-" * 90)
        for linea in arch:
            reserva = json.loads(linea.strip())  # Carga cada linea JSON al python
            print(f"Número de Reserva: {reserva['numero_reserva']}")
            print(f"Destino: {reserva['destino']}")
            print(f"Continente: {reserva['continente']}")
            print(f"Dias: {reserva['dias']}")
            print(f"Aerolinea: {reserva['aerolinea']}")
            print(f"Hotel: {reserva['hotel']}")
            print(f"Régimen de Comidas: {reserva['regimen_comida']}")
            print(f"Precio: {reserva['precio']}$")
            print(f"Fecha del Viaje: {reserva['fecha_viaje']}")
            print(f"Cantidad de Personas: {reserva['cantidad_personas']}")
            print("Clientes:")
            for cliente in reserva["clientes"]:
                print(f"  Nombre: {cliente['nombre']}, DNI: {cliente['dni']}")
            print("-" * 90)
    except FileNotFoundError:
        print("Error: El archivo no existe.")
    except json.JSONDecodeError:
        print("Error: El archivo contiene datos inválidos.")
    except OSError as error:
        print("Error al abrir el archivo:", error)
    finally:
        if arch:
            try:
                arch.close()
            except OSError as mensaje:
                print("Error al cerrar el archivo:", mensaje)
            except ValueError:
                pass

def agregar_paquete_reservado(paquete, clientes, cantidad_personas, fecha_viaje, nuevo_numero):
    nueva_reserva = {
        "destino": paquete[0],
        "continente": paquete[1],
        "dias": paquete[2],
        "aerolinea": paquete[3],
        "hotel": paquete[4],
        "regimen_comida": paquete[5],
        "precio": int(paquete[6]) * cantidad_personas,
        "fecha_viaje": fecha_viaje,
        "cantidad_personas": cantidad_personas,
        "numero_reserva": nuevo_numero,
        "clientes": clientes
    }

    # Agregar la nueva reserva como una linea JSON
    try:
        arch = open("reservas.json", "a")
        
        json.dump(nueva_reserva, arch)
        arch.write("\n")
    except OSError as error:
        print("Error al guardar la reserva:", error)
    finally:
        try:
            arch.close()
        except OSError as mensaje:
            print("Error al cerrar el archivo:", mensaje)
        except ValueError:
            pass
                
# -------------------------------------------------------------------------------------------------------------------------------
    
# PROGRAMA PRINCIPAL

# Meses para la fecha
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

# Obtener fecha actual para funciones de validar fecha
fecha_actual = time.localtime()
anio_actual, mes_actual, dia_actual = fecha_actual.tm_year, fecha_actual.tm_mon, fecha_actual.tm_mday

# Resultados maximos para la busqueda
MAX_RESULTADOS = 20

# Maxima fecha de reserva
MAX_FECHA = 2030

# Numero de reserva
numero_reserva = 0

# Diccionario de funciones de busqueda
criterios_busqueda = {
    "1": lambda paquete, destino: paquete[0].lower() == destino.lower(),
    "2": lambda paquete, continente: paquete[1].lower() == continente.lower(),
    "3": lambda paquete, dias: int(paquete[2]) == int(dias),
    "4": lambda paquete, regimen_comida: paquete[5].lower() == regimen_comida.lower(),
    "5": lambda paquete, precio: int(paquete[6]) <= int(precio)
}

mensajes_busqueda = {
    "1": "Ingrese el destino que desea buscar: ",
    "2": "Ingrese el continente que desea buscar: ",
    "3": "Ingrese la cantidad de dias que desea buscar: ",
    "4": "Ingrese el regimen de comidas que desea buscar (Desayuno, Media Pension, Todo Incluido): ",
    "5": "Ingrese el precio maximo que desea buscar: ",
}

print("--- Sistema de busqueda y reserva de paquetes turisticos ---")

while True:
    try:
        # Menú de opciones
        print("\n1. Agregar paquete")
        print("2. Busqueda y reserva de paquete")
        print("3. Mostrar todos los paquetes disponibles")
        print("4. Mostrar reservas")
        print("5. Salir")
        
        # Solicitar opción
        opcion = int(input("\nSeleccione una opcion: "))
        
        # Verificar que la opción esté en el rango válido
        assert 1 <= opcion <= 5
        
        print("") 

        if opcion == 1:
            try:
                arch = open("matriz_paquetes.csv", "at")
                
                while True:
                    while True:
                        destino = input("Ingrese el destino: ").title()
                        if destino.replace(" ", "").isalpha():
                            break
                        else:
                            print("Error: El destino no puede contener numeros ni caracteres especiales. Intente nuevamente.")
                    while True:
                        continente = input("Ingrese el continente: ").title()
                        opciones_continente = ["America", "Europa", "Asia", "Africa", "Oceania", "Antartida"]
                        try:
                            assert continente in opciones_continente, "Continente invalido. Opciones validas: America, Europa, Asia, Africa, Oceania, Antartida."
                            break
                        except AssertionError as mensaje:
                            print("Error en los datos ingresados:", mensaje)
                            
                    dias = validar_numero_positivo("Ingrese la cantidad de dias: ", "La cantidad de dias debe ser un numero positivo y menos de 10000.")
                    transporte = input("Ingrese la aerolinea: ").title()
                    hotel = input("Ingrese el nombre del hotel: ").title()

                    while True:
                        regimen_comida = input("Ingrese el regimen de comidas (Desayuno, Media Pension, Todo Incluido): ").title()
                        opciones_regimen = ["Desayuno", "Media Pension", "Todo Incluido"]
                        try:
                            assert regimen_comida in opciones_regimen, "Regimen de comidas invalido. Opciones validas: Desayuno, Media Pension, Todo Incluido."
                            break
                        except AssertionError as mensaje:
                            print("Error en los datos ingresados:", mensaje)

                    precio = validar_numero_positivo("Ingrese el precio: ", "El precio debe ser un numero positivo y menos de 10000.")

                    agregar_paquete(arch, destino, continente, dias, transporte, hotel, regimen_comida, precio)
                    print("Paquete agregado con exito.")

                    # Preguntar si desea seguir agregando paquetes
                    continuar = input("¿Desea agregar otro paquete? (si/no): ").lower()
                    if continuar != 'si':
                        break
                    
            except FileNotFoundError:
                print("Error: El archivo no se encontro.")
            except PermissionError:
                print("Error: No se encontraron permisos para escribir en el archivo.")
            except OSError as mensaje:
                print("Error del sistema al intentar acceder al archivo:", mensaje)
            
            finally:
                try:
                    arch.close()
                except OSError as mensaje:
                    print("Error al cerrar el archivo:", mensaje)
                except ValueError:
                    pass

        elif opcion == 2:
            
            try:
                arch = open("matriz_paquetes.csv", "rt")
            except FileNotFoundError:
                print("No se encontro el archivo de paquetes.")
            except OSError:
                print("Hubo un error al leer el archivo.")
            except ValueError:
                print("Error: entrada invalida.")
            
            else:
                cantidad_personas = int(input("¿Cuantas personas van a viajar? (Hasta 30 personas): "))

                # Validacion de cantidad de personas
                while not (0 < cantidad_personas <= 30):
                    print("Numero de personas no valido, ingrese de nuevo.")
                    cantidad_personas = int(input("¿Cuantas personas van a viajar?: "))
                
                resultados_totales = []
                realizar_reserva = False
                salir_filtros = False
                
                while not salir_filtros:
                    
                    # Menu de filtros
                    print("\nSeleccione el criterio de busqueda:")
                    print("1. Por destino")
                    print("2. Por continente")
                    print("3. Por dias")
                    print("4. Por regimen de comidas")
                    print("5. Por precio")
                    print("6. Seleccionar un paquete de los resultados")

                    criterio_opcion = input("Ingrese el numero de criterio de busqueda: ")
                  
                    if criterio_opcion in criterios_busqueda: 
                        
                        # Validacion para dia y precio
                        
                        if criterio_opcion in ["3", "5"]:  
                            parametro = validar_numero_positivo(mensajes_busqueda[criterio_opcion], "Debe ingresar un numero positivo.")
                        else:
                            parametro = input(mensajes_busqueda[criterio_opcion])
                        
                        arch.seek(0)
                        nuevos_resultados = []
                        
                        if resultados_totales:
                            for linea in resultados_totales:
                                paquete = linea.strip().split(",")
                                if criterios_busqueda[criterio_opcion](paquete, parametro):
                                    if len(nuevos_resultados) < MAX_RESULTADOS:  # Limitar a 20 resultados para no llenar memoria
                                        nuevos_resultados.append(linea)
                                    else:
                                        print("Se han encontrado demasiados resultados. Por favor, refine su busqueda.")
                                        nuevos_resultados = []
                                        break

                        else:
                            for linea in arch:
                                paquete = linea.strip().split(",")
                                if criterios_busqueda[criterio_opcion](paquete, parametro):
                                    if len(nuevos_resultados) < MAX_RESULTADOS:  # Limitar a 20 resultados para no llenar memoria
                                        nuevos_resultados.append(linea)
                                    else:
                                        print("Se han encontrado demasiados resultados. Por favor, refine su busqueda.")
                                        nuevos_resultados = []
                                        break
                        
                        resultados_totales = nuevos_resultados
                        
                        if resultados_totales:
                            mostrar_paquetes(resultados_totales)
                        else:
                            print("No se encontraron paquetes que coincidan con los criterios.")
                            
                    elif criterio_opcion == "6":
                        
                        if not resultados_totales:
                            print("No hay paquetes filtrados aun. Realice una busqueda primero.")
                            continue  # Vuelve a la seleccion de criterios de busqueda
                        
                        else:    
                            # Codigo para seleccionar un paquete de los resultados
                            try:
                                seleccion = int(input(f"Seleccione el paquete (1-{len(resultados_totales)}): "))
                                if 1 <= seleccion <= len(resultados_totales):
                                    paquete_seleccionado = resultados_totales[seleccion - 1]
                                    paquete_split = paquete_seleccionado.split(",")
                                    print(f"Has seleccionado el paquete: {paquete_split[0]} de {paquete_split[2]} dias")  # Muestra el nombre del destino
                                    realizar_reserva = True
                                    # Continuar con la reserva...
                                else:
                                    print("Opcion fuera de rango, intente nuevamente.")
                                    continue
                            except ValueError:
                                print("Opcion no valida, debe ingresar un numero.")
                                continue
                            
                    else:
                        print("Opcion no valida.")
                        continue
                        
                    #RESERVA
                    if len(resultados_totales) == 1:
                            paquete_seleccionado = resultados_totales[0]
                            realizar_reserva = True
                    
                    if realizar_reserva == True:
                        
                        print("\n---- Reserva de Paquete ----")
                        
                        while True:
                            reservar = input("¿Desea reservar este paquete? (si/no): ")
                
                            if reservar.lower() == "si":
                                bandera = True
                                while bandera:
                                    fecha_viaje = input("Ingrese la fecha del viaje (yyyy-mm-dd): ")
                                    try:
                                        # Verificacion de la fecha
                                        viaje_anio, viaje_mes, viaje_dia = map(int, fecha_viaje.split('-'))
                                        bandera = validar_fecha(viaje_anio, viaje_mes, viaje_dia, anio_actual, mes_actual, dia_actual)
                                    except ValueError:
                                        print("Fecha no válida. Intente de nuevo.")

                                fecha_viaje = f"{numero_a_palabras(viaje_dia)} de {MESES[viaje_mes - 1]} de {viaje_anio}"
                                clientes = []  # lista para almacenar los datos de los clientes

                                for i in range(cantidad_personas):
                                    print(f"Cliente {i+1}:")
                                    while True:
                                        nombre = input("Ingrese el nombre completo del cliente: ")
                                        if nombre.replace(" ", "").isalpha():
                                            break
                                        else:
                                            print("Error: El nombre no puede contener numeros ni caracteres especiales. Intente nuevamente.")
                                    while True:
                                        try:
                                            dni = int(input("Ingrese el DNI del cliente: "))
                                            break
                                        except ValueError:
                                            print("Error: El DNI no puede contener espacios, signos de puntuacion ni letras. Pruebe nuevamente:")
                                    
                                    cliente = {'nombre': nombre.title(), 'dni': dni}
                                    clientes.append(cliente)

                                # Generar número de reserva
                                numero_reserva = generar_numero_reserva(numero_reserva)
                                paquete_split = paquete_seleccionado.split(",")
                                
                                agregar_paquete_reservado(paquete_split, clientes, cantidad_personas, fecha_viaje, numero_reserva)

                                print("Paquete reservado con exito. Generando factura...")
                                generar_factura(paquete_split, clientes, cantidad_personas, fecha_viaje, numero_reserva)

                                salir_filtros = True
                                break
                                
                            elif reservar.lower() == "no":
                                print("No se realizó la reserva.")
                                salir_filtros = True
                                break
                            
                            else:
                                print("Respuesta no valida. Por favor, ingrese 'si' o 'no'.")

            finally:
                try:
                    arch.close()
                except OSError as mensaje:
                    print("Error al cerrar el archivo:", mensaje)
                except ValueError:
                    pass

        elif opcion == 3:
            try:
                arch = open("matriz_paquetes.csv", "rt")
                
                mostrar_paquetes(arch)
            
            except FileNotFoundError:
                print("Error: El archivo no se encontro.")
            except PermissionError:
                print("Error: No se encontraron permisos para escribir en el archivo.")
            except OSError as mensaje:
                print("Error del sistema al intentar acceder al archivo:", mensaje)
            
            finally:
                try:
                    arch.close()
                except OSError as mensaje:
                    print("Error al cerrar el archivo:", mensaje)
                except ValueError:
                    pass
        
        elif opcion == 4:
            mostrar_reservas()

        elif opcion == 5:
            print("Saliendo del sistema...")
            break
        
    except AssertionError:
        print("Opcion no valida. Por favor, ingrese un numero entre 1 y 5.")
    except ValueError:
        print("Dato invalido. Por favor, ingrese un numero entre 1 y 5.")
