STOCK = "AAPL"
COMPANY_NAME = "Apple INC"
api_key = "#################"
mediastackapikey = "#####################"
mediastackurl = "http://api.mediastack.com/v1/news?"
account_sid = "###################"
auth_token = "################"


import requests
from twilio.rest import Client

def getnews():
    mediastackparams = {
        "keywords": COMPANY_NAME,
        "access_key": mediastackapikey,
        "limit": 3,
        "categories": "business"
    }
    newsresponse = requests.get(url=mediastackurl, params=mediastackparams)
    newsresponse.raise_for_status()
    news_data = newsresponse.json()
    news = []
    news.append(news_data["data"][0]["title"])
    news.append(news_data["data"][1]["title"])
    news.append(news_data["data"][2]["title"])
    return news

def sendSMS(news):
    client = Client(account_sid, auth_token)
    for story in news:
        if change > 0:
            message = client.messages.create(
                body=f"{COMPANY_NAME}: 🔺{round(change, 2)}\n{story}",
                from_='+447723613314',
                to='+##########'
            )
            print(message.status)
        else:
            message = client.messages.create(
                body=f"{COMPANY_NAME}: 🔻{round(change, 2)}\n{story}",
                from_='+447723613314',
                to='+##########'
            )
            print(message.status)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = "https://www.alphavantage.co/query?"
params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": api_key
}
response = requests.get(url=url, params=params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday = float(data_list[0]["4. close"])
day_before = float(data_list[1]["4. close"])
#yesterday = float(stock_data["Time Series (Daily)"]["2023-06-29"]["4. close"])
#day_before = float(stock_data["Time Series (Daily)"]["2023-06-28"]["4. close"])
print(f"Yesterdays share price: {yesterday}")
print(f"Day befores share price: {day_before}")
change = ((yesterday - day_before)/day_before)*100
print(round(change, 2))
if change < 5 or change > -5:
    print("Change is less the 5%")
else:
    news = getnews()
    sendSMS(news)

## STEP 2: Use https://newsapi.org
## used this instead: https://mediastack.com/documentation
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.






#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


