# ========================
# GRAFO DE RUTAS Y COSTOS
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

# ========================
# ALGORITMO DIJKSTRA
# ========================

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
# MOSTRAR MAPA DE RUTAS
# ========================

def mostrar_mapa():
    print("\n=== MAPA DE RUTAS ===")
    for origen in grafo:
        for destino in grafo[origen]:
            costo = costos.get(origen, {}).get(destino, "desconocido")
            print(f"{origen} -> {destino} (Costo: {costo})")

# ========================
# CONSULTAR RUTA
# ========================

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

# ========================
# MENÚ
# ========================

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

# Ejecutar
menu_grafo()