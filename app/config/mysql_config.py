from app.config.config import DB_HOST, DB_PASSWORD, DB_USER, DB_NAME
import mysql.connector
from mysql.connector import Error
import app.logger as logger

def initialize_mysql_connection() -> mysql.connector.connection.MySQLConnection:
    """
    Initializes a MySQL connection using the provided configuration.
    Returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
    except Error as e:
        logger.error(f"Error while connecting to MySQL: {e}")
        return None