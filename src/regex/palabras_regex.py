#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo que utiliza expresiones regulares para encontrar palabras en un texto (archivo o cadena de texto),
distinguiendolas de números, símbolos, etc.
"""

import re
patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+")


def encontrar_palabras_archivo(archivo, cantidad_palabras):
    """ Encuentra palabras en un archivo mediante expresiones regulares.
        Parametros: 
            archivo: archivo de texto plano, formato utf-8, donde encontrar las palabras.
            cantidad_palabras: tamaño de la lista que será devuelta.
                Tipo: (int)
        Retorna:
            Lista con palabras encontradas, de largo de cantidad_palabras."""
    with open(archivo, 'r') as f:
        return re.findall(patron, f.read())[:cantidad_palabras]


def encontrar_palabras_string(cadena):
    """ Encuentra palabras en una cadena de texto mediante expresiones regulares.
        Parametros: 
            cadena: texto donde encontraremos las palabras.
                Tipo:(str)
        Retorna:
                 Lista con las palabras encontradas."""
    return re.findall(patron, cadena)
