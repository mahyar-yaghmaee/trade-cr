import gdax

class GdaxHelper():
    COIN_TO_USD_PRODUCT_ID = {
        'bitcoin': 'BTC-USD',
        'bitcoincash': 'BCH-USD',
        'etherium': 'ETH-USD',
        'litecoin': 'LTC-USD'
    }
    NAME_OF_COINS_LIST = list(COIN_TO_USD_PRODUCT_ID.keys())

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

    def get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices(self):
        """
        Shows the current price ratio beetween all coins
        :return: retusn a dictionary in for of {'bitcoin/litecoin': 80.5, 'bitcoin/etherium': 20.2, 'litecoin/bitcoin': 0.17, ...}, {'litecoin: 100,'bitcon':1000, ,,,,}
        This is for all types of coins and also individual prcing
        #TODO: improve doc
        """
        price_ratio = {}
        coin_price_pair = self.get_current_price_for_all_coins()
        # TODO: remove hardcoding

        # TODO: need to return individual + all prices in one call ot avoid delay!
        # litecoin-to-others!
        price_ratio['litecoin/bitcoin'] = float(coin_price_pair['litecoin']) / float(coin_price_pair['bitcoin'])
        price_ratio['litecoin/bitcoincash'] = float(coin_price_pair['litecoin']) / float(coin_price_pair['bitcoincash'])
        price_ratio['litecoin/etherium'] = float(coin_price_pair['litecoin']) / float(coin_price_pair['etherium'])
        # etherium-to-others!
        price_ratio['etherium/bitcoin'] = float(coin_price_pair['etherium']) / float(coin_price_pair['bitcoin'])
        price_ratio['etherium/bitcoincash'] = float(coin_price_pair['etherium']) / float(
            coin_price_pair['bitcoincash'])
        price_ratio['etherium/litecoin'] = float(coin_price_pair['etherium']) / float(coin_price_pair['litecoin'])
        # bitcoincash-to-others!
        price_ratio['bitcoincash/bitcoin'] = float(coin_price_pair['bitcoincash']) / float(coin_price_pair['bitcoin'])
        price_ratio['bitcoincash/etherium'] = float(coin_price_pair['bitcoincash']) / float(coin_price_pair['etherium'])
        price_ratio['bitcoincash/litecoin'] = float(coin_price_pair['bitcoincash']) / float(coin_price_pair['litecoin'])
        # bitcoin-to-others!
        price_ratio['bitcoin/bitcoincash'] = float(coin_price_pair['bitcoin']) / float(coin_price_pair['bitcoincash'])
        price_ratio['bitcoin/etherium'] = float(coin_price_pair['bitcoin']) / float(coin_price_pair['etherium'])
        price_ratio['bitcoin/litecoin'] = float(coin_price_pair['bitcoin']) / float(coin_price_pair['litecoin'])

        return price_ratio, coin_price_pair

    def get_coin_to_coin_ratio(self, first_coin, second_coin):
        """
        Generates price ratio of two coins at current time
        :param first_coin: first coin type
        :param second_coin: second coin type
        :return: int, ratio of first_coin_price/second_coin_price
        """
        if first_coin.lower() not in self.COIN_TO_USD_PRODUCT_ID or second_coin.lower() not in self.COIN_TO_USD_PRODUCT_ID:
            raise RuntimeError('Incorrect coin type for ratio {}/{}'.format(first_coin, second_coin))

        # need to get first element of price function which returns the price!

        current_price_ratio = float(self.get_coin_price(first_coin)[0]) / float(self.get_coin_price(second_coin)[0])
        # TODO: better to return everythin (including prices of the coins with a single call...to avoid delays)
        # todo: return current_price_ratio, price1, price2
        return current_price_ratio
