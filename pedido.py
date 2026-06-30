from __future__ import annotations

from modelos.cliente import Cliente
from modelos.detalledepedido import DetallePedido
from modelos.producto import Producto


class Pedido:
    def __init__(
        self,
        idpedido: str,
        fecha: str,
        cliente: Cliente
    ) -> None:
        self.idpedido: str = idpedido
        self.fecha: str = fecha
        self.cliente: Cliente = cliente
        self.detalles: list[DetallePedido] = []

        cliente.agregar_pedido(self)

    def agregar_producto(
        self,
        producto: Producto,
        cantidad: int
    ) -> None:
        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")

        elif producto.reducir_stock(cantidad):
            detalle: DetallePedido = DetallePedido(producto, cantidad)
            self.detalles.append(detalle)
            print("Producto agregado correctamente al pedido.")

        else:
            print("Stock insuficiente para el producto:", producto.descripcion)

    def calcular_total(self) -> float:
        total: float = 0

        for detalle in self.detalles:
            total = total + detalle.calcular_subtotal()

        return total

    def mostrar_pedido(self) -> None:
        print("\n========== DATOS DEL PEDIDO ==========")
        print("Pedido:", self.idpedido)
        print("Fecha:", self.fecha)
        print("Cliente:", self.cliente)
        print("\nDetalle del pedido:")

        if len(self.detalles) == 0:
            print("El pedido no tiene productos.")
        else:
            for detalle in self.detalles:
                print(detalle)

        print("--------------------------------------")
        print(f"Total del pedido: S/ {self.calcular_total():.2f}")

    def __str__(self) -> str:
        return (
            f"Pedido {self.idpedido} | "
            f"Fecha: {self.fecha} | "
            f"Total: S/ {self.calcular_total():.2f}"
        )
