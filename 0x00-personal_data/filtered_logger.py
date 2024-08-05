#!/usr/bin/env python3
"""Contains a filter function for data obfuscate."""

from typing import List
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self , fields):
        """COnstructor method."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log record."""
        return filter_datum(self.fields, self.REDACTION, super(RedactingFormatter, self).format(record), self.SEPARATOR)

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscate specified fields data"""

    return_val = re.sub(r'(\w+)=[a-zA-Z0-9@.-\:]*',
                        lambda match_: match_.group(1) + '=' + redaction
                        if match_.group(1) in fields
                        else match_.group(0), message)
    return return_val
