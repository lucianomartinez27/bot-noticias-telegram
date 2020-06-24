# BOT NOTICIAS ARGENTINAS - TELEGRAM
Proyecto para el curso de Python de [GUGLER](https://www.gugler.com.ar)

## Detalles IMPORTANTES a tener en cuenta:

Para que el bot funciones es necesario crear un token en Telegram mediante *BotFather*, además de generar una Key en [NewsAPI](https://newsapi.org/). 

Estos códigos deben colocarse en un archivo llamado 'keys.py', en una carpeta llamada 'config' (la misma **NO** se encuentra en el repositorio.).

La estructora de keys.py es la siguiente:

```
TOKEN_TELEGRAM = "TOKEN"
API_NEWS_KEY = "KEY"
```

### Requirements
    * python-telegram-bot
    * pyshorteners
    * newsapi-python
