#Proyecto ----> Rutas Turisticas

#Menú general e Integracion
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
            guardar_rutas(grafo.grafo, "rutas.txt")
            print("Cambios guardados.")

        elif opcion == "7":
            break
            
# MENÚ PRINCIPAL

def main():
    print("Bienvenido al POLITOUR ")
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
