#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Librerias telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler

# Registro de actividades
import logging


class BotTelegram:
    """Clase base para crear instancias de un Bot de Telegram

        >>> MiBot = BotTelegram(nombre, token)

    """

    def __init__(self, nombre, token):
        """Inicializa las variables básicas para que el bot de Telegram funcione."""
        # loggin: Sirve para enviar un registro de las actividades.
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(nombre)
        # Updater: es el encargado de contestar a los comandos que envíe el usuario.
        self.updater = Updater(token=token, use_context=True)
        # Polling se pone a la espera de que se ingresen comandos
        self.updater.start_polling()
        # Dispatcher: está al pendiente de todas las ventanas donde se encuentra el bot.
        self.dispatcher = self.updater.dispatcher
        # Diccionario con los comandos que va a ejecutar el bo
        self.comandos = {}
        
    def enviar_mensaje(self, bot, id_usuario, mensaje, parse_mode=None):
        """Función que envía un mensaje desde un bot y a un usuario en particular.
        Parámetros:
        bot: --completar
        usuario: id de telegram del usuario
        text: mensaje a enviar
        parse_mode:"""
        bot.send_message(chat_id=id_usuario, text=mensaje, parse_mode=parse_mode)

    def ejecutar_comando(self, update, context):
        """Intenta ejecutar un comando de el diccionario 'comandos' cuando lo ingresa por el chat.
            Si no lo encuentra, se captura la excepción y se informa al usuario de que no existe."""
        bot = context.bot
        usuario = update.message
        comando = update.message.text

        try:
            self.comandos[comando](bot, usuario)
        except KeyError:
            self.enviar_mensaje(bot, usuario.chat_id, "Comando no disponible.")
        
    def esperar_comando(self):
        """ Función que espera que un comando se ingrese en el chat de telegram.
        """
        comando = MessageHandler(Filters.command, self.ejecutar_comando)
        self.dispatcher.add_handler(comando)
          
    def contestar_consulta(self, funcion):
        """Función que espera que el usuario presione un botón que se despliega en el chat de telegram
        Parametro:
        funcion (func): función que se ejecuta al presionar un botón en el chat"""
        self.dispatcher.add_handler(CallbackQueryHandler(funcion))
    
    def contestar_mensaje(self, funcion):
        """ Espera cualquier cosa en el chat que no sea un comando (mensajes)
        Parametro:
        funcion (func): función que se ejecuta al recibir un mensaje en el chat""" 
        mensaje_recibido = MessageHandler(Filters.text & (~Filters.command), funcion)
        self.dispatcher.add_handler(mensaje_recibido)
