#!/usr/bin/env python3
"""
filtered_logger.py
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter_datum """
    for field in fields:
        message = re.sub(rf'{field}=[^{separator}]+',
                         rf'{field}={redaction}', message)
    return message
