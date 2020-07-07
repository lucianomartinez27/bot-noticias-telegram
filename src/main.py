#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import KEYS API
from config.keys import TOKEN_TELEGRAM
from bot_noticias import BotDeNoticiasPorTelegram


if __name__ == '__main__':
    noticias_bot = BotDeNoticiasPorTelegram("noticias_argentina_bot", TOKEN_TELEGRAM)
