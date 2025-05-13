import json
import os
from tabulate import tabulate

ARCHIVO_DATOS = "Base_productos.txt"

# Carga la base de datos desde el archivo
def Cargar_registros():
    if os.path.isfile(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as file:
            return json.load(file)
    return []

# Guarda los datos en el archivo
def Guardar_registros(lista):
    with open(ARCHIVO_DATOS, "w") as file:
        json.dump(lista, file, indent=4)
        
# Desde aqui comienza la parte de productos ---------------------------------------------------------------------------------
# Def para crear los productos
def Crear_producto(nombre, precio, cantidad, codigo_producto):
    registros = Cargar_registros()
    nuevo_id = registros[-1]["id"] + 1 if registros else 1
    registros.append({
        "id": nuevo_id,
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
        "codigo_producto": codigo_producto
    })
    Guardar_registros(registros)
    print("👌 Nuevo registro agregado. 👌") 
    
# Def para editar los productos por id y codigo de producto
def Editar_producto(id_producto=None, codigo_producto=None, nombre=None, precio=None, cantidad=None):
    registros = Cargar_registros()
    for producto in registros:
        # Verifica si coincide el ID o el código del producto
        if (id_producto is not None and producto["id"] == id_producto) or \
           (codigo_producto is not None and producto["codigo_producto"] == codigo_producto):
            # Actualiza los valores solo si se proporcionan
            if nombre is not None:
                producto["nombre"] = nombre
            if precio is not None:
                producto["precio"] = precio
            if cantidad is not None:
                producto["cantidad"] = cantidad
            if codigo_producto is not None:
                producto["codigo_producto"] = codigo_producto
            Guardar_registros(registros)
            print("👌 Registro editado correctamente. 👌")
            return
    print("⚠️ Producto no encontrado. ⚠️")    
    
# Def para eliminar productos por id o codigo de producto
def Eliminar_producto(id_producto=None, codigo_producto=None):
    registros = Cargar_registros()
    for producto in registros:
        if (id_producto is not None and producto["id"] == id_producto) or \
           (codigo_producto is not None and producto["codigo_producto"] == codigo_producto):
            registros.remove(producto)
            Guardar_registros(registros)
            print("👌 Producto eliminado correctamente. 👌")
            return
    print("⚠️ Producto no encontrado. ⚠️")
    
# Def para buscar productos por id o codigo de producto
def Buscar_producto_id_codigo(id_producto=None, codigo_producto=None):
    registros = Cargar_registros()  
    for producto in registros:
        if (id_producto is not None and producto["id"] == id_producto) or \
           (codigo_producto is not None and producto["codigo_producto"] == codigo_producto):
            print("👌 Producto encontrado. 👌")
            return producto
    print("⚠️ Producto no encontrado. ⚠️")
    return None    

# Def para buscar productos por nombre
def Buscar_producto_por_nombre(nombre):
    registros = Cargar_registros()
    encontrados = [p for p in registros if p["nombre"].lower() == nombre.lower()]
    if encontrados:
        print("👌 Producto encontrado. 👌")
        return encontrados
    else:
        print("⚠️ No se encontró ningún producto con ese nombre. ⚠️")
        return None

# Def para mostrar los productos en forma de tabla
def Mostrar_tabla(lista):
    if not lista:
        print("⚠️ No existen registros para mostrar. ⚠️")
        return
    datos_tabla = []
    encabezados = ["ID", "Nombre", "Precio", "Cantidad", "Codigo_producto"]
    for producto in lista:
        datos_tabla.append([
            producto["id"],
            producto["nombre"],
            producto["precio"],
            producto["cantidad"],
            producto["codigo_producto"]
        ])
    print(tabulate(datos_tabla, headers=encabezados, tablefmt="fancy_grid"))

# Def para mostrar TODOS los productos    
def Mostrar_todos_los_productos():
    registros = Cargar_registros()  
    Mostrar_tabla(registros)
    
# Eliminar todos los registros
def Eliminar_todo():
    if os.path.isfile(ARCHIVO_DATOS):
        confirmacion = input("Escribe 'BorrarTodo' tal cual para confirmar o 'Cancelar': ").strip()
        if confirmacion == "BorrarTodo":
            Guardar_registros([])  # Elimina todos los registros
            print("⚠️ Todos los registros han sido eliminados.")
        elif confirmacion == "Cancelar":
            print("🚫 Operación cancelada.")
        else:
            print("🔴 Opción no válida. No se realizó ninguna acción.")
    else:
        print("⚠️ No se encontró el archivo de datos para eliminar.") # en caso de que no exista el archivo de datos
        
# Comienza la selección del menú -------------------------------------------------------------------------------------------     
# Menú
def menu():
    while True:
        print("\n🛒 Menú de Productos 🛒")
        print("1. Crear producto")
        print("2. Editar producto por id o código de producto")
        print("3. Eliminar producto por id o código de producto")
        print("4. Buscar producto por por id o código de producto")
        print("5. Buscar producto por Nombre")
        print("6. Mostrar TODOS los productos")
        print("7. Eliminar TODOS los Registros")
        print("8. Salir")

        opcion = input("Selecciona una opción: ")
        
        # Primera opción para crear un producto
        if opcion == "1":
            # Validación para el nombre
            while True:
                nombre = input("Nombre del producto (o escribe 'cancelar' o '0' para regresar al menú): ").strip()
                if nombre.lower() == "cancelar" or nombre == "0":
                    print("🚫 Operación cancelada. Regresando al menú...")
                    continue  # Regresa al menú
                if len(nombre) < 3 or len(nombre) > 50:
                    print("⚠️ El nombre debe tener entre 3 y 50 caracteres.")
                elif not nombre.replace(" ", "").isalpha():
                    print("⚠️ El nombre solo puede contener letras y espacios.")
                elif any(p["nombre"].lower() == nombre.lower() for p in Cargar_registros()):
                    print("⚠️ Ya existe un producto con este nombre.")
                else:
                    break
            
            # Validación para el precio
            while True:
                try:
                    precio = input("Precio del producto (o escribe 'cancelar' o '0' para regresar al menú): ")
                    if precio.lower() == "cancelar" or precio == "0":
                        print("🚫 Operación cancelada. Regresando al menú...")
                        continue  # Regresa al menú
                    precio = float(precio)
                    if precio <= 0 or precio > 1000.00:
                        print("⚠️ El precio debe ser mayor a 0 y no exceder $1000.")
                    elif round(precio, 2) != precio:
                        print("⚠️ El precio no puede tener más de 2 decimales.")
                    else:
                        break
                except ValueError:
                    print("⚠️ Debes ingresar un número válido para el precio.")
            
            # Validación para la cantidad
            while True:
                try:
                    cantidad = input("Cantidad del producto (o escribe 'cancelar' o '0' para regresar al menú): ")
                    if cantidad.lower() == "cancelar" or cantidad == "0":
                        print("🚫 Operación cancelada. Regresando al menú...")
                        continue  # Regresa al menú
                    cantidad = int(cantidad)
                    if cantidad < 0 or cantidad > 1000:
                        print("⚠️ La cantidad debe ser un número entero entre 0 y 1000.")
                    else:
                        break
                except ValueError:
                    print("⚠️ Debes ingresar un número entero válido para la cantidad.")
            
            # Validación para el código
            while True:
                codigo_producto = input("Código del producto (o escribe 'cancelar' o '0' para regresar al menú): ").strip().upper()
                if codigo_producto.lower() == "cancelar" or codigo_producto == "0":
                    print("🚫 Operación cancelada. Regresando al menú...")
                    continue  # Regresa al menú
                if len(codigo_producto) < 4 or len(codigo_producto) > 20:
                    print("⚠️ El código debe tener entre 4 y 20 caracteres.")
                elif not codigo_producto.replace("-", "").isalnum():
                    print("⚠️ El código solo puede contener caracteres alfanuméricos y guiones.")
                elif any(p["codigo_producto"] == codigo_producto for p in Cargar_registros()):
                    print("⚠️ Ya existe un producto con este código.")
                else:
                    break
            
            Crear_producto(nombre, precio, cantidad, codigo_producto)
        
        # Segunda opción para editar un producto
        elif opcion == "2":
            identificador = input("Escriba el ID o el código del producto que desea editar (o escribe 'cancelar' o '0' para regresar al menú): ").strip()
            if identificador.lower() == "cancelar" or identificador == "0":
                print("🚫 Operación cancelada. Regresando al menú...")
                continue  # Regresa al menú
            
            # Determinar si es un ID o un código
            id_producto = None
            codigo_producto = None
            if identificador.isdigit():
                id_producto = int(identificador)
            else:
                codigo_producto = identificador.upper()
            
            # Buscar el producto
            producto = Buscar_producto_id_codigo(id_producto, codigo_producto)
            if not producto:
                print("⚠️ Producto no encontrado. ⚠️")
                continue
            
            print(f"Producto encontrado: {producto}")
            
            # Validación para el nuevo nombre
            while True:
                nombre = input("Nuevo nombre del producto (dejar en blanco si no se desea editar, o escribe 'cancelar' o '0' para regresar al menú): ").strip()
                if nombre.lower() == "cancelar" or nombre == "0":
                    print("🚫 Operación cancelada. Regresando al menú...")
                    continue  # Regresa al menú
                if not nombre:
                    nombre = None
                    break
                elif len(nombre) < 3 or len(nombre) > 50:
                    print("⚠️ El nombre debe tener entre 3 y 50 caracteres.")
                elif not nombre.replace(" ", "").isalpha():
                    print("⚠️ El nombre solo puede contener letras y espacios.")
                elif any(p["nombre"].lower() == nombre.lower() for p in Cargar_registros() if p["id"] != producto["id"]):
                    print("⚠️ Ya existe un producto con este nombre.")
                else:
                    break
            
            # Validación para el nuevo precio
            while True:
                try:
                    precio = input("Nuevo precio del producto (dejar en blanco si no se desea editar, o escribe 'cancelar' o '0' para regresar al menú): ")
                    if precio.lower() == "cancelar" or precio == "0":
                        print("🚫 Operación cancelada. Regresando al menú...")
                        continue  # Regresa al menú
                    if not precio:
                        precio = None
                        break
                    precio = float(precio)
                    if precio <= 0 or precio > 1000.00:
                        print("⚠️ El precio debe ser mayor a 0 y no exceder $1000.")
                    elif round(precio, 2) != precio:
                        print("⚠️ El precio no puede tener más de 2 decimales.")
                    else:
                        break
                except ValueError:
                    print("⚠️ Debes ingresar un número válido para el precio.")
            
            # Validación para la nueva cantidad
            while True:
                try:
                    cantidad = input("Nueva cantidad del producto (dejar en blanco si no se desea editar, o escribe 'cancelar' o '0' para regresar al menú): ")
                    if cantidad.lower() == "cancelar" or cantidad == "0":
                        print("🚫 Operación cancelada. Regresando al menú...")
                        continue  # Regresa al menú
                    if not cantidad:
                        cantidad = None
                        break
                    cantidad = int(cantidad)
                    if cantidad < 0 or cantidad > 1000:
                        print("⚠️ La cantidad debe ser un número entero entre 0 y 1000.")
                    else:
                        break
                except ValueError:
                    print("⚠️ Debes ingresar un número entero válido para la cantidad.")
            
            # Validación para el nuevo código
            while True:
                nuevo_codigo = input("Nuevo código del producto (dejar en blanco si no se desea editar, o escribe 'cancelar' o '0' para regresar al menú): ").strip().upper()
                if nuevo_codigo.lower() == "cancelar" or nuevo_codigo == "0":
                    print("🚫 Operación cancelada. Regresando al menú...")
                    continue  # Regresa al menú
                if not nuevo_codigo:
                    nuevo_codigo = None
                    break
                elif len(nuevo_codigo) < 4 or len(nuevo_codigo) > 20:
                    print("⚠️ El código debe tener entre 4 y 20 caracteres.")
                elif not nuevo_codigo.replace("-", "").isalnum():
                    print("⚠️ El código solo puede contener caracteres alfanuméricos y guiones.")
                elif any(p["codigo_producto"] == nuevo_codigo for p in Cargar_registros() if p["id"] != producto["id"]):
                    print("⚠️ Ya existe un producto con este código.")
                else:
                    break
            
            # Editar el producto
            Editar_producto(id_producto, codigo_producto, nombre, precio, cantidad)
        
        # Tercera opción para eliminar un producto
        elif opcion == "3":
            identificador = input("Escriba el ID o el código del producto que desea eliminar (o escribe 'cancelar' o '0' para regresar al menú): ").strip()
            if identificador.lower() == "cancelar" or identificador == "0":
                print("🚫 Operación cancelada. Regresando al menú...")
                return
            
            id_producto = None
            codigo_producto = None
            if identificador.isdigit():
                id_producto = int(identificador)
            else:
                codigo_producto = identificador.upper()
            
            Eliminar_producto(id_producto, codigo_producto)
        
        # Cuarta opción para buscar un producto --------------------------------------------------------------------------------------------            
        elif opcion == "4":
            id_producto = int(input("ID del producto a buscar (dejar en blanco si no se desea buscar): ") or 0)
            codigo_producto = input("Código del producto a buscar (dejar en blanco si no se desea buscar): ") or None
            Buscar_producto_id_codigo(id_producto, codigo_producto)

# Quinta opción para buscar un producto por nombre ---------------------------------------------------------------------------------            
        elif opcion == "5":
            nombre = input("Nombre del producto a buscar: ")
            Buscar_producto_por_nombre(nombre)

# Sexta opción para mostrar todos los productos -----------------------------------------------------------------------------------            
        elif opcion == "6":
            Mostrar_todos_los_productos()

# Séptima opción para eliminar todos los registros ---------------------------------------------------------------------------------            
        elif opcion == "7":
            Eliminar_todo()

# Octava opción para salir del programa ---------------------------------------------------------------------------------------------            
        elif opcion == "8":
            print("👋 ¡Hasta luego! 👋")
            break
            
        else:
            print("🔴 Opción no válida. Por favor, selecciona una opción del 1 al 8.")
            
if __name__ == "__main__":
    menu()
