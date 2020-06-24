#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Librerias telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Registro de actividades
import logging

# Import KEYS API
from config.keys import TOKEN_TELEGRAM

class BotTelegram:
    """ Crea un objeto Bot para telegram.

    Parametros:
    nombre (str): Nombre que tiene el bot.

    """
    def __init__(self, nombre, token):
        """Inicializa las variables básicas para que el bot de Telegram funcione"""
        # loggin: Sirve para enviar un registro de las actividades.
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(nombre)
        # Updater: es el encargado de contestar a los comandos que envíe el usuario.
        self.updater = Updater(token=token, use_context=True)
        # Polling se pone a la espera de que se ingresen comandos
        self.updater.start_polling()
        # Dispatcher: está al pendiente de todas las ventanas donde se encuentra el bot.
        self.dispatcher = self.updater.dispatcher
        
    def esperar_comando(self, nombre = None, comando = None):
        """ Función que espera que un comando se ingrese en el chat de telegram.
        Parametros:
        nombre (str): nombre del comando que el usuario escibe en el chat ejm: 'start'.
        comando (func): función que se ejecutará al llamar al comando.
        """
        self.dispatcher.add_handler(CommandHandler(nombre, comando))
    
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