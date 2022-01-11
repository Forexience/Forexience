import requests
import calendar
import dateutil.parser as parser
import yaml
import time
import pandas as pd
import warnings
import concurrent.futures
warnings.filterwarnings('ignore')

t1 = time.perf_counter()

def convert_date(utc_time): 
    parsed_date = parser.parse(utc_time)
    var_date=parsed_date.date()
    var_time=parsed_date.time()
    var_f_time=var_time.hour
    var_julian_date=parsed_date.timetuple().tm_yday
    var_weekday=parsed_date.weekday()
    var_weekday_name=calendar.day_name[parsed_date.weekday()]
    return var_date, var_time, var_f_time, var_julian_date, var_weekday, var_weekday_name

with open ('config.yml') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    oanda_api_key = cfg['creds']['oanda_api']
    account_number = cfg['creds']['account_number']


currency_pairs = ['EUR_USD','USD_CAD','EUR_GBP','EUR_AUD','EUR_CHF',
                  'GBP_USD','GBP_CHF','GBP_NZD','GBP_AUD','GBP_CAD',
                  'AUD_CAD','AUD_CHF','AUD_NZD','NZD_USD','EUR_CAD',
                  'USD_CHF','CAD_CHF','NZD_CAD','AUD_USD','EUR_NZD',
                  'NZD_CHF']


timeframe = "H4"
price_char = "M"
price_com = "mid"
candles_count = 5000

params_count = (
    ('price', price_char),
    ('count', candles_count),
    ('granularity', timeframe),
)


provider_api_url = 'https://api-fxpractice.oanda.com/v3/accounts/{}/orders'.format(account_number)
request_headers = {
    "Authorization": oanda_api_key,
    "Accept-Datetime-Format": "RFC3339",
    "Connection": "Keep-Alive",
    "Content-Type": "application/json;charset=UTF-8"
}

provider_authorization = 'Bearer {0}'.format(oanda_api_key)

headers = {
    'Content-Type': 'application/json',
    'Authorization': provider_authorization,
}


def get_candles(pair):
    output = []
    filename = "{}_{}.csv".format(pair, timeframe)
    first_response = requests.get('https://api-fxpractice.oanda.com/v3/instruments/{}/candles'.format(pair), 
                            headers=headers,
                            params=params_count).json()

    response=first_response['candles']    
    all_candlesticks = response

    for i in range (len(all_candlesticks)):
        result= (convert_date(response[i]['time']))
        output.append([(result[0]),(result[1]),
                    (result[2]),(result[3]),
                    (result[4]),(result[5]),
                        response[i]['time'],
                        response[i]['volume'], 
                        response[i][price_com]['o'],
                        response[i][price_com]['h'],
                        response[i][price_com]['l'],
                        response[i][price_com]['c']])
        
    output = pd.DataFrame(output)
    output.columns = ['Date','Time',
                    'f_time','julian_date',
                    'Weekday','Weekday_Name',
                    'UTC_Time', 'Volume',
                    'Open', 'High', 'Low', 'Close']
    output.to_csv(filename, header = True, index = False)

with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(get_candles, currency_pairs)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')