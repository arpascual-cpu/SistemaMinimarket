from __future__ import annotations

from modelos.categoria import Categoria


class Producto:
    def __init__(
        self,
        idproducto: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria: Categoria
    ) -> None:
        self.idproducto: str = idproducto
        self.descripcion: str = descripcion
        self.precio: float = precio
        self.stock: int = stock
        self.categoria: Categoria = categoria

        categoria.agregar_producto(self)

    def reducir_stock(self, cantidad: int) -> bool:
        if cantidad <= self.stock:
            self.stock = self.stock - cantidad
            return True
        else:
            return False

    def __str__(self) -> str:
        return (
            f"{self.idproducto} - {self.descripcion} | "
            f"Precio: S/ {self.precio:.2f} | "
            f"Stock: {self.stock} | "
            f"Categoría: {self.categoria.descripcion}"
        )
