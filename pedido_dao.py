from mysql.connector import Error

from bd.conexion import Conexion
from modelos.cliente import Cliente
from modelos.detalledepedido import DetallePedido
from modelos.pedido import Pedido
from modelos.producto import Producto
from modelos.categoria import Categoria


class PedidoDAO:
    _INSERTAR_PEDIDO: str = """
        INSERT INTO pedido (idpedido, fecha, idcliente)
        VALUES (%s, %s, %s);
    """

    _INSERTAR_DETALLE: str = """
        INSERT INTO detalle_pedido (idpedido, idproducto, cantidad, precio)
        VALUES (%s, %s, %s, %s);
    """

    _DESCONTAR_STOCK: str = """
        UPDATE producto
        SET stock = stock - %s
        WHERE idproducto = %s AND stock >= %s;
    """

    _DEVOLVER_STOCK: str = """
        UPDATE producto p
        INNER JOIN detalle_pedido d ON p.idproducto = d.idproducto
        SET p.stock = p.stock + d.cantidad
        WHERE d.idpedido = %s;
    """

    _SELECCIONAR: str = """
        SELECT pe.idpedido, pe.fecha,
               c.idcliente, c.apellidos, c.nombres, c.direccion, c.telefono
        FROM pedido pe
        INNER JOIN cliente c ON pe.idcliente = c.idcliente
        ORDER BY pe.fecha DESC, pe.idpedido DESC;
    """

    _BUSCAR_PEDIDO: str = """
        SELECT pe.idpedido, pe.fecha,
               c.idcliente, c.apellidos, c.nombres, c.direccion, c.telefono
        FROM pedido pe
        INNER JOIN cliente c ON pe.idcliente = c.idcliente
        WHERE pe.idpedido = %s;
    """

    _DETALLES_PEDIDO: str = """
        SELECT p.idproducto, p.descripcion, d.precio, p.stock,
               c.idcategoria, c.descripcion,
               d.cantidad
        FROM detalle_pedido d
        INNER JOIN producto p ON d.idproducto = p.idproducto
        INNER JOIN categoria c ON p.idcategoria = c.idcategoria
        WHERE d.idpedido = %s
        ORDER BY p.descripcion;
    """

    _ELIMINAR_PEDIDO: str = """
        DELETE FROM pedido
        WHERE idpedido = %s;
    """

    @classmethod
    def registrar_pedido(cls, pedido: Pedido) -> bool:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None

        if cursor is None:
            return False

        try:
            cursor.execute(cls._INSERTAR_PEDIDO, (pedido.idpedido, pedido.fecha, pedido.cliente.idcliente))

            for detalle in pedido.detalles:
                cursor.execute(
                    cls._DESCONTAR_STOCK,
                    (detalle.cantidad, detalle.producto.idproducto, detalle.cantidad)
                )

                if cursor.rowcount == 0:
                    raise ValueError(f"Stock insuficiente para el producto {detalle.producto.descripcion}.")

                cursor.execute(
                    cls._INSERTAR_DETALLE,
                    (pedido.idpedido, detalle.producto.idproducto, detalle.cantidad, detalle.precio)
                )

            conexion.commit()
            return True

        except (Error, ValueError) as e:
            print(f"Error al registrar pedido: {e}")
            conexion.rollback()
            return False

        finally:
            Conexion.cerrar_recursos(conexion, cursor)

    @classmethod
    def seleccionar(cls) -> list[Pedido]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        pedidos: list[Pedido] = []

        if cursor is not None:
            try:
                cursor.execute(cls._SELECCIONAR)
                for reg in cursor.fetchall():
                    cliente = Cliente(reg[2], reg[3], reg[4], reg[5], reg[6])
                    pedido = Pedido(reg[0], str(reg[1]), cliente)
                    pedido.detalles = cls.obtener_detalles_pedido(reg[0])
                    pedidos.append(pedido)
            except Error as e:
                print(f"Error al listar pedidos: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return pedidos

    @classmethod
    def buscar_por_id(cls, idpedido: str) -> Pedido | None:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        pedido: Pedido | None = None

        if cursor is not None:
            try:
                cursor.execute(cls._BUSCAR_PEDIDO, (idpedido,))
                reg = cursor.fetchone()
                if reg is not None:
                    cliente = Cliente(reg[2], reg[3], reg[4], reg[5], reg[6])
                    pedido = Pedido(reg[0], str(reg[1]), cliente)
                    pedido.detalles = cls.obtener_detalles_pedido(idpedido)
            except Error as e:
                print(f"Error al buscar pedido: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return pedido

    @classmethod
    def obtener_detalles_pedido(cls, idpedido: str) -> list[DetallePedido]:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None
        detalles: list[DetallePedido] = []

        if cursor is not None:
            try:
                cursor.execute(cls._DETALLES_PEDIDO, (idpedido,))
                for reg in cursor.fetchall():
                    categoria = Categoria(reg[4], reg[5])
                    producto = Producto(reg[0], reg[1], float(reg[2]), int(reg[3]), categoria)
                    detalle = DetallePedido(producto, int(reg[6]))
                    detalle.precio = float(reg[2])
                    detalles.append(detalle)
            except Error as e:
                print(f"Error al obtener detalles del pedido: {e}")
            finally:
                Conexion.cerrar_recursos(conexion, cursor)

        return detalles

    @classmethod
    def eliminar(cls, idpedido: str) -> bool:
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor() if conexion else None

        if cursor is None:
            return False

        try:
            cursor.execute(cls._DEVOLVER_STOCK, (idpedido,))
            cursor.execute(cls._ELIMINAR_PEDIDO, (idpedido,))
            filas = cursor.rowcount
            conexion.commit()
            return filas > 0

        except Error as e:
            print(f"Error al eliminar pedido: {e}")
            conexion.rollback()
            return False

        finally:
            Conexion.cerrar_recursos(conexion, cursor)
