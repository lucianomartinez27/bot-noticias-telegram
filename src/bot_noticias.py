#!/ust/bin/env python3
#-*- coding: utf-8 -*-

# Se importa el Bot Base
from bot import BotTelegram

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Import Counter (para trend topics)
from collections import Counter

# Import KEYS API
from config.keys import API_NEWS_KEY
# Import NEWSAPI
from newsapi import NewsApiClient

# Import acortador de URL
from pyshorteners import Shortener

# Importamos funcion para filtrar palabras comunes en /tt
from regex.palabras_regex import encontrar_palabras_archivo, encontrar_palabras_string

# Init NEWSAPI
newsapi = NewsApiClient(api_key=API_NEWS_KEY)

# Init shortener
shortener = Shortener()
tinyurl = shortener.tinyurl.short

class BotNoticias(BotTelegram):
    """Clase que hereda de BotTelegram, añadiendo los métodos para un bot de noticias Argentinas"""
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)

    def start(self, update, context):
        """ Esta función realiza una presentación cuando se ejecuta el comando '/start'."""
        self.logger.info('He recibido el comando start')
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = "Bienvenido al Bot de Noticias de Argentina, puedes usar '/ayuda' \npara ver los comandos"
        )

    def ayuda(self, update, context):
        """ Muestra los comandos más importantes. """
        self.logger.info('He recibido el comando ayuda')
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = """Los comandos que pueden ayudarte son:
        /seccion - Busca las noticias por sección
        /tt - Te devuelve las 10 palabras más usadas en las noticias del día.
        /top5 - Devuelve las 5 noticias más relevantes del momento
        
        Además, escribiendo palabras claves, recibes una noticia relacionada a ese palabra. """)

    def top_noticias(self, update, context):
        """ Devuelve las 5 noticias más importantes del momento en Argentina."""
        self.logger.info('He recibido el comando top5')
        
        top5_noticias = newsapi.get_top_headlines(
                                        language='es',
                                        country='ar',
                                        page_size=5)
        for articulo in top5_noticias['articles']:  
                context.bot.send_message(
                parse_mode = 'Markdown',
                chat_id = update.message.chat_id,
                text = "Título: [{}]({}) \nAutor: {}".format(articulo['title'],tinyurl(articulo['url']), articulo['author']))

    def seccion(self, update, context):
        """Genera una botonera para que el usuario seleccione la opción que desea ingresar"""
        self.logger.info('He recibido el comando seccion')
        opciones = [[InlineKeyboardButton("Entretenimiento", callback_data='entertainment'),
        InlineKeyboardButton("Salud", callback_data='health')],
        [InlineKeyboardButton("Ciencia", callback_data='science'),
        InlineKeyboardButton("Tecnología", callback_data='technology')],
        [InlineKeyboardButton("Deportes", callback_data='sports'),
        InlineKeyboardButton("Negocios", callback_data='business')]]
                    
        botones = InlineKeyboardMarkup(opciones)
        update.message.reply_text('Elija una de las secciones:', reply_markup=botones)
        
    def noticia_por_tema(self, update, context):
        """Devuelve al usuario 3 noticias según la opción el elija mediante la función seccion"""
        self.logger.info('He recibido el comando noticia_por_tema')

        # Objeto que devuelve Telegram
        query = update.callback_query
        # Botón que presiona el usuario desde la app
        tema = query.data

        top3_noticias_tema = newsapi.get_top_headlines(
                                        language='es',
                                        country='ar',
                                        page_size=3,
                                        category=tema)
        for articulo in top3_noticias_tema['articles']:
            context.bot.send_message(
            parse_mode = 'Markdown',
            chat_id = query.message.chat_id,
            text = "Título: [{}]({}) \nAutor: {}".format(articulo['title'],tinyurl(articulo['url']), articulo['author']))
        
    def noticia_por_mensaje(self, update, context):
        """ Devuelve al usuario tres noticias relacionadas con el texto que escriba, si las encuentra. """
        self.logger.info('He recibido un mensaje')

        # Recolecta una noticia mediante la api
        mensaje = update.message.text.lower()
        noticias_mensaje = newsapi.get_top_headlines(
                                        q=mensaje,
                                        language='es',
                                        country = 'ar',
                                        page_size=3,
                                        )
        # Comprueba que haya al menos una noticia.
        if noticias_mensaje['articles']:
            for articulo in noticias_mensaje['articles']:
                context.bot.send_message(
                parse_mode = 'Markdown',
                chat_id = update.message.chat_id,
                text = "Título: [{}]({}) \nAutor: {}".format(articulo['title'],tinyurl(articulo['url']), articulo['author']))
        else:
            context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Lo siento, no pude encontrar noticias relacionadas a '{}'.".format(mensaje))
    
    def trend_topics(self, update, context):
        """"Devuelve cuales son los temás más escritos en las noticias nacionales."""
        self.logger.info('He recibido el comando trend topics')

        # Buscamos las noticas en la API
        noticias_tt = newsapi.get_top_headlines(
                                            language='es',
                                            country='ar',
                                            page_size=100)
        
        # Palabras que no queremos ver entre los trend topics.
        medios = ["infobae", "clarín", "telefé" ,"telefenoticias", "mdz", "chars", "com"]
        palabras_comunes = encontrar_palabras_archivo("src/10000_formas_RAE.txt", 5000)
        palabras_a_descartar = palabras_comunes + medios

        # Recorremos los artículos y luego su descripción, título y contenido, obteniendo el texto.
        # Agregamos las palabras a la lista palabras_clave.
        palabras_clave = []
        for articulo in noticias_tt['articles']:
            cadena = "{} {} {}".format(articulo['description'], articulo['title'], articulo['content'] )
            contenido = encontrar_palabras_string(cadena)
            for palabra in contenido:
                if palabra.lower() not in palabras_a_descartar:
                    palabras_clave.append(palabra.title()) # Añadimos las palabras que cumplen las condiciones.

        # Crea un objeto de tipo Counter de la clase collections para contar las palabras más usadas.
        cantidad_palabras = Counter(palabras_clave)
        temas_tt = ""
        for tema in enumerate(cantidad_palabras.most_common(10), 1): # Elige los 10 temas mas mencionados en las noticas.
            temas_tt += f"{tema[0]} - {tema[1][0]}\n" # Número y tema.
        context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = "Los temas del momento son:\n{}".format(temas_tt))