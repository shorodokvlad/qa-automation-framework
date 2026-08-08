import os
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBConnector:
    """
    Database connector supporting both PostgreSQL (psycopg2) and MySQL (pymysql).
    Used to validate data persistence directly against the database during automated tests.
    """

    def __init__(
        self,
        db_type: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None
    ):
        self.db_type = (db_type or os.getenv("DB_TYPE", "postgresql")).lower()
        self.host = host or os.getenv("DB_HOST", "aws-0-eu-central-1.pooler.supabase.com")
        self.port = int(port or os.getenv("DB_PORT", "5432" if self.db_type == "postgresql" else "3306"))
        self.dbname = dbname or os.getenv("DB_NAME", "postgres")
        self.user = user or os.getenv("DB_USER", "postgres.ztgssqhtytwtxzjdmdyu")
        self.password = password or os.getenv("DB_PASSWORD", "_7zxTLcY85HJ$F4/")
        self.connection = None

    def connect(self):
        """Establish connection to the configured database engine."""
        if self.connection and not self.connection.closed if hasattr(self.connection, "closed") else False:
            return self.connection

        try:
            if self.db_type == "postgresql":
                import psycopg2
                from psycopg2.extras import RealDictCursor
                self.connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    cursor_factory=RealDictCursor
                )
            elif self.db_type == "mysql":
                import pymysql
                import pymysql.cursors
                self.connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    database=self.dbname,
                    user=self.user,
                    password=self.password,
                    cursorclass=pymysql.cursors.DictCursor
                )
            else:
                raise ValueError(f"Unsupported DB_TYPE: {self.db_type}. Use 'postgresql' or 'mysql'.")

            logger.info(f"Successfully connected to {self.db_type} database '{self.dbname}' on {self.host}:{self.port}")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to {self.db_type} database on {self.host}:{self.port} - Error: {e}")
            raise

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return rows as a list of dictionaries."""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an UPDATE/INSERT query and commit changes."""
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution error: {e}")
            conn.rollback()
            raise

    def set_user_email_verified(self, email: str) -> bool:
        """Helper to mark user email as verified directly in database for testing."""
        query = "UPDATE users SET email_verified = true WHERE email = %s;"
        rows_affected = self.execute_update(query, (email,))
        return rows_affected > 0


    def verify_user_exists_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Verify user record exists in 'users' table."""
        query = "SELECT id, name, email, role, email_verified FROM users WHERE email = %s;"
        rows = self.execute_query(query, (email,))
        return rows[0] if rows else None

    def get_order_items_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetch all order items associated with a specific user ID."""
        query = "SELECT id, quantity, price, status, product_id, user_id FROM order_items WHERE user_id = %s;"
        return self.execute_query(query, (user_id,))

    def get_or_create_test_product(self) -> int:
        """Fetch existing product ID or insert a test category & product."""
        try:
            products = self.execute_query("SELECT id FROM products LIMIT 1;")
            if products:
                return products[0]["id"]
            
            categories = self.execute_query("SELECT id FROM categories LIMIT 1;")
            if categories:
                cat_id = categories[0]["id"]
            else:
                self.execute_update("INSERT INTO categories (name) VALUES ('General');")
                cat_id = self.execute_query("SELECT id FROM categories LIMIT 1;")[0]["id"]

            self.execute_update(
                "INSERT INTO products (name, description, price, category_id, stock_quantity) VALUES (%s, %s, %s, %s, %s);",
                ("QA Test Item", "Automated test item", 60.00, cat_id, 100)
            )
            res = self.execute_query("SELECT id FROM products WHERE name = %s;", ("QA Test Item",))
            return res[0]["id"] if res else 1
        except Exception as e:
            logger.warning(f"Unable to query/create test product: {e}")
            return 1


    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")
