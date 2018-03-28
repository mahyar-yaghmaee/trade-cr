import sys
import time
import gdax
import datetime
import os



def get_lite_coin_price(public_client):
    lite_coin_api = public_client.get_product_ticker(product_id='LTC-USD')
    lite_coin_price = lite_coin_api['price']
    query_time = lite_coin_api['time']
    return query_time, lite_coin_price


def get_historic_average_price(litecoin_historic_prices_list, current_price, number_of_historic_points):
    litecoin_historic_prices_list.append(float(current_price))
    print(litecoin_historic_prices_list)
    litecoin_historic_prices_list = litecoin_historic_prices_list[-number_of_historic_points:]
    print(litecoin_historic_prices_list)

    average_price = sum(litecoin_historic_prices_list) / float(len(litecoin_historic_prices_list))
    return average_price


def get_current_time():
    return datetime.datetime.utcnow().isoformat()


def get_past_date_time_utc(days, hours, minutes, seconds):
    past_date = datetime.datetime.utcnow() - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return past_date.isoformat()


def main(argv):
    key = os.environ['GDAX_KEY']
    b64secret = os.environ['GDAX_B64SECRET']
    passphrase = os.environ['GDAX_PASSPHRASE']

    period = 1
    public_client = gdax.PublicClient()
    litecoin_historic_prices_list = []
    number_of_historic_points = 3

    print public_client.get_product_historic_rates('LTC-USD', granularity=100)

    print public_client.get_product_24hr_stats('LTC-USD')

    while True:
        time.sleep(int(period))
        query_time, lite_coin_price = get_lite_coin_price(public_client=public_client)

        average_price = get_historic_average_price(
            litecoin_historic_prices_list=litecoin_historic_prices_list,
            current_price=lite_coin_price,
            number_of_historic_points=number_of_historic_points)
   #     print(litecoin_historic_prices_list)

        print 'past : ', get_past_date_time_utc(days=0, hours=1, minutes=0, seconds=0)
        print 'time: ', query_time, ', price: ', lite_coin_price, ', Moving average: ', average_price
        print '-----'



if __name__ == "__main__":
    main(sys.argv[1:])