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

        query = update.callback_query
        tema = query.data

        try:
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
        except:
            query.edit_message_text(text= "Lo siento. Ocurrió un error intesperado.")
        
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
        palabras_clave = []
        palabras_a_descartar = "para como entre desde este esta estas estos días lunes martes \
        miércoles jueves viernes sábado domingo chars] nuevo nueva nuevos nuevas comenzó terminó  \
        casos cuando porque quien durante después menos inicio final cerca pero  mientras contra \
        tambien está podría podrían será hasta ahora según luego donde tiene tienen gran \
        otro otra otros otras infobae ambito clarín crónica todo noticias".split()

        # Recorremos los artículos y luego su descripción, título y contenido.
        for articulo in noticias_tt['articles']:
            # El if revisa que las secciones no estén vacías, ya que daría error al hacer split().
            if articulo['description'] and articulo['title'] and articulo['content']:
                contenido = articulo['description'].split() + articulo['title'].split() + articulo['content'].split()
                for palabra in contenido:
                    if palabra.lower() not in palabras_a_descartar and "." not in palabra and len(palabra) > 3:
                        palabras_clave.append(palabra) # Añadimos las palabras que cumplen las condiciones.

        # Crea un objeto de tipo Counter de la clase collections para contar las palabras más usadas.
        cantidad_palabras = Counter()
        for palabra in palabras_clave:
            cantidad_palabras[palabra.title()] += 1
        temas_tt = ""
        for elemento in enumerate(cantidad_palabras.most_common(10), 1): # Elige los 10 temas mas mencionados en las noticas.
            temas_tt += f"{elemento[0]} - {elemento[1][0]}\n"
        context.bot.send_message(
                    chat_id = update.message.chat_id,
                    text = "Los temas del momento son:\n{}".format(temas_tt))