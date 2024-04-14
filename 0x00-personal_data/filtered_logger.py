#!/usr/bin/env python3
"""
filtered_logger.py
"""
from typing import List
import re
import logging
import mysql.connector
import os


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter_datum """
    return re.sub(
        rf"\b({'|'.join(fields)})=[^{separator}]+",
        lambda m: f"{m.group(1)}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ RedactingFormatter """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ __init__ """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)


PII_FIELDS = (
    "name",
    "email",
    "phone",
    "ssn",
    "password",
)


def get_logger() -> logging.Logger:
    """ get_logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get_db """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main() -> None:
    """ main """
    my_db = get_db()
    my_cursor = my_db.cursor()

    my_cursor.execute("SELECT * FROM users")
    records = my_cursor.fetchall()

    logger = get_logger()

    for record in records:
        name, email, phone, ssn, password, ip, last_login, user_agent = record
        logger.info(
            f"name={name};email={email};phone={phone};" +
            f"ssn={ssn};password={password};ip={ip};" +
            f"last_login={last_login};user_agent={user_agent};")


if __name__ == "__main__":
    main()
