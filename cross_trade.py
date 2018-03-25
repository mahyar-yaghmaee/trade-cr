import sys
import time
import gdax
import datetime
import os


class GdaxHelper():
    COIN_TO_USD_PRODUCT_ID = {
                              'bitcoin': 'BTC-USD',
                              'bitcoincash': 'BCH-USD',
                              'etherium': 'ETH-USD',
                              'litecoin': 'LTC-USD'
                              }

    def __init__(self):
        self.public_client = gdax.PublicClient()

    def get_coin_price(self, coin_type):
        """
        Shows current coin price as well as time of the query
        :param coin_type: type  of coin, could be : bitcoin, bitcoincash,  etherium, litecoin
        :return: list of price and query time [coin_price, query_time]
        """
        if coin_type.lower() not in self.COIN_TO_USD_PRODUCT_ID:
            raise RuntimeError('Incorrect coin type {}'.format({coin_type}))

        coin_product_id = self.COIN_TO_USD_PRODUCT_ID[coin_type]
        crypto_coin_api = self.public_client.get_product_ticker(product_id=coin_product_id)
        return crypto_coin_api['price'], crypto_coin_api['time']

    def get_current_price_for_all_coins(self):
        """
        shows the current price for all coins (ehterium, bitcoin, bitcoin-cash, and litecoin)
        :return: dictionary in form of {'bitcoin': 10234, 'litecoin': 100, 'bitcoincash': 900, 'etherium': 500}
        to map coin name to ts current price
        """
        coin_price_pair = {}
        # TODO: look at performace for iterator
        for coin_name, coin_product_id in self.COIN_TO_USD_PRODUCT_ID.iteritems():
            coin_price_pair[coin_name] = self.public_client.get_product_ticker(product_id=coin_product_id)['price']
        return coin_price_pair

 #   def get_lite_coin_to_all_other_coins_price_ratio(self, coin_to_compare_to_others):




    def get_coin_to_coin_ratio(self, first_coin, second_coin):
        """
        Generates price ratio of two coins at current time
        :param first_coin: first coin type
        :param second_coin: second coin type
        :return: int, ratio of first_coin_price/second_coin_price
        """
        if first_coin.lower() not in self.COIN_TO_USD_PRODUCT_ID or second_coin.lower() not in self.COIN_TO_USD_PRODUCT_ID:
            raise RuntimeError('Incorrect coin type for ratio {}/{}' .format(first_coin, second_coin))

        # need to get first element of price function which returns the price!

        current_price_ratio = float(self.get_coin_price(first_coin)[0])/float(self.get_coin_price(second_coin)[0])
        #TODO: better to return everythin (including prices of the coins with a single call...to avoid delays)
        # todo: return current_price_ratio, price1, price2
        return current_price_ratio


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
        bitcoin_current_price, bitcoincoin_query_time = gdax_helper.get_coin_price(coin_type='bitcoin')
        bitcoincash_current_price, bitcoincash_query_time = gdax_helper.get_coin_price(coin_type='bitcoincash')
        etherium_current_price, etherium_query_time = gdax_helper.get_coin_price(coin_type='etherium')
        litecoin_current_price, litecoin_query_time = gdax_helper.get_coin_price(coin_type='litecoin')


        print 'bitcash :  ', bitcoincash_current_price
        print 'lite:  ', litecoin_current_price
        print 'ratio: ', gdax_helper.get_coin_to_coin_ratio('litecoin', 'bitcoin')

        print '00000'
        print gdax_helper.get_current_price_for_all_coins()
        print '-------'


if __name__ == "__main__":
    main(sys.argv[1:])