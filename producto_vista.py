from controladores.producto_controlador import ProductoControlador
from vistas.utilidades import leer_float, leer_int, mostrar_lista


class ProductoVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========== GESTIÓN DE PRODUCTOS ==========")
        print("1. Registrar producto")
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Modificar producto")
        print("5. Eliminar producto")
        print("6. Listar productos por categoría")
        print("7. Listar productos con stock bajo")
        print("8. Volver")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idproducto = input("ID producto: ").strip()
                descripcion = input("Descripción: ").strip()
                precio = leer_float("Precio: ")
                stock = leer_int("Stock: ")
                idcategoria = input("ID categoría: ").strip()

                if ProductoControlador.registrar(idproducto, descripcion, precio, stock, idcategoria):
                    print("Producto registrado correctamente.")
                else:
                    print("No se pudo registrar el producto.")

            elif opcion == "2":
                productos = ProductoControlador.listar()
                mostrar_lista(productos)

            elif opcion == "3":
                idproducto = input("ID producto: ").strip()
                producto = ProductoControlador.buscar(idproducto)

                if producto is None:
                    print("Producto no encontrado.")
                else:
                    print(producto)

            elif opcion == "4":
                idproducto = input("ID producto a modificar: ").strip()
                producto = ProductoControlador.buscar(idproducto)

                if producto is None:
                    print("Producto no encontrado.")
                else:
                    print("Producto actual:", producto)
                    descripcion = input("Nueva descripción: ").strip()
                    precio = leer_float("Nuevo precio: ")
                    stock = leer_int("Nuevo stock: ")
                    idcategoria = input("Nueva ID categoría: ").strip()

                    if ProductoControlador.modificar(idproducto, descripcion, precio, stock, idcategoria):
                        print("Producto modificado correctamente.")
                    else:
                        print("No se pudo modificar el producto.")

            elif opcion == "5":
                idproducto = input("ID producto a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if ProductoControlador.eliminar(idproducto):
                        print("Producto eliminado correctamente.")
                    else:
                        print("No se pudo eliminar el producto.")

            elif opcion == "6":
                idcategoria = input("ID categoría: ").strip()
                productos = ProductoControlador.listar_por_categoria(idcategoria)
                mostrar_lista(productos)

            elif opcion == "7":
                stock_maximo = leer_int("Mostrar productos con stock menor o igual a: ")
                productos = ProductoControlador.listar_stock_bajo(stock_maximo)
                mostrar_lista(productos)

            elif opcion == "8":
                break

            else:
                print("Opción inválida.")
