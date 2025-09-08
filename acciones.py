import yfinance as yf
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Diccionario de tickers de acciones argentinas.
# El sufijo.BA es necesario para las acciones que cotizan en la BCBA.
ARGENTINIAN_STOCKS = {
    "ggal": "GGAL.BA",
    "pamp": "PAMP.BA",
    "ypfd": "YPFD.BA",
    "alua": "ALUA.BA",
    "bma": "BMA.BA",
    "txar": "TXAR.BA",
    "loma": "LOMA.BA",
    # Puedes añadir más tickers aquí, como "YPFD" [2, 3]
}

COMPANY_LOGOS = {
    "ggal": "./archivos/img/logos/Logo_Banco_Galicia.png",
    "pamp": "./archivos/img/logos/Logo_Pampa.png",
    "ypfd": "./archivos/img/logos/Logo_YPF.png",
    "alua": "./archivos/img/logos/Logo_Aluar.png",
    "bma": "./archivos/img/logos/Logo_Macro.png",
    "txar": "./archivos/img/logos/Logo_Ternium.png",
    "loma": "./archivos/img/logos/Logo_Loma.png",
}

def create_stocks_markup():
    """
    Crea un teclado con botones inline para las acciones.
    """
    markup = InlineKeyboardMarkup()
    for name, ticker in ARGENTINIAN_STOCKS.items():
        markup.add(InlineKeyboardButton(text=f"📈 {name.upper()}", callback_data=f"stock_{name}"))
        
    markup.add(InlineKeyboardButton(text="📊 Todas las acciones", callback_data="stock_all"))
    return markup

    

def get_stock_price(ticker_symbol):
    """
    Obtiene y formatea el precio de una acción utilizando yfinance.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        if 'regularMarketPrice' in info:
            price = info['regularMarketPrice']
            name = info.get('longName', ticker_symbol)
            change = info.get('regularMarketChangePercent')

            # Determinar emoji según signo de variación
            if change is not None:
                if change > 0:
                    change_text = f"🟢 +{change:.2f}%"
                elif change < 0:
                    change_text = f"🔴 {change:.2f}%"
                else:
                    change_text = f"⚪ {change:.2f}%"
            else:
                change_text = "N/D"

            message_text = (
                f"📈 *{name} ({ticker_symbol}):*\n"
                f"Precio actual: *${price:.2f}*\n"
                f"Variación diaria: *{change_text}*"
            )
            return message_text
        else:
            return f"❌ No se pudo obtener el precio para el ticker {ticker_symbol}.\n"

    except Exception as e:
        return f"❌ Error: {e}\n"
