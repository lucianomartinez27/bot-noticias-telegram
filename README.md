# BOT NOTICIAS ARGENTINAS - TELEGRAM
Proyecto para el curso de Python de [GUGLER](https://www.gugler.com.ar)

## Detalles IMPORTANTES a tener en cuenta:

Para que el bot funcione, es necesario crear un token en Telegram mediante [BotFather](https://t.me/botfather), además de generar una Key en [NewsAPI](https://newsapi.org/). 

Estos códigos deben colocarse en un archivo llamado 'keys.py', en la carpeta 'config' dentro de 'src' (el archivo **no** se encuentra en el repositorio.).

La estructura de keys.py es la siguiente:

```
TOKEN_TELEGRAM = "TOKEN"
API_NEWS_KEY = "KEY"
```
### Enlaces útiles:
* [Documentación Python-Telegram-Bot](https://python-telegram-bot.readthedocs.io/en/stable/)
* [Bots de Telegram en Python - Medium](https://medium.com/@goyoregalado/bots-de-telegram-en-python-134b964fcdf7)

#### Requirements
    * python-telegram-bot
    * pyshorteners
    * newsapi-python
