from controladores.cliente_controlador import ClienteControlador
from vistas.utilidades import mostrar_lista


class ClienteVista:
    @classmethod
    def mostrar_menu(cls) -> None:
        print("\n========== GESTIÓN DE CLIENTES ==========")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por ID")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("6. Ver pedidos de un cliente")
        print("7. Volver")

    @classmethod
    def ejecutar(cls) -> None:
        while True:
            cls.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                idcliente = input("ID cliente: ").strip()
                apellidos = input("Apellidos: ").strip()
                nombres = input("Nombres: ").strip()
                direccion = input("Dirección: ").strip()
                telefono = input("Teléfono: ").strip()

                if ClienteControlador.registrar(idcliente, apellidos, nombres, direccion, telefono):
                    print("Cliente registrado correctamente.")
                else:
                    print("No se pudo registrar el cliente.")

            elif opcion == "2":
                clientes = ClienteControlador.listar()
                mostrar_lista(clientes)

            elif opcion == "3":
                idcliente = input("ID cliente: ").strip()
                cliente = ClienteControlador.buscar(idcliente)

                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print(cliente)

            elif opcion == "4":
                idcliente = input("ID cliente a modificar: ").strip()
                cliente = ClienteControlador.buscar(idcliente)

                if cliente is None:
                    print("Cliente no encontrado.")
                else:
                    print("Cliente actual:", cliente)
                    apellidos = input("Nuevos apellidos: ").strip()
                    nombres = input("Nuevos nombres: ").strip()
                    direccion = input("Nueva dirección: ").strip()
                    telefono = input("Nuevo teléfono: ").strip()

                    if ClienteControlador.modificar(idcliente, apellidos, nombres, direccion, telefono):
                        print("Cliente modificado correctamente.")
                    else:
                        print("No se pudo modificar el cliente.")

            elif opcion == "5":
                idcliente = input("ID cliente a eliminar: ").strip()
                confirmacion = input("¿Está seguro? (s/n): ").lower()

                if confirmacion == "s":
                    if ClienteControlador.eliminar(idcliente):
                        print("Cliente eliminado correctamente.")
                    else:
                        print("No se pudo eliminar el cliente.")

            elif opcion == "6":
                idcliente = input("ID cliente: ").strip()
                pedidos = ClienteControlador.listar_pedidos_cliente(idcliente)
                mostrar_lista(pedidos)

            elif opcion == "7":
                break

            else:
                print("Opción inválida.")
