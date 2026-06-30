from mysql.connector import Error

from bd.conexion import Conexion
from modelos.categoria import Categoria


class CategoriaDAO:
    _INSERTAR: str = """
        INSERT INTO categoria (idcategoria, descripcion)
        VALUES (%s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idcategoria, descripcion
        FROM categoria
        ORDER BY descripcion;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idcategoria, descripcion
        FROM categoria
        WHERE idcategoria = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE categoria
        SET descripcion = %s
        WHERE idcategoria = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM categoria
        WHERE idcategoria = %s;
    """

    @classmethod
    def insertar(cls, categoria: Categoria) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._INSERTAR, (categoria.idcategoria, categoria.descripcion))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar categoría: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Categoria]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        categorias: list[Categoria] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    categorias.append(Categoria(reg[0], reg[1]))
            except Error as e:
                print(f"Error al listar categorías: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return categorias

    @classmethod
    def buscar_por_id(cls, idcategoria: str) -> Categoria | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        categoria: Categoria | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idcategoria,))
                reg = cursor.fetchone()
                if reg is not None:
                    categoria = Categoria(reg[0], reg[1])
            except Error as e:
                print(f"Error al buscar categoría: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return categoria

    @classmethod
    def actualizar(cls, categoria: Categoria) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ACTUALIZAR, (categoria.descripcion, categoria.idcategoria))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar categoría: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idcategoria: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idcategoria,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar categoría: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas
