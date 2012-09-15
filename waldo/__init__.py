'''
WALDO : WHERE PROTEINS ARE

This is a Python library to collect information about proteins from online
databases (Uniprot, MGI, ...) and expose it as an easy to use Python library.
'''
from .translations.services import translate

__all__ = [
    'translate',
    ]
