from vistas.categoria_vista import CategoriaVista
from vistas.cliente_vista import ClienteVista
from vistas.pedido_vista import PedidoVista
from vistas.producto_vista import ProductoVista


class MenuPrincipal:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========================================")
        print("        SISTEMA ACME S.A.")
        print("        Python + MySQL + POO + DAO + MVC")
        print("========================================")
        print("1. Gestión de clientes")
        print("2. Gestión de categorías")
        print("3. Gestión de productos")
        print("4. Gestión de pedidos")
        print("5. Salir")
        print("========================================")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                ClienteVista.ejecutar()
            elif opcion == "2":
                CategoriaVista.ejecutar()
            elif opcion == "3":
                ProductoVista.ejecutar()
            elif opcion == "4":
                PedidoVista.ejecutar()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida.")
