from __future__ import annotations


class Categoria:
    def __init__(self, idcategoria: str, descripcion: str) -> None:
        self.idcategoria: str = idcategoria
        self.descripcion: str = descripcion
        self.productos: list[Producto] = []

    def agregar_producto(self, producto: Producto) -> None:
        self.productos.append(producto)

    def mostrar_productos(self) -> None:
        print(f"\nCategoría: {self.descripcion}")
        print("Productos:")

        for producto in self.productos:
            print(producto)

    def __str__(self) -> str:
        return f"{self.idcategoria} - {self.descripcion}"
