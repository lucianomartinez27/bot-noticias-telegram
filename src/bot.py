#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from telegram.ext import Updater
from config.token import token
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging

class Bot:
    """ Crea un objeto Bot para telegram.

    Parametros:
    nombre (str): Nombre que tiene el bot.

    """
    def __init__(self, nombre):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(nombre)
        self.level = logging.INFO

        # Updater: es el encargado de contestar a los comandos que envíe el usuario.
        self.updater = Updater(token=token, use_context=True)
        # Está a la espera de que se ingresen comandos
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
    
    def esperar_mensaje(self):
        """ Espera cualquier cosa en el chat que no sea un comando """ 
        mensaje = MessageHandler(Filters.text & (~Filters.command), self.echo)
        self.dispatcher.add_handler(mensaje)

    def contestar_mensaje(self, update, context):
        """ Responde al usuario cuando ingresa algo que no sea un comando """
        context.bot.send_message(chat_id=update.effective_chat.id, text="Disculpá, no te entiendo. Aún estoy en construcción.")
        #mensaje = update.message.text
        self.logger.info(update.message.text)
        #if mensaje in secciones:
            #mostrar_noticias(mensaje)
        
    def start(self, update, context):
        """ Esta función se ejecuta cuando al bot le envían el comando '/start'. """
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
            /secciones
            /diarios
            /clima
            """)



if __name__ == '__main__':
    noticias_bot = Bot("noticias_argentina_bot")
    noticias_bot.esperar_comando("start", noticias_bot.start)
    noticias_bot.esperar_comando("ayuda", noticias_bot.ayuda)
    noticias_bot.esperar_mensaje()