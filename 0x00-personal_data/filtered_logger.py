#!/usr/bin/env python3
"""
filtered_logger.py
"""
import re


def filter_datum(fields, redaction, message, separator):
    """ filter_datum """
    for field in fields:
        message = re.sub(rf'{field}=[^{separator}]+',
                         rf'{field}={redaction}', message)
    return message
