import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


class Conexion:
    _HOST: str = "localhost"
    _USER: str = "root"
    _PASSWORD: str = "123456"
    _DATABASE: str = "bd_acme_poo_dao_mvc"
    _PORT: int = 3306

    @classmethod
    def obtener_conexion(cls) -> MySQLConnection | None:
        try:
            conexion: MySQLConnection = mysql.connector.connect(
                host=cls._HOST,
                user=cls._USER,
                password=cls._PASSWORD,
                database=cls._DATABASE,
                port=cls._PORT
            )
            return conexion
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    @classmethod
    def cerrar_recursos(
        cls,
        conexion: MySQLConnection | None = None,
        cursor: MySQLCursor | None = None
    ) -> None:
        try:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
        except Error as e:
            print(f"Error al cerrar recursos: {e}")
