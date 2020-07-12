#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Import Counter (para temas del día)
from collections import Counter

# Import KEYS API
from config.keys import API_NEWS_KEY
# Import NEWSAPI
from newsapi import NewsApiClient

# Importamos funcion para filtrar palabras comunes en temas del día
from regex.palabras_regex import encontrar_palabras_archivo, encontrar_palabras_string


class Canillita:
    """Clase que se encarga de recolectar las noticias de Argentina."""
    def __init__(self):
        # Init NEWSAPI
        self.repositorio_noticias = NewsApiClient(api_key=API_NEWS_KEY)

    def pedir_noticias(self, categoria=None, cantidad=1, tema= None):
        """función que devuelve las cinco noticias más destacadas del repositorio.
            Para más información se puede visitar  <https://newsapi.org/docs/endpoints/top-headlines>.
        Parámetros:
            categoria: Devuelve noticias de esa categoría.
                Elegir entre: {"business", "entertainment", "general", "health", "science", "sports", "technology"}
                Tipo: (str o None)
            cantidad: Devuelve esa cantidad de noticias.
                Tipo: (int o None)
            tema: Devuelve las noticias que contengan esa palabra clave.
                Tipo: (str o None)
        Retorna:
            Diccionario con los articulos obtenidos mediante ApiNews.
        """
        articulos = self.repositorio_noticias.get_top_headlines(
                                                            q=tema,
                                                            language='es',
                                                            country='ar',
                                                            page_size=cantidad,
                                                            category=categoria)
        return articulos
        
    def pedir_temas_del_dia(self, cantidad=1):
        """Devuelve las palabras más mencionados en las noticias del día.
        Parámetros:
            cantidad: cantidad de temas del día.
                Tipo: (int)
        Retorno:
            Tipo: collections.Counter
            Contenido: Palabras y la cantidad de apariciones.
                Ejm: {'Coronavirus': 23, 'Pandemia': 10, 'Covid': 8}
        """
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