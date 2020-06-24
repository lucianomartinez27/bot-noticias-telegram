#!/ust/bin/env python3
#-*- coding: utf-8 -*-

from bot import BotTelegram

# Import Counter (para trend topics)
from collections import Counter

# Import KEYS API
from config.keys import API_NEWS_KEY
# Import NEWSAPI
from newsapi import NewsApiClient

# Import acortador de URL

from pyshorteners import Shortener

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
        """ Muestra los comandos más importantes """
        self.logger.info('He recibido el comando ayuda')
        context.bot.send_message(
            chat_id = update.message.chat_id,
            text = """Los comandos que pueden ayudarte son:
        /seccion - Busca las noticias por sección
        /tt - Te devuelve las 10 palabras más usadas en las noticias del día.
        /top5 - Devuelve las 5 noticias más relevantes del momento
        
        Además, escribiendo palabras claves, recibes una noticia relacionada a ese palabra. """)

    def top_noticias(self, update, context):
        """ Devuelve las 5 noticias más importantes del momento en Argentina"""
        self.logger.info('He recibido el comando top5')
        
        top5_noticias = newsapi.get_top_headlines(
                                        language='es',
                                        country='ar',
                                        page_size=5)
        for articulo in top5_noticias['articles']:  
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = tinyurl(articulo['url']))
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Título: {} \nAutor: {}".format(articulo['title'], articulo['author']))
        
    def noticia_por_tema(self, update, context):
        """Devuelve las 3 noticias más relevantes para el tema que se elija"""
        self.logger.info('He recibido el comando top_tema')

        if not context.args:
            context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Las secciones disponibles son 'entretenimiento', 'ciencia', 'deportes', 'tecnología, 'salud'")
            return None
        elif context.args[0].lower() == 'entretenimiento':
            tema = 'entertainment'
        elif context.args[0].lower() == 'ciencia':
            tema = 'science'
        elif context.args[0].lower() == 'deportes':
            tema = 'sports'
        elif context.args[0].lower() == 'salud':
            tema = 'health'
        elif context.args[0].lower() in ['tecnología', 'tecnologia']:
            tema = 'technology'

        try:
            top3_noticias_tema = newsapi.get_top_headlines(
                                            language='es',
                                            country='ar',
                                            page_size=3,
                                            category=tema)
            for articulo in top3_noticias_tema['articles']:
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = tinyurl(articulo['url']))
                context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Título: {} \nAutor: {}".format(articulo['title'], articulo['author']))

        except:
            context.bot.send_message(
                chat_id = update.message.chat_id,
                text = "Lo siento, no reconozco esa sección.")
        
    def noticia_por_mensaje(self, update, context):
        """ Devuelve al usuario tres noticias relacionadas con el texto que escriba, si las encuentra. """
        self.logger.info('He recibido un mensaje')

        # Recolecta una noticia mediante la api
        mensaje = update.message.text.lower()
        noticias_mensaje = newsapi.get_everything(
                                        q=mensaje,
                                        language='es',
                                        page_size=3,
                                        )

        if noticias_mensaje['articles']:
            for articulo in noticias_mensaje['articles']:
                    context.bot.send_message(
                        chat_id = update.message.chat_id,
                        text = tinyurl(articulo['url']))
                    context.bot.send_message(
                        chat_id = update.message.chat_id,
                        text = "Título: {} \nAutor: {}".format(articulo['title'], articulo['author']))
        else:
            context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = "Lo siento, no pude encontrar noticias relacionadas a '{}'.".format(mensaje))
    def trend_topics(self, update, context):
        """"Devuelve cuales son los temás más escritos en las noticias nacionales."""
        self.logger.info('He recibido el comando trend topics')

        noticias_tt = newsapi.get_top_headlines(
                                            language='es',
                                            country='ar',
                                            page_size=100)
        palabras_clave = []
        palabras_a_descartar = "para como entre desde este esta días lunes martes miercoles jueves \
        viernes sabado domingo infobae ambito chars] nuevo nuevas comenzó terminó casos contra para \
        cuando sin porque contra quien durante menos con inicio final cerca pero nueva".split()

        for articulo in noticias_tt['articles']:
                contenido = articulo['description'].split() + articulo['title'].split() + articulo['content'].split()
                for palabra in contenido:
                    if palabra not in palabras_a_descartar and "." not in palabra and len(palabra) > 3:
                        palabras_clave.append(palabra)

        # Crea un objeto de tipo Counter de la clase collections para contar las palabras más usadas
        cantidad_palabras = Counter()
        for palabra in palabras_clave:
            cantidad_palabras[palabra.title()] += 1
        temas_tt = ""
        for elemento in cantidad_palabras.most_common(10): # Elige los 10 temas mas mencionados en las noticas
            temas_tt += "* " + elemento[0] + "\n"
        context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = "Los temas del momento son:\n{}".format(temas_tt))