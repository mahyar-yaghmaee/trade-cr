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
        return current_price_ratio


def main(argv):
    period = 1
    gdax_helper = GdaxHelper()

    while True:
        time.sleep(int(period))
        bitcoincoin_price, bitcoincoin_query_time = gdax_helper.get_coin_price(coin_type='bitcoin')
        bitcoincash_price, bitcoincash_query_time = gdax_helper.get_coin_price(coin_type='bitcoincash')
        etherium_price, etherium_query_time = gdax_helper.get_coin_price(coin_type='etherium')
        litecoin_price, litecoin_query_time = gdax_helper.get_coin_price(coin_type='litecoin')

        get_coin_to_coin_ratio = gdax_helper.get_coin_to_coin_ratio('litecoin', 'bitcoin')
        print 'bit :  ', bitcoincoin_price
        print 'lite:  ', litecoin_price
        print 'ratio: ', get_coin_to_coin_ratio
        print '-------'


if __name__ == "__main__":
    main(sys.argv[1:])