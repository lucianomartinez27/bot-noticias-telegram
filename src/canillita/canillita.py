#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Import Counter (para trend topics)
from collections import Counter

# Import KEYS API
from config.keys import API_NEWS_KEY
# Import NEWSAPI
from newsapi import NewsApiClient

# Importamos funcion para filtrar palabras comunes en /tt
from regex.palabras_regex import encontrar_palabras_archivo, encontrar_palabras_string


class Canillita:
    """Clase que se encarga de recolectar las noticias de Argentina"""
    def __init__(self):
        # Init NEWSAPI
        self.repositorio_noticias = NewsApiClient(api_key=API_NEWS_KEY)

    def pedir_noticias(self, categoria=None, cantidad=1, tema= None):
        """función que devuelve las cinco noticas más destacadas del repositorio
        Parámetros:
        categoria:
        cantidad:
        tema:"""
        articulos = self.repositorio_noticias.get_top_headlines(
                                                            q=tema,
                                                            language='es',
                                                            country='ar',
                                                            page_size=cantidad,
                                                            category=categoria)
        return articulos
        
    def pedir_temas_del_dia(self, cantidad):
        """Devuelve las palabras más mencionados en las noticias del día.
        Parámetros:
            cantidad (int): cantidad de temas
        Devuelve:
            Lista de tuplas con la palabra y la cantidad de apariciones."""
        noticias_del_dia = self.pedir_noticias(cantidad=100)

        # Palabras que no queremos ver entre los trend topics.
        palabras_comunes = encontrar_palabras_archivo("./canillita/10000_formas_RAE.txt", 5000)
        medios = ["infobae", "clarín", "telefé" ,"telefenoticias", "mdz", "chars", "com", "nación"]
        palabras_a_descartar = palabras_comunes + medios

        # Recorremos los artículos y luego su descripción, título y contenido, obteniendo el texto.
        # Agregamos las palabras a la lista palabras_clave.
        palabras_clave = []
        for articulo in noticias_del_dia['articles']:
            texto = "{} {} {}".format(articulo['description'], articulo['title'], articulo['content'] )
            palabras = encontrar_palabras_string(texto)
            for palabra in palabras:
                if palabra.lower() not in palabras_a_descartar:
                    palabras_clave.append(palabra.title()) # Añadimos las palabras que cumplen las condiciones.

        # Crea un objeto de tipo Counter de la clase collections para contar las palabras más usadas.
        temas_del_dia = Counter(palabras_clave)
        return temas_del_dia.most_common(cantidad)