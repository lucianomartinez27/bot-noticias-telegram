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

### Requirements
    * python-telegram-bot
    * pyshorteners
    * newsapi-python
