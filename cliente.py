from __future__ import annotations


class Cliente:
    def __init__(
        self,
        idcliente: str,
        apellidos: str,
        nombres: str,
        direccion: str,
        telefono: str
    ) -> None:
        self.idcliente: str = idcliente
        self.apellidos: str = apellidos
        self.nombres: str = nombres
        self.direccion: str = direccion
        self.telefono: str = telefono
        self.pedidos: list[Pedido] = []

    def agregar_pedido(self, pedido: Pedido) -> None:
        self.pedidos.append(pedido)

    def mostrar_pedidos(self) -> None:
        print(f"\nCliente: {self.apellidos}, {self.nombres}")
        print("Pedidos realizados:")

        if len(self.pedidos) == 0:
            print("No tiene pedidos registrados.")
        else:
            for pedido in self.pedidos:
                print(pedido)

    def __str__(self) -> str:
        return f"{self.idcliente} - {self.apellidos}, {self.nombres}"
