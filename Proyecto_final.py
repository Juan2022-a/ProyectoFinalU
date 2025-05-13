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
        
# Desde aqui comienza la parte de productos        
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

# Def para mostrar todos los productos    
def Mostrar_todos_los_productos():
    registros = Cargar_registros()  
    Mostrar_tabla(registros)