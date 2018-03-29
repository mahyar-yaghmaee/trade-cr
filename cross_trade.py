import sys
import time
import logging
import gdax
import os

from gdax_helper import GdaxHelper

GDAX_FEE = 0.006  # 0.6 percent fee
BUY_SELL_MARGIN = 0.005  # 0.5 percent profit


class GdaxTrader():
    def __init__(self):
        key = os.environ['GDAX_KEY']
        b64secret = os.environ['GDAX_B64SECRET']
        passphrase = os.environ['GDAX_PASSPHRASE']
        self.auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
        self.gdax_helper = GdaxHelper()

    def sell_market_value(self, size_to_sell_coin_size, coin_type):
        """
        Sell coin in market value with coin size. coin size needs to be at least 0.1 (for litecoin)
        :param size_to_sell_coin_size: String representation of float. like '0.1'
        :param coin_type: type of coin: 'bitcoin', 'litecoin', bitcoincash', 'etherium'
        :return: sell result in json
        """
        sell_result = self.auth_client.sell(
            size=size_to_sell_coin_size,  # of Coin
            product_id=self.gdax_helper.COIN_TO_USD_PRODUCT_ID[coin_type.lower()],  # example 'LTC-USD'
            type='market')

        return sell_result

    def buy_market_value(self, funds_in_usd, coin_type):
        """
        Buys 'coin_type' in market value with USD. minimum USD =10 is required for the transaction
        :param funds_in_usd: Int, amount to buy in USD
        :param coin_type: type of coin: 'bitcoin', 'litecoin', bitcoincash', 'etherium'
        :return: result of buy
        """
        buy_result = self.auth_client.buy(
                    funds=funds_in_usd, #USD
                    product_id=self.gdax_helper.COIN_TO_USD_PRODUCT_ID[coin_type.lower()],#'LTC-USD'
                    type='market')
        return buy_result

    def get_account_available_amounts(self):
        """
        get avaialble amuunts of USD, bitcoin, litecoin, bitcoincash, etherium from account
        :return: dictionary consist of prodduct:amount pair.
        example: {'bitcoin': 1, 'usd': 2.2, 'litecoin': 3.12, 'bitcoincash': .01, 'etherium': 0.0002}
        """
        account_available_amounts = {}
        my_account_full = self.auth_client.get_accounts()

        for product_info in my_account_full:
            if product_info['currency'] == 'BTC':
                account_available_amounts['bitcoin'] = float(product_info['available'].encode('ascii', 'ignore'))
            if product_info['currency'] == 'USD':
                account_available_amounts['usd'] = float(product_info['available'].encode('ascii', 'ignore'))
            if product_info['currency'] == 'LTC':
                account_available_amounts['litecoin'] = float(product_info['available'].encode('ascii', 'ignore'))
            if product_info['currency'] == 'ETH':
                account_available_amounts['etherium'] = float(product_info['available'].encode('ascii', 'ignore'))
            if product_info['currency'] == 'BCH':
                account_available_amounts['bitcoincash'] = float(product_info['available'].encode('ascii', 'ignore'))

        return account_available_amounts






