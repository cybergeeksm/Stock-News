import requests
from datetime import datetime, timedelta
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API = "OPMXIZRAFE6AQB8H"
NEWS_API = 'a65f4c9e6cde4520ade2f594a6f6f4ce'
ACCOUNT_SID = 'ACc957806b8b31753944b30bdc60711b20'
AUTH_TOKEN = '126586737a8dc0731f5b3fa93d6c4c81'
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
STOCK_URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey={STOCK_API}'
stock_response = requests.get(STOCK_URL)
stock_data = stock_response.json()['Time Series (Daily)']
now = datetime.today()
previous_day = str((now - timedelta(days=2)).date())
day_before_yesterday = str((now - timedelta(days=3)).date())
prev_price = float(stock_data[previous_day]['4. close'])
day_before_prev_price = float(stock_data[day_before_yesterday]['4. close'])
diff = prev_price - day_before_prev_price
per = diff/prev_price * 100
stock_message=""""""
# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"),
# actually get the first 3 news pieces for the COMPANY_NAME.
if abs(per) > 5:
    per = per.__round__(2)
    news_para = {
        'q': COMPANY_NAME,
        'from': now.date(),
        'sortBy': 'popularity',
        'apiKey': NEWS_API
    }
    news_url = f'https://newsapi.org/v2/everything?'
    news = requests.get(url=news_url, params=news_para)
    news_data = news.json()['articles']

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.
    symbols = ['🔺', '🔻']
    if per < 0:
        symbol = symbols[1]
    else:
        symbol = symbols[0]

    for i in range(3):
        stock_message += f"""
        TESLA: {symbol}{per}%
        Headline: {news_data[i]['title']}. 
        Brief:{news_data[i]['description']}.\n
        """
    print(stock_message)
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=stock_message,
        from_='+19497872169',
        to='+919123784891'
    )
    print(message.sid)

# Optional: Format the SMS message like this:


