# news_service.py
import requests
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("MARKETAUX_API_KEY")



# === Diccionario de países ===
PAISES = {
    "us": "USA",
    "mx": "México",
    "br": "Brasil",
    "ar": "Argentina",
    "gb": "Reino Unido"
}

# === Obtener noticias financieras ===
# === Diccionario de países con banderas ===
PAISES = {
    "us": {"nombre": "USA", "bandera": "🇺🇸"},
    "mx": {"nombre": "México", "bandera": "🇲🇽"},
    "br": {"nombre": "Brasil", "bandera": "🇧🇷"},
    "ar": {"nombre": "Argentina", "bandera": "🇦🇷"},
    "gb": {"nombre": "Reino Unido", "bandera": "🇬🇧"}
}


# === Obtener noticias financieras ===
def get_noticias(country="us", api_token=API_TOKEN):
    """
    Consulta las últimas noticias financieras de un país.
    Devuelve una lista de diccionarios con 'title' y 'url'.
    """
    url = (
        f"https://api.marketaux.com/v1/news/all?"
        f"countries={country}&"
        f"filter_entities=true&"
        f"limit=5&"
        f"api_token={api_token}"
    )
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            return [
                {"title": item.get("title", "Sin título"), "url": item.get("url", "#")}
                for item in data.get("data", [])
            ]
        else:
            return []
    except Exception as e:
        print(f"❌ Error al obtener noticias: {e}")
        return []


# === Construir teclado para selección de país ===
def build_news_keyboard():
    markup = InlineKeyboardMarkup()
    for pais, datos in PAISES.items():
        nombre = datos["nombre"]
        bandera = datos["bandera"]
        markup.add(InlineKeyboardButton(f"{bandera} {nombre}", callback_data=f"news:{pais}"))
    return markup


# === Formatear respuesta de noticias ===
def format_news_response(country_code, noticias):
    datos = PAISES.get(country_code, {"nombre": country_code.upper(), "bandera": "🏳️"})
    nombre_pais = datos["nombre"]
    bandera = datos["bandera"]

    if noticias:
        respuesta = f"{bandera} *Noticias de {nombre_pais}:*\n\n"
        for n in noticias:
            respuesta += f"🔹 [{n['title']}]({n['url']})\n"
    else:
        respuesta = f"{bandera} ❌ No se encontraron noticias para {nombre_pais}."
    return respuesta