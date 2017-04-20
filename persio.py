#!/usr/bin/env python3
u"""
Persio - "Wrapper" para el módulo shelve (persistencia).

Copyleft 2017, Carlos Zayas Guggiari <czayas@gmail.com>
"""

import shelve


class Persio:
    u""""Wrapper" para el módulo shelve."""

    def __init__(self, nombre='persio.db'):
        """Constructor: Carga (si existe) o crea el archivo shelve.

        :param str nombre: Nombre del archivo que contiene la base de datos.
        """
        try:
            self.dic = shelve.open(nombre, writeback=True)
        except:
            self.dic = {}

    def __del__(self):
        """Destructor: Cierra el archivo shelve."""
        try:
            self.dic.close()
        except:
            pass

    def __repr__(self):
        """La clase va a estar representada por el diccionario dic (shelve)."""
        return repr(self.dic)

    def __getitem__(self, clave):
        """"Getter": Permite usar a la clase como si fuera un diccionario."""
        # La siguiente linea es equivalente a:
        # return None if not clave in self.dic.keys() else self.dic[clave]
        return self.dic.get(clave, None)

    def __setitem__(self, clave, valor):
        """"Setter": Permite usar a la clase como si fuera un diccionario."""
        self.dic[clave] = valor

    def __contains__(self, clave):
        """Retorna "True" si la clave existe en el diccionario."""
        # Equivalente a: return True if clave in self.dic else False
        try:
            return clave in self.dic
        except TypeError:
            return False

    def keys(self):
        """Retorna una lista con las claves del diccionario."""
        return list(self.dic.keys())

    def esarchivo(self):
        """Retorna "True" si el diccionario es un archivo shelve."""
        return isinstance(self.dic, shelve.DbfilenameShelf)
