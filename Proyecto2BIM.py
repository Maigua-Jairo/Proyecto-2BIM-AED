# Proyecto ----> Rutas Turísticas
import os

# VALIDACIÓN DE CONTRASEÑA

def es_contrasena_segura(clave):
    tiene_mayuscula = any(c.isupper() for c in clave)
    tiene_minuscula = any(c.islower() for c in clave)
    tiene_numero = any(c.isdigit() for c in clave)
    return tiene_mayuscula and tiene_minuscula and tiene_numero and len(clave) >= 6

# REGISTRO DE USUARIO

def registrar_usuario():
    print("=== REGISTRO ===")
    nombre = input("Nombre completo: ")
    cedula = input("Cédula: ")
    edad = input("Edad: ")
    usuario = input("Correo (nombre.apellido@gmail.com): ")
    clave = input("Contraseña segura: ")

    if not es_contrasena_segura(clave):
        print("❌ La contraseña debe tener una mayúscula, una minúscula, un número y mínimo 6 caracteres.\n")
        return

    if not os.path.exists("data"):
        os.makedirs("data")

    with open("data/usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{clave},{nombre},{cedula},{edad}\n")

    print("✅ Usuario registrado con éxito.\n")

# INICIO DE SESIÓN

def iniciar_sesion():
    print("=== INICIAR SESIÓN ===")
    usuario = input("Correo: ")
    clave = input("Contraseña: ")

    if not os.path.exists("data/usuarios.txt"):
        print("⚠️ No hay usuarios registrados aún.\n")
        return None

    with open("data/usuarios.txt", "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if datos[0] == usuario and datos[1] == clave:
                print(f"✅ Bienvenido, {datos[2]}!\n")
                return datos  # Retorna los datos del usuario

    print("❌ Correo o contraseña incorrectos.\n")
    return None

# MENÚ CLIENTE (SIMPLIFICADO PARA COMPLETAR EJECUCIÓN)
def menu_cliente():
    print("Menú del cliente en desarrollo...\n")

# FUNCIONES DE GRAFO (SIMPLIFICADAS AQUÍ)
class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_ruta(self, origen, destino, costo):
        if origen not in self.grafo:
            self.grafo[origen] = []
        self.grafo[origen].append((destino, costo))

def cargar_rutas():
    grafo = {}
    if os.path.exists("data/rutas.txt"):
        with open("data/rutas.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) == 3:
                    origen, destino, costo = partes
                    costo = int(costo)
                    if origen not in grafo:
                        grafo[origen] = []
                    grafo[origen].append((destino, costo))
    return grafo

def guardar_rutas(grafo, ruta):
    with open(ruta, "w") as archivo:
        for origen in grafo:
            for destino, costo in grafo[origen]:
                archivo.write(f"{origen},{destino},{costo}\n")

# MENÚ GENERAL E INTEGRACIÓN
def burbuja(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def busqueda_lineal(lista, elemento):
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    return -1

def menu_administrador():
    grafo = Grafo()
    grafo.grafo = cargar_rutas()

    while True:
        print("\n#### MENÚ ADMINISTRADOR #####")
        print("1. Agregar una ruta")
        print("2. Mostrar rutas")
        print("3. Consultar ciudad")
        print("4. Actualizar ciudad")
        print("5. Eliminar ciudad")
        print("6. Guardar cambios")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            origen = input("Ciudad origen: ")
            destino = input("Ciudad destino: ")
            costo = int(input("Costo: "))
            grafo.agregar_ruta(origen, destino, costo)
            print("Ruta agregada.")

        elif opcion == "2":
            print("\n--- Rutas actuales ---")
            ciudades = list(grafo.grafo.keys())
            ordenadas = burbuja(ciudades.copy())
            for ciudad in ordenadas:
                print(f"Desde {ciudad}:")
                for destino, costo in grafo.grafo[ciudad]:
                    print(f"  -> {destino} | Costo: {costo}")

        elif opcion == "3":
            ciudad = input("Nombre de la ciudad a consultar: ")
            ciudades = list(grafo.grafo.keys())
            pos = busqueda_lineal(ciudades, ciudad)
            if pos != -1:
                print(f"{ciudad} tiene rutas a:")
                for destino, costo in grafo.grafo[ciudad]:
                    print(f"  -> {destino} | Costo: {costo}")
            else:
                print("Ciudad no encontrada.")

        elif opcion == "4":
            ciudad = input("Ciudad origen a actualizar: ")
            if ciudad in grafo.grafo:
                nuevo_destino = input("Nuevo destino: ")
                nuevo_costo = int(input("Nuevo costo: "))
                grafo.grafo[ciudad] = [(nuevo_destino, nuevo_costo)]
                print("Ruta actualizada.")
            else:
                print("Ciudad no encontrada.")

        elif opcion == "5":
            ciudad = input("Ciudad origen a eliminar: ")
            if ciudad in grafo.grafo:
                del grafo.grafo[ciudad]
                print("Ciudad eliminada.")
            else:
                print("Ciudad no encontrada.")

        elif opcion == "6":
            guardar_rutas(grafo.grafo, "data/rutas.txt")
            print("Cambios guardados.")

        elif opcion == "7":
            break

# MENÚ PRINCIPAL
def main():
    print("Bienvenido al POLITOUR")
    print("1. Registrarse\n2. Iniciar sesión como Cliente\n3. Iniciar sesión como Administrador")
    op = input("Seleccione: ")

    if op == "1":
        registrar_usuario()
    elif op == "2":
        if iniciar_sesion():
            menu_cliente()
    elif op == "3":
        menu_administrador()

main()
