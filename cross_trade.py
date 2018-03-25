import sys
import time
import datetime
import os

from gdax_helper import GdaxHelper


def main(argv):
    period = 1
    gdax_helper = GdaxHelper()

    litecoin_initial_price = 160.21
    bitcoin_cash_initial_price = 979.38
    bitcoin_initial_price = 8521.00
    etherium_initial_price = 521.18
    usd = 52.60
    init_amount_of_litecoin_bought = 0.32733706

    while True:
        time.sleep(int(period))
    #    bitcoin_current_price, bitcoincoin_query_time = gdax_helper.get_coin_price(coin_type='bitcoin')
    #    bitcoincash_current_price, bitcoincash_query_time = gdax_helper.get_coin_price(coin_type='bitcoincash')
    #    etherium_current_price, etherium_query_time = gdax_helper.get_coin_price(coin_type='etherium')
    #    litecoin_current_price, litecoin_query_time = gdax_helper.get_coin_price(coin_type='litecoin')


     #   print 'bitcash :  ', bitcoincash_current_price
     #   print 'lite:  ', litecoin_current_price
     #   print 'ratio: ', gdax_helper.get_coin_to_coin_ratio('litecoin', 'bitcoin')

     #   print '00000'
     #   print gdax_helper.get_current_price_for_all_coins()
        print gdax_helper.get_coin_to_coin_price_ratio_for_all_coins()
        print '-------'


if __name__ == "__main__":
    main(sys.argv[1:])