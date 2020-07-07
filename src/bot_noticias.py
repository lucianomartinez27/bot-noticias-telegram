#!/ust/bin/env python3
#-*- coding: utf-8 -*-

# Se importa el Bot Base
from bot import BotTelegram

# Se importa Canillita que ayuda a recolectar noticias
from canillita.canillita import Canillita

# Import acortador de URL
from pyshorteners import Shortener

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Init shortener
acortar_url = Shortener().tinyurl.short


class BotDeNoticiasPorTelegram(BotTelegram):
    """Clase que hereda de BotTelegram, añadiendo los métodos para un bot de noticias Argentinas
        >>> MiBotDeNoticias = BotTelegram(nombre, token)"""

    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)
        self.canillita = Canillita()
        self.comandos = {"/start": self.start, "/ayuda": self.ayuda, "/top5": self.top5, "/tt": self.trend_topics,
                         "/seccion": self.secciones}
        self.contestar_consulta(self.noticia_por_seccion)
        self.contestar_mensaje(self.noticia_por_mensaje)
        self.esperar_comando()

    def enviar_noticias(self, bot, id_usuario, noticias):
        if noticias['articles']:
            for articulo in noticias['articles']:
                mensaje = "Título: [{}]({}) \nAutor: {}".format(articulo['title'], acortar_url(articulo['url']),
                                                                articulo['author'])
                self.enviar_mensaje(bot, id_usuario, mensaje, 'Markdown')
        else:
            mensaje = "Lo siento, no pude encontrar ninguna noticia."
            self.enviar_mensaje(bot, id_usuario, mensaje)

    def start(self, bot, usuario):
        """ Esta función realiza una presentación cuando se ejecuta el comando '/start'."""
        self.logger.info('He recibido el comando start')

        mensaje = "Bienvenido al Bot de Noticias de Argentina, puedes usar '/ayuda' \npara ver todos los comandos."
        self.enviar_mensaje(bot, usuario.chat_id, mensaje)

    def ayuda(self, bot, usuario):
        """ Muestra los comandos más importantes. """
        self.logger.info('He recibido el comando ayuda')

        mensaje = """Los comandos que pueden ayudarte son:
                    /seccion - Busca las noticias por sección
                    /tt - Te devuelve las 10 palabras más usadas en las noticias del día.
                    /top5 - Devuelve las 5 noticias más relevantes del momento
                    Además, escribiendo palabras claves, recibes una noticia relacionada a ese palabra.
                """
        self.enviar_mensaje(bot, usuario.chat_id, mensaje)

    def top5(self, bot, usuario):
        """ Devuelve las 5 noticias más importantes del momento en Argentina."""
        self.logger.info('He recibido el comando top5')

        # Recolección y envío de noticias
        top5_noticias = self.canillita.pedir_noticias(cantidad=5)
        self.enviar_noticias(bot, usuario.chat_id, top5_noticias)

    def trend_topics(self, bot, usuario):
        """"Devuelve cuales son los temás más escritos en las noticias nacionales."""
        self.logger.info('He recibido el comando trend topics')

        # Búsqueda de temas del día y envío de mensaje
        temas_del_dia = self.canillita.pedir_temas_del_dia(10)
        temas_tt = ""
        for pos, tema in enumerate(temas_del_dia, 1): # Elige los 10 temas mas mencionados en las noticas.
            temas_tt += f"{pos} - {tema[0]}\n" # posición y tema.
        mensaje = "Los temas del momento son:\n {}".format(temas_tt)
        self.enviar_mensaje(bot, usuario.chat_id, mensaje)

    def secciones(self, bot, usuario):
        """Genera una botonera para que el usuario seleccione la opción que desea ingresar"""
        self.logger.info('He recibido el comando seccion')

        opciones = [[InlineKeyboardButton("Entretenimiento", callback_data='entertainment'),
                    InlineKeyboardButton("Salud", callback_data='health')],
                    [InlineKeyboardButton("Ciencia", callback_data='science'),
                    InlineKeyboardButton("Tecnología", callback_data='technology')],
                    [InlineKeyboardButton("Deportes", callback_data='sports'),
                    InlineKeyboardButton("Negocios", callback_data='business')]]

        botones = InlineKeyboardMarkup(opciones)
        usuario.reply_text('Elija una de las secciones:', reply_markup=botones)
        
    def noticia_por_seccion(self, update, context):
        """Devuelve al usuario 3 noticias según la opción el elija mediante la función seccion"""
        self.logger.info('He recibido el comando noticia_por_tema')

        categoria = update.callback_query.data
        usuario = update.callback_query.message.chat_id
        bot = context.bot
        # Recolección y envío de noticias
        noticias = self.canillita.pedir_noticias(categoria=categoria)
        self.enviar_noticias(bot, usuario, noticias)
        
    def noticia_por_mensaje(self, update, context):
        """ Devuelve al usuario tres noticias relacionadas con el texto que escriba. """
        self.logger.info('He recibido un mensaje')

        # Datos que devuelve Telegram
        usuario = update.message.chat_id
        bot = context.bot
        mensaje = update.message.text

        # Recolección y envío de noticias
        noticias_mensaje = self.canillita.pedir_noticias(tema=mensaje)
        self.enviar_noticias(bot, usuario, noticias_mensaje)
