from __future__ import annotations

from modelos.producto import Producto


class DetallePedido:
    def __init__(
        self,
        producto: Producto,
        cantidad: int
    ) -> None:
        self.producto: Producto = producto
        self.cantidad: int = cantidad
        self.precio: float = producto.precio

    def calcular_subtotal(self) -> float:
        return self.cantidad * self.precio

    def __str__(self) -> str:
        return (
            f"{self.producto.descripcion} | "
            f"Cantidad: {self.cantidad} | "
            f"Precio: S/ {self.precio:.2f} | "
            f"Subtotal: S/ {self.calcular_subtotal():.2f}"
        )