def main(argv):

    period = 1
    gdax_helper = GdaxHelper()
    gdax_trader = GdaxTrader()

    litecoin_price_at_buy_time = 160.21
    bitcoin_cash_price_at_buy_time = 979.38
    bitcoin_price_at_buy_time = 8521.00
    etherium_price_at_buy_time = 521.18
    usd = 52.60
    init_amount_of_litecoin_bought = 0.32733706
    selected_coin_to_buy = 'litecoin'

    price_ratio_at_buy_time = {}
    # Since we have litecoin in bank,I should buy/sell based on litecoin first
    price_ratio_at_buy_time['litecoin/bitcoincash'] = litecoin_price_at_buy_time/bitcoin_cash_price_at_buy_time
    price_ratio_at_buy_time['litecoin/etherium'] = litecoin_price_at_buy_time/etherium_price_at_buy_time
    price_ratio_at_buy_time['litecoin/bitcoin'] = litecoin_price_at_buy_time/bitcoin_price_at_buy_time

    price_ratio_at_buy_time['etherium/litecoin'] = etherium_price_at_buy_time/litecoin_price_at_buy_time
    price_ratio_at_buy_time['etherium/bitcoincash'] = etherium_price_at_buy_time/bitcoin_cash_price_at_buy_time
    price_ratio_at_buy_time['etherium/bitcoin'] = etherium_price_at_buy_time/bitcoin_price_at_buy_time

    price_ratio_at_buy_time['bitcoincash/litecoin'] = bitcoin_cash_price_at_buy_time/litecoin_price_at_buy_time
    price_ratio_at_buy_time['bitcoincash/etherium'] = bitcoin_cash_price_at_buy_time/etherium_price_at_buy_time
    price_ratio_at_buy_time['bitcoincash/bitcoin'] = bitcoin_cash_price_at_buy_time/bitcoin_price_at_buy_time

    price_ratio_at_buy_time['bitcoin/litecoin'] = bitcoin_price_at_buy_time/litecoin_price_at_buy_time
    price_ratio_at_buy_time['bitcoin/etherium'] = bitcoin_price_at_buy_time/etherium_price_at_buy_time
    price_ratio_at_buy_time['bitcoin/bitcoincash'] = bitcoin_price_at_buy_time/bitcoin_cash_price_at_buy_time
    print 'init price_ratio_at_buy_time:       ', price_ratio_at_buy_time
    initial_available_amounts_in_account =  gdax_trader.get_account_available_amounts()


    while True:
        time.sleep(int(period))

        # check all price ratios
        # pattern for selected coin is 'coin_name/*'
        # get a subset dictionary of all ratios for the coin we actually bought
        selected_coin_to_other_coins_initial_price_ratios_dict = dict(
            (key, value) for key, value in price_ratio_at_buy_time.items() if selected_coin_to_buy + '/' in key.lower())
        print 'Selected coin to other coins price at buy time: {}'.format(selected_coin_to_other_coins_initial_price_ratios_dict)

        for coin_to_coin_pair_name, initial_price_ratio_for_selected_coins in selected_coin_to_other_coins_initial_price_ratios_dict.iteritems():
            print 'contocoinpair: ' + coin_to_coin_pair_name
            current_price_ratios, current_individual_prices = gdax_helper.get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
            current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]

            # TODO: for now we are only looking at litecoin
            # put a margin on top of actual fee to make some profit!
            fee_coefficient = 1 - init_amount_of_litecoin_bought*(GDAX_FEE + BUY_SELL_MARGIN)

            # if this formula is true for coin1/coin2 need to sell coin1, and buy coin2
            if initial_price_ratio_for_selected_coins < current_price_ratio_for_selected_coins*fee_coefficient:
                print 'SELLLLL'
                # new coin to buy: selected_pair-'previous coin'
                # TODO: sell previous coin!
                selected_coin_to_buy = coin_to_coin_pair_name.replace(selected_coin_to_buy + '/', '')
                print 'New selected coin to buy: {}'.format(selected_coin_to_buy)
                #TODO: buy new coin!

                #TODO: put in a method?
                # update prices when bought
                price_ratio_at_buy_time['litecoin/bitcoincash'] = current_price_ratios['litecoin/bitcoincash']
                price_ratio_at_buy_time['litecoin/etherium'] = current_price_ratios['litecoin/etherium']
                price_ratio_at_buy_time['litecoin/bitcoin'] = current_price_ratios['litecoin/bitcoin']

                price_ratio_at_buy_time['etherium/litecoin'] = current_price_ratios['etherium/litecoin']
                price_ratio_at_buy_time['etherium/bitcoincash'] = current_price_ratios['etherium/bitcoincash']
                price_ratio_at_buy_time['etherium/bitcoin'] = current_price_ratios['etherium/bitcoin']

                price_ratio_at_buy_time['bitcoincash/litecoin'] = current_price_ratios['bitcoincash/litecoin']
                price_ratio_at_buy_time['bitcoincash/etherium'] = current_price_ratios['bitcoincash/etherium']
                price_ratio_at_buy_time['bitcoincash/bitcoin'] = current_price_ratios['bitcoincash/bitcoin']

                price_ratio_at_buy_time['bitcoin/litecoin'] = current_price_ratios['bitcoin/litecoin']
                price_ratio_at_buy_time['bitcoin/etherium'] = current_price_ratios['bitcoin/etherium']
                price_ratio_at_buy_time['bitcoin/bitcoincash'] = current_price_ratios['bitcoin/bitcoincash']


                break
            else:
                print 'no sel!!'

            print('------')
        print('=========')


if __name__ == "__main__":
    main(sys.argv[1:])