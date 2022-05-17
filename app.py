import json, config
from os import environ
from flask import Flask, request , render_template
from binance.client import Client
from binance.enums import *
from binance.futures import Futures as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
import logging
import os
app = Flask(__name__)
config_logging(logging, logging.DEBUG)


proxies = {
"http": "http://wmno21chfaf6yl:nr5xfafkybz11d8ddy98xa4nh3drp@us-east-static-08.quotaguard.com:9293",
"https": "http://wmno21chfaf6yl:nr5xfafkybz11d8ddy98xa4nh3drp@us-east-static-08.quotaguard.com:9293",
}

API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']

client = Client(API_KEY, API_SECRET, base_url="https://fapi.binance.com", proxies=proxies)
#client = Client(config.TEST_API_KEY, config.TEST_API_SECRET, base_url="https://testnet.binancefuture.com", proxies=proxies)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():

    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code" : "error",
            "message":"Nice Try invalid passphrase"
        }
    dict = {'key': 'value'}
    all_balance = client.balance()
    for currency in all_balance:
        dict[currency['asset']] = currency['balance']
    try:
        leverageBtc = client.change_leverage(symbol='BTCBUSD',leverage = 2, recvWindow=6000)
        leverageEth = client.change_leverage(symbol='ETHBUSD',leverage = 3, recvWindow=6000)
        leverageSol = client.change_leverage(symbol='SOLBUSD',leverage = 2, recvWindow=6000)
        leverageBnb = client.change_leverage(symbol='BNBBUSD',leverage = 2, recvWindow=6000)
        leverageXrp = client.change_leverage(symbol='XRPBUSD',leverage = 2, recvWindow=6000)
        if(data['ticker'] == "BTCBUSDPERP"):
            quantity_busd = round((float(dict['BUSD']) / data['price']) * 0.45,3)
            response = client.new_order(symbol='BTCBUSD', side = data['order_action'].upper(), type= "MARKET", quantity=quantity_busd)
            print(f"The quantity is {quantity_busd}")
            logging.info(response)
            logging.info(leverageBtc)
        elif(data['ticker'] == "ETHBUSDPERP"):
            quantity_busd = round((float(dict['BUSD']) / data['price']) * 0.45,3)
            print(f"Quantity is {quantity_busd}")
            response = client.new_order(symbol='ETHBUSD',side = data['order_action'].upper(), type= "MARKET", quantity=quantity_busd)
            logging.info(response)
            logging.info(leverageEth)
        elif(data['ticker'] == "SOLBUSDPERP"):
            quantity_busd = round((float(dict['BUSD']) / data['price']) * 0.45,1)
            print(f"Quantity is {quantity_busd}")
            response = client.new_order(symbol='SOLBUSD',side = data['order_action'].upper(), type= "MARKET", quantity=quantity_busd)
            logging.info(response)
            logging.info(leverageSol)
        elif(data['ticker'] == "BNBBUSDPERP"):
            quantity_busd = round((float(dict['BUSD']) / data['price']) * 0.45,2)
            print(f"Quantity is {quantity_busd}")
            response = client.new_order(symbol='SOLBUSD',side = data['order_action'].upper(), type= "MARKET", quantity=quantity_busd)
            logging.info(response)
            logging.info(leverageBnb)
        elif(data['ticker'] == "XRPBUSDPERP"):
            quantity_busd = (float(dict['BUSD']) / data['price']) * 0.45
            print(f"Quantity is {quantity_busd}")
            response = client.new_order(symbol='XRPBUSD',side = data['order_action'].upper(), type= "MARKET", quantity=quantity_busd)
            logging.info(response)
            logging.info(leverageXrp)
    except ClientError as error:
        logging.error(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.error_code, error.error_message
            )
        )

    return {
        "code": "success",
        "message": "Order success"
    }
