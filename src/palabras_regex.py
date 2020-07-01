#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import re
patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]{1,}")

def encontrar_palabras_archivo(archivo, cantidad_palabras):
    """ Encuentra palabras en un archivo mediante expresiones regulares
        Parametros: 
                    archivo: texto plano donde encontrar la palabra.
                    cantidad_palabras: tamaño de la lista que será devuelta.
        Devuelve:
                 Lista de largo cantidad_palabras"""
    with open(archivo, 'r') as f:
        return re.findall(patron, f.read())[:cantidad_palabras]

def encontrar_palabras_string(cadena):
    """ Encuentra palabras en una cadena de texto mediante expresiones regulares
        Parametros: 
                    cadena: tamaño de la lista que será devuelta.
        Devuelve:
                 Lista de largo cantidad_palabras"""
    patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]{1,}")
    return re.findall(patron, cadena)