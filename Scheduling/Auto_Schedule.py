import threading
import requests
import json
import time
import re
import datetime
import logging
import traceback

logging.basicConfig(filename='production.log', level=logging.DEBUG)


def oanda_request(login_request_body, provider_api_url, request_headers):
    logging.info(str(datetime.datetime.now()) + "  ******* Start OANDA Request  *******  ")
    response = requests.post(provider_api_url, data=json.dumps(login_request_body),
                             headers=request_headers,
                             verify=False)
    logging.info(response)
    logging.info(response.status_code)

    logging.info(str(datetime.datetime.now()) + " ////////// End  OANDA Request ///////////  ")


def fire_oanda_request(login_request_body, provider_api_url, request_headers):
    threading.Thread(target=oanda_request, args=(login_request_body, provider_api_url, request_headers)).start()


def main():
    #  ************************* Start Declaration *************************++

    provider_api_url = 'https://api-fxpractice.oanda.com/v3/accounts/101-001-16477519-001/orders'
    provider_authorization = 'Bearer 4e6693eb463b767a665647581259288f-d21a4563efeb0510fadfd58ba94f13bc'
    provider_accept_datetime_format = 'RFC3339'

    #  ************************* Start Telegram API Call **************************

    request_headers = {
        "Authorization": provider_authorization,
        "Accept-Datetime-Format": provider_accept_datetime_format,
        "Connection": "Keep-Alive",
        "Content-Type": "application/json;charset=UTF-8"
    }

    while True:
        
        try:
              utc_time=datetime.utcnow()




              

                    login_request_body = {
                        "order": {
                            "type": "MARKET",
                            "instrument": instrument,
                            "units": units,
                            "timeInForce": "IOC",
                            "positionFill": "DEFAULT",
                            "takeProfitOnFill": {
                                "price": take_profit
                            },
                            "stopLossOnFill": {
                                "price": stop_loss
                            }
                        }
                    }

                    logging.info(request_headers)
                    logging.info(login_request_body)
                    fire_oanda_request(login_request_body, provider_api_url, request_headers)      

        except:
            logging.error("Oops! somethings is wrong , " + traceback.format_exc())

        send_request = True
        time.sleep(1)
        logging.shutdown()


if __name__ == '__main__':
    main()
