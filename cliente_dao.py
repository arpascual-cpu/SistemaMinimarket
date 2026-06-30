from mysql.connector import Error

from bd.conexion import Conexion
from modelos.cliente import Cliente


class ClienteDAO:
    _INSERTAR: str = """
        INSERT INTO cliente (idcliente, apellidos, nombres, direccion, telefono)
        VALUES (%s, %s, %s, %s, %s);
    """

    _SELECCIONAR: str = """
        SELECT idcliente, apellidos, nombres, direccion, telefono
        FROM cliente
        ORDER BY apellidos, nombres;
    """

    _BUSCAR_POR_ID: str = """
        SELECT idcliente, apellidos, nombres, direccion, telefono
        FROM cliente
        WHERE idcliente = %s;
    """

    _ACTUALIZAR: str = """
        UPDATE cliente
        SET apellidos = %s,
            nombres = %s,
            direccion = %s,
            telefono = %s
        WHERE idcliente = %s;
    """

    _ELIMINAR: str = """
        DELETE FROM cliente
        WHERE idcliente = %s;
    """

    @classmethod
    def insertar(cls, cliente: Cliente) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                valores = (cliente.idcliente, cliente.apellidos, cliente.nombres, cliente.direccion, cliente.telefono)
                cursor.execute(cls._INSERTAR, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al insertar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def seleccionar(cls) -> list[Cliente]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        clientes: list[Cliente] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    clientes.append(Cliente(reg[0], reg[1], reg[2], reg[3], reg[4]))
            except Error as e:
                print(f"Error al listar clientes: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return clientes

    @classmethod
    def buscar_por_id(cls, idcliente: str) -> Cliente | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        cliente: Cliente | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_POR_ID, (idcliente,))
                reg = cursor.fetchone()
                if reg is not None:
                    cliente = Cliente(reg[0], reg[1], reg[2], reg[3], reg[4])
            except Error as e:
                print(f"Error al buscar cliente: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return cliente

    @classmethod
    def actualizar(cls, cliente: Cliente) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                valores = (cliente.apellidos, cliente.nombres, cliente.direccion, cliente.telefono, cliente.idcliente)
                cursor.execute(cls._ACTUALIZAR, valores)
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al actualizar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas

    @classmethod
    def eliminar(cls, idcliente: str) -> int:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        filas: int = 0

        if cursor is not None:
            try:
                cursor.execute(cls._ELIMINAR, (idcliente,))
                conexion.commit()
                filas = cursor.rowcount
            except Error as e:
                print(f"Error al eliminar cliente: {e}")
                conexion.rollback()
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return filas
