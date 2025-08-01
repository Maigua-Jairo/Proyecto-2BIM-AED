import os

# ========================
# ARCHIVOS NECESARIOS
# ========================
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("data/usuarios.txt"):
    with open("data/usuarios.txt", "w") as f:
        pass
if not os.path.exists("data/rutas.txt"):
    with open("data/rutas.txt", "w") as f:
        pass

# ========================
# VALIDACIÓN DE CONTRASEÑA
# ========================
def es_contrasena_segura(clave):
    tiene_mayuscula = any(c.isupper() for c in clave)
    tiene_minuscula = any(c.islower() for c in clave)
    tiene_numero = any(c.isdigit() for c in clave)
    return tiene_mayuscula and tiene_minuscula and tiene_numero and len(clave) >= 6

# ========================
# REGISTRO E INICIO DE SESIÓN
# ========================
def registrar_usuario():
    print("=== REGISTRO ===")
    nombre = input("Nombre completo: ")
    cedula = input("Cédula: ")
    edad = input("Edad: ")
    usuario = input("Correo (nombre.apellido@gmail.com): ")
    clave = input("Contraseña segura: ")

    if not es_contrasena_segura(clave):
        print("La contraseña debe tener una mayúscula, una minúscula, un número y mínimo 6 caracteres.\n")
        return

    with open("data/usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{clave},{nombre},{cedula},{edad}\n")

    print("Usuario registrado con éxito.\n")

def iniciar_sesion():
    print("=== INICIAR SESIÓN ===")
    usuario = input("Correo: ")
    clave = input("Contraseña: ")

    with open("data/usuarios.txt", "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if datos[0] == usuario and datos[1] == clave:
                print(f"Bienvenido, {datos[2]}!\n")
                return datos
    print("Correo o contraseña incorrectos.\n")
    return None

# ========================
# GESTIÓN DE RUTAS (ADMINISTRADOR)
# ========================
class Grafo:
    def __init__(self):
        self.grafo = {}

    def agregar_ruta(self, origen, destino, costo):
        if origen not in self.grafo:
            self.grafo[origen] = []
        self.grafo[origen].append((destino, costo))

def cargar_rutas():
    grafo = {}
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

# ========================
# ZONAS TURÍSTICAS Y DIJKSTRA
# ========================
grafo = {
    "Quito": ["Guayaquil", "Cuenca", "Baños", "Ambato", "Riobamba"],
    "Guayaquil": ["Quito", "Cuenca", "Machala", "Loja"],
    "Cuenca": ["Quito", "Guayaquil", "Azuay", "Loja"],
    "Baños": ["Quito", "Puyo"],
    "Ambato": ["Quito", "Baños", "Riobamba"],
    "Riobamba": ["Quito", "Ambato", "Guaranda"],
    "Machala": ["Guayaquil", "Loja"],
    "Loja": ["Guayaquil", "Cuenca", "Machala"],
    "Azuay": ["Cuenca"],
    "Puyo": ["Baños"]
}

costos = {
    "Quito": {"Guayaquil": 500, "Cuenca": 300, "Baños": 100, "Ambato": 150, "Riobamba": 200},
    "Guayaquil": {"Quito": 500, "Cuenca": 200, "Machala": 250, "Loja": 300},
    "Cuenca": {"Quito": 300, "Guayaquil": 200, "Azuay": 50, "Loja": 150},
    "Baños": {"Quito": 100, "Puyo": 80},
    "Ambato": {"Quito": 150, "Baños": 50, "Riobamba": 100},
    "Riobamba": {"Quito": 200, "Ambato": 100, "Guaranda": 120},
    "Machala": {"Guayaquil": 250, "Loja": 150},
    "Loja": {"Guayaquil": 300, "Cuenca": 150, "Machala": 150},
    "Azuay": {"Cuenca": 50},
    "Puyo": {"Baños": 80}
}

def dijkstra(ciudad_inicio, ciudad_fin):
    visitadas = []
    distancias = {ciudad: float('inf') for ciudad in grafo}
    anterior = {ciudad: None for ciudad in grafo}
    distancias[ciudad_inicio] = 0

    while len(visitadas) < len(grafo):
        ciudad_actual = None
        menor_dist = float('inf')
        for ciudad in grafo:
            if ciudad not in visitadas and distancias[ciudad] < menor_dist:
                menor_dist = distancias[ciudad]
                ciudad_actual = ciudad

        if ciudad_actual is None:
            break

        visitadas.append(ciudad_actual)

        for vecino in grafo[ciudad_actual]:
            if vecino in costos.get(ciudad_actual, {}) and vecino in distancias:
                nueva_dist = distancias[ciudad_actual] + costos[ciudad_actual][vecino]
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    anterior[vecino] = ciudad_actual

    ruta = []
    actual = ciudad_fin
    while actual is not None:
        ruta.insert(0, actual)
        actual = anterior[actual]

    if distancias[ciudad_fin] == float('inf'):
        return None, []
    else:
        return distancias[ciudad_fin], ruta

# ========================
# CLIENTE: SELECCIÓN DE RUTAS
# ========================
lugares_seleccionados = []

def mostrar_zonas():
    print("\n=== ZONAS DISPONIBLES ===")
    for ciudad in grafo:
        print(f"- {ciudad}")

def seleccionar_lugares():
    mostrar_zonas()
    while True:
        lugar = input("Selecciona un lugar turístico ('fin' para salir): ").strip()
        if lugar.lower() == "fin":
            break
        if lugar in lugares_seleccionados:
            print("Ya está seleccionado.")
        elif lugar in grafo:
            lugares_seleccionados.append(lugar)
            print(f"{lugar} agregado.")
        else:
            print("Lugar no encontrado.")

def mostrar_seleccion():
    if not lugares_seleccionados:
        print("No has seleccionado ningún lugar.")
    else:
        print("Lugares seleccionados:")
        for lugar in lugares_seleccionados:
            print(f"- {lugar}")

def calcular_ruta_total():
    if len(lugares_seleccionados) < 2:
        print("Selecciona al menos 2 lugares.")
        return

    total = 0
    ruta_completa = []

    for i in range(len(lugares_seleccionados) - 1):
        origen = lugares_seleccionados[i]
        destino = lugares_seleccionados[i + 1]
        costo, ruta = dijkstra(origen, destino)
        if not ruta:
            print(f"No hay ruta entre {origen} y {destino}.")
            return
        total += costo
        if ruta_completa:
            ruta_completa += ruta[1:]
        else:
            ruta_completa += ruta

    print("\nRuta seleccionada:")
    print(" -> ".join(ruta_completa))
    print(f"Costo total: {total}")

def guardar_seleccion(nombre_cliente="cliente"):
    if len(lugares_seleccionados) < 2:
        print("No hay suficientes lugares para guardar.")
        return

    total = 0
    ruta_completa = []
    for i in range(len(lugares_seleccionados) - 1):
        origen = lugares_seleccionados[i]
        destino = lugares_seleccionados[i + 1]
        costo, ruta = dijkstra(origen, destino)
        if not ruta:
            print(f"No se puede guardar. No hay ruta de {origen} a {destino}.")
            return
        total += costo
        if ruta_completa:
            ruta_completa += ruta[1:]
        else:
            ruta_completa += ruta

    with open(f"rutas-{nombre_cliente}.txt", "w") as archivo:
        archivo.write(f"Cliente: {nombre_cliente}\n")
        archivo.write("Lugares seleccionados: " + ", ".join(lugares_seleccionados) + "\n")
        archivo.write("Ruta completa: " + " -> ".join(ruta_completa) + "\n")
        archivo.write(f"Costo total: {total}\n")

    print(f"Ruta guardada como rutas-{nombre_cliente}.txt")

def menu_seleccion():
    while True:
        print("\n=== SELECCIÓN DE RUTAS ===")
        print("1. Ver zonas turísticas")
        print("2. Seleccionar lugares")
        print("3. Ver lugares seleccionados")
        print("4. Calcular ruta total")
        print("5. Guardar selección")
        print("6. Salir")
        opcion = input("Opción: ")
        if opcion == "1":
            mostrar_zonas()
        elif opcion == "2":
            seleccionar_lugares()
        elif opcion == "3":
            mostrar_seleccion()
        elif opcion == "4":
            calcular_ruta_total()
        elif opcion == "5":
            guardar_seleccion("cliente")
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

# ========================
# GESTIÓN DE GRAFO FIJO
# ========================
def mostrar_mapa():
    print("\n=== MAPA DE RUTAS ===")
    for origen in grafo:
        for destino in grafo[origen]:
            costo = costos.get(origen, {}).get(destino, "desconocido")
            print(f"{origen} -> {destino} (Costo: {costo})")

def consultar_ruta():
    inicio = input("Ciudad de inicio: ")
    fin = input("Ciudad destino: ")

    if inicio not in grafo or fin not in grafo:
        print("Una o ambas ciudades no existen.")
        return

    costo, ruta = dijkstra(inicio, fin)
    if ruta:
        print(f"\nRuta más económica: {' -> '.join(ruta)}")
        print(f"Costo total: {costo}")
    else:
        print("No hay ruta disponible.")

def menu_grafo():
    while True:
        print("\n====== GESTIÓN DE GRAFO Y RUTAS ======")
        print("1. Ver mapa de rutas")
        print("2. Consultar ruta óptima")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_mapa()
        elif opcion == "2":
            consultar_ruta()
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

# ========================
# MENÚ PRINCIPAL
# ========================
def main():
    while True:
        print("\n=== BIENVENIDO A POLITOUR ===")
        print("1. Registrarse")
        print("2. Iniciar sesión como Cliente")
        print("3. Iniciar sesión como Administrador")
        print("4. Gestión de Grafo y Rutas")
        print("5. Salir")
        op = input("Seleccione: ")

        if op == "1":
            registrar_usuario()
        elif op == "2":
            datos = iniciar_sesion()
            if datos:
                menu_cliente()
        elif op == "3":
            menu_administrador()
        elif op == "4":
            menu_grafo()
        elif op == "5":
            print("Gracias por usar POLITOUR.")
            break
        else:
            print("Opción inválida.")

# ========================
# EJECUCIÓN
# ========================
main()
