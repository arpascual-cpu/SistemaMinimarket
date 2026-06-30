from mysql.connector import Error

from bd.conexion import Conexion
from dao.categoria_dao import CategoriaDAO
from modelos.categoria import Categoria
from modelos.producto import Producto


class ProductoDAO:
    _INSERTAR: str = """
        INSERT INTO producto (idproducto, descripcion, precio, stock, idcategoria)
        VALUES (%s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT p.idproducto, p.descripcion, p.precio, p.stock,
               c.idcategoria, c.descripcion
        FROM producto p
        INNER JOIN categoria c ON p.idcategoria = c.idcategoria
        ORDER BY p.descripcion;
    """

    _BUSCAR_POR_ID: str = """
        SELECT p.idproducto, p.descripcion, p.precio, p.stock,
               c.idcategoria, c.descripcion
        FROM producto p
        INNER JOIN categoria c ON p.idcategoria = c.idcategoria
        WHERE p.idproducto = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE producto
        SET descripcion = %s,
            precio = %s,
            stock = %s,
            idcategoria = %s
        WHERE idproducto = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM producto
        WHERE idproducto = %s;
    """

    _PRODUCTOS_POR_CATEGORIA: str = """
        SELECT p.idproducto, p.descripcion, p.precio, p.stock,
               c.idcategoria, c.descripcion
        FROM producto p
        INNER JOIN categoria c ON p.idcategoria = c.idcategoria
        WHERE c.idcategoria = %s
        ORDER BY p.descripcion;
    """

    _STOCK_BAJO: str = """
        SELECT p.idproducto, p.descripcion, p.precio, p.stock,
               c.idcategoria, c.descripcion
        FROM producto p
        INNER JOIN categoria c ON p.idcategoria = c.idcategoria
        WHERE p.stock <= %s
        ORDER BY p.stock ASC;
    """

    @classmethod
    def _crear_producto_desde_registro(cls, reg: tuple) -> Producto:
        categoria = Categoria(reg[4], reg[5])
        return Producto(reg[0], reg[1], float(reg[2]), int(reg[3]), categoria)

    @classmethod
    def insertar(cls, producto: Producto) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                valores = (
                    producto.idproducto,
                    producto.descripcion,
                    producto.precio,
                    producto.stock,
                    producto.categoria.idcategoria
                )
                cursor.execute(cls._INSERTAR, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar producto: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Producto]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        productos: list[Producto] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    productos.append(cls._crear_producto_desde_registro(reg))
            except Error as e:
                print(f"Error al listar productos: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return productos

    @classmethod
    def buscar_por_id(cls, idproducto: str) -> Producto | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        producto: Producto | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idproducto,))
                reg = cursor.fetchone()
                if reg is not None:
                    producto = cls._crear_producto_desde_registro(reg)
            except Error as e:
                print(f"Error al buscar producto: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return producto

    @classmethod
    def actualizar(cls, producto: Producto) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                valores = (
                    producto.descripcion,
                    producto.precio,
                    producto.stock,
                    producto.categoria.idcategoria,
                    producto.idproducto
                )
                cursor.execute(cls._ACTUALIZAR, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar producto: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idproducto: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idproducto,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar producto: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def listar_por_categoria(cls, idcategoria: str) -> list[Producto]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        productos: list[Producto] = []

        if cursor is not None:
            try:
                cursor.execute(cls._PRODUCTOS_POR_CATEGORIA, (idcategoria,))
                for reg in cursor.fetchall():
                    productos.append(cls._crear_producto_desde_registro(reg))
            except Error as e:
                print(f"Error al listar productos por categoría: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return productos

    @classmethod
    def listar_stock_bajo(cls, stock_maximo: int) -> list[Producto]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        productos: list[Producto] = []

        if cursor is not None:
            try:
                cursor.execute(cls._STOCK_BAJO, (stock_maximo,))
                for reg in cursor.fetchall():
                    productos.append(cls._crear_producto_desde_registro(reg))
            except Error as e:
                print(f"Error al listar productos con stock bajo: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return productos
