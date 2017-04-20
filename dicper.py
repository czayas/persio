#!/usr/bin/env python3
u"""
DicPer - Diccionario Persistente (Ejemplo de uso de Persio).

Copyleft 2017, Carlos Zayas Guggiari <czayas@gmail.com>
"""

import sys
import readline
import persio


class Main:
    """Se instancia si este script se ejecuta como programa principal."""

    def __init__(self, nombre='dicper.db'):
        """Constructor: Prepara el archivo y procesa los argumentos."""
        self.estante = persio.Persio(nombre)
        if not self.estante.esarchivo():
            print('El archivo "{}" ya existe y está en uso.'.format(nombre))

        # Configuración de autocompletado.
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completar)

        args = sys.argv[1:]  # Lista de argumentos de la linea de comandos.
        arg = '' if not args else ' '.join(args)

        if arg:
            self.procesar(arg)
        else:
            self.consola()

    def completar(self, prefijo, indice):
        """Completador (event handler para readline)."""
        if prefijo is not None:
            palabras = [palabra for palabra in self.estante.keys()
                        if palabra.startswith(prefijo)]
        try:
            return palabras[indice]
        except IndexError:
            return None

    def procesar(self, linea):
        u"""Procesa la línea introducida como argumento o por consola."""
        secciones = [seccion.strip() for seccion in linea.split(':', 1)]
        clave = secciones.pop(0)  # Retira primer elemento de la lista.
        existe = lambda k: k in self.estante
        elemento = None if not secciones else secciones.pop()
        consulta = ':' not in linea

        if not consulta:
            if not elemento:
                resultado = self.estante.dic.pop(clave, None)
            else:
                if existe(clave):
                    self.estante[clave].append(elemento)
                else:
                    self.estante[clave] = [elemento]
                resultado = []
        else:
            resultado = None if not existe(clave) else self.estante[clave]

        return resultado

    def consola(self):
        u"""CLI: Interfaz de Línea de Comandos."""
        print(__doc__)
        print(self.ayuda())

        while True:
            try:
                linea = input('> ')  # Inductor (Prompt).
                if linea not in ['quit', 'exit']:
                    resultado = self.procesar(linea)
                    if resultado:
                        for elemento in resultado:
                            print(elemento)
                    else:
                        if resultado is None:
                            print(self.ayuda())
                else:
                    break
            except (KeyboardInterrupt, EOFError):  # Ctrl+D o fin de archivo.
                sys.exit(0)  # Salir sin errores.

    def ayuda(self):
        u"""Retorna texto explicativo de la aplicación de ejemplo."""
        return ''.join(open('dicper.txt').readlines())


MAIN = __name__ == '__main__'  # Determina si se ejecuta como principal.
# Esto permite al script ser importado como un módulo desde otro script.
if MAIN:
    Main()  # Si se ejecuta como principal, se instancia la clase Main.
