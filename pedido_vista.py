from controladores.pedido_controlador import PedidoControlador
from vistas.utilidades import leer_int, mostrar_lista


class PedidoVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========== GESTIÓN DE PEDIDOS ==========")
        print("1. Registrar pedido")
        print("2. Listar pedidos")
        print("3. Buscar pedido por ID")
        print("4. Mostrar detalle de pedido")
        print("5. Eliminar pedido")
        print("6. Volver")

    @classmethod
    def registrar_pedido(cls) -> None:
        idpedido = input("ID pedido: ").strip()
        fecha = input("Fecha (YYYY-MM-DD): ").strip()
        idcliente = input("ID cliente: ").strip()

        pedido = PedidoControlador.crear_pedido(idpedido, fecha, idcliente)

        if pedido is None:
            return

        while True:
            idproducto = input("ID producto a agregar: ").strip()
            cantidad = leer_int("Cantidad: ")
            PedidoControlador.agregar_producto(pedido, idproducto, cantidad)

            continuar = input("¿Desea agregar otro producto? (s/n): ").lower()
            if continuar != "s":
                break

        print("\nResumen del pedido antes de registrar:")
        pedido.mostrar_pedido()

        confirmacion = input("¿Confirmar registro del pedido? (s/n): ").lower()
        if confirmacion == "s":
            if PedidoControlador.registrar_pedido(pedido):
                print("Pedido registrado correctamente.")
            else:
                print("No se pudo registrar el pedido.")
        else:
            print("Registro cancelado.")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                cls.registrar_pedido()

            elif opcion == "2":
                pedidos = PedidoControlador.listar()
                mostrar_lista(pedidos)

            elif opcion == "3":
                idpedido = input("ID pedido: ").strip()
                pedido = PedidoControlador.buscar(idpedido)

                if pedido is None:
                    print("Pedido no encontrado.")
                else:
                    print(pedido)

            elif opcion == "4":
                idpedido = input("ID pedido: ").strip()
                pedido = PedidoControlador.buscar(idpedido)

                if pedido is None:
                    print("Pedido no encontrado.")
                else:
                    pedido.mostrar_pedido()

            elif opcion == "5":
                idpedido = input("ID pedido a eliminar: ").strip()
                confirmacion = input("¿Está seguro? Se devolverá el stock. (s/n): ").lower()

                if confirmacion == "s":
                    if PedidoControlador.eliminar(idpedido):
                        print("Pedido eliminado correctamente.")
                    else:
                        print("No se pudo eliminar el pedido.")

            elif opcion == "6":
                break

            else:
                print("Opción inválida.")
