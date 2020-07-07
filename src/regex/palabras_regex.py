#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+")


def encontrar_palabras_archivo(archivo, cantidad_palabras):
    """ Encuentra palabras en un archivo mediante expresiones regulares.
        Parametros: 
                    archivo: texto plano donde encontrar la palabra.
                    cantidad_palabras: tamaño de la lista que será devuelta.
        Devuelve:
                 Lista con palabras encontradas, de largo cantidad_palabras."""
    with open(archivo, 'r') as f:
        return re.findall(patron, f.read())[:cantidad_palabras]


def encontrar_palabras_string(cadena):
    """ Encuentra palabras en una cadena de texto mediante expresiones regulares.
        Parametros: 
                    cadena: texto donde encontraremos las palabras.
        Devuelve:
                 Lista con las palabras encontradas."""
    return re.findall(patron, cadena)