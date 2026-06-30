from controladores.categoria_controlador import CategoriaControlador
from vistas.utilidades import mostrar_lista


class CategoriaVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========== GESTIÓN DE CATEGORÍAS ==========")
        print("1. Registrar categoría")
        print("2. Listar categorías")
        print("3. Buscar categoría por ID")
        print("4. Modificar categoría")
        print("5. Eliminar categoría")
        print("6. Ver productos de una categoría")
        print("7. Volver")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idcategoria = input("ID categoría: ").strip()
                descripcion = input("Descripción: ").strip()

                if CategoriaControlador.registrar(idcategoria, descripcion):
                    print("Categoría registrada correctamente.")
                else:
                    print("No se pudo registrar la categoría.")

            elif opcion == "2":
                categorias = CategoriaControlador.listar()
                mostrar_lista(categorias)

            elif opcion == "3":
                idcategoria = input("ID categoría: ").strip()
                categoria = CategoriaControlador.buscar(idcategoria)

                if categoria is None:
                    print("Categoría no encontrada.")
                else:
                    print(categoria)

            elif opcion == "4":
                idcategoria = input("ID categoría a modificar: ").strip()
                categoria = CategoriaControlador.buscar(idcategoria)

                if categoria is None:
                    print("Categoría no encontrada.")
                else:
                    print("Categoría actual:", categoria)
                    descripcion = input("Nueva descripción: ").strip()

                    if CategoriaControlador.modificar(idcategoria, descripcion):
                        print("Categoría modificada correctamente.")
                    else:
                        print("No se pudo modificar la categoría.")

            elif opcion == "5":
                idcategoria = input("ID categoría a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if CategoriaControlador.eliminar(idcategoria):
                        print("Categoría eliminada correctamente.")
                    else:
                        print("No se pudo eliminar la categoría.")

            elif opcion == "6":
                idcategoria = input("ID categoría: ").strip()
                productos = CategoriaControlador.listar_productos(idcategoria)
                mostrar_lista(productos)

            elif opcion == "7":
                break

            else:
                print("Opción inválida.")
