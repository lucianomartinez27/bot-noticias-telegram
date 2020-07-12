#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import KEYS API
from config.keys import TOKEN_TELEGRAM
from bot_noticias import BotDeNoticiasPorTelegram


if __name__ == '__main__':
    noticias_bot = BotDeNoticiasPorTelegram("noticias_argentina_bot", TOKEN_TELEGRAM)
    noticias_bot.esperar_comando("start", noticias_bot.start)
    noticias_bot.esperar_comando("ayuda", noticias_bot.ayuda)
    noticias_bot.esperar_comando("top5", noticias_bot.top5)
    noticias_bot.esperar_comando("trendtopics", noticias_bot.trend_topics)
    noticias_bot.esperar_comando("secciones", noticias_bot.secciones)
    noticias_bot.contestar_consulta(noticias_bot.noticia_por_seccion)
    noticias_bot.contestar_mensaje(noticias_bot.noticia_por_mensaje)
