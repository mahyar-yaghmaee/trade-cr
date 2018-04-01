import sys
import time
import logging
import gdax
import os
import datetime

from gdax_helper import GdaxHelper

GDAX_FEE = 0.006  # 0.6 percent fee
BUY_SELL_MARGIN = 0.003  # 0.3 percent profit >>>> NOTE: We round down amount to buy/sell 0.01. see if it affect this


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

    def get_account_all_products_available_amounts(self):
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

    # Todo :get initial price and ratios regarding the fee I paid (market fee)
    period = 1
    gdax_helper = GdaxHelper()
    gdax_trader = GdaxTrader()
    no_of_sell_or_buys = 0

    litecoin_price_at_buy_time = 114.86
    bitcoin_cash_price_at_buy_time = 649.00
    bitcoin_price_at_buy_time = 6833.00
    etherium_price_at_buy_time = 381.76
    usd = 38.62
    init_amount_of_coin_bought = 0.3348216
    # TODO: MAKE SURE TO GEt THIS AS ARGUMENT!!!!!!!! <<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>
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
    account_available_amounts_at_buy_time = gdax_trader.get_account_all_products_available_amounts()

    while True:
        time.sleep(int(period))

        # check all price ratios
        # pattern for selected coin is 'coin_name/*'
        # get a subset dictionary of all ratios for the coin we actually bought
        selected_coin_to_other_coins_initial_price_ratios_dict = dict(
            (key, value) for key, value in price_ratio_at_buy_time.items() if selected_coin_to_buy + '/' in key.lower())
        print 'Selected coin to other coins price at buy time: {}'.\
            format(selected_coin_to_other_coins_initial_price_ratios_dict)

        # go over the all permutations of the current coin Vs other coins to find out if
        # cur_coin(t1)/other_ones(t1) < cur_coin(t2)/other_ones(t2)
        for coin_to_coin_pair_name, initial_price_ratio_for_selected_coins in \
                selected_coin_to_other_coins_initial_price_ratios_dict.iteritems():
            coin_to_sell, coin_to_buy = coin_to_coin_pair_name.split("/")  # split based on / for coin1/coin2

            # 1- get current coin to other coins ratio
            current_price_ratios, current_individual_prices = gdax_helper.\
                get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
            current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]

            # put a margin on top of actual fee to make some profit!
            fee_coefficient = 1 - init_amount_of_coin_bought*(GDAX_FEE + BUY_SELL_MARGIN)

            # 2- if this formula is true for coin1/coin2 need to sell coin1, and buy coin2
            if initial_price_ratio_for_selected_coins < current_price_ratio_for_selected_coins*fee_coefficient:
                print 'SEL!'
                # 2.a - round down 0.01 of coin to be able to sell sometimes gdax has error , mnostly with doller!)
                # TODO: llook at this!
                amount_coin_to_sell = account_available_amounts_at_buy_time[coin_to_sell]
                amount_coin_to_sell_rounded_down = round(amount_coin_to_sell - 0.01)
                # 2.a - Sell the product (coin1) with market value
                gdax_trader.sell_market_value(
                    size_to_sell_coin_size=amount_coin_to_sell_rounded_down,
                    coin_type=coin_to_sell
                )

                # 2.b - Buy coin2 in market value
                # new coin to buy: selected_pair-'previous coin'
                print 'BUY!'
                selected_coin_to_buy = coin_to_coin_pair_name.replace(selected_coin_to_buy + '/', '')
                print 'New selected coin to buy: {}'.format(selected_coin_to_buy)

                # 2.c - need to round down 0.01$ so we can buy, gdax can not buy for example 3.123124124125$
                amount_in_usd_to_buy = account_available_amounts_at_buy_time[coin_to_buy]
                amount_in_usd_to_buy_round_down_two_digits = round(amount_in_usd_to_buy - 0.01)

                account_available_amounts_at_buy_time = gdax_trader.get_account_all_products_available_amounts()
                gdax_trader.buy_market_value(coin_type=coin_to_buy,
                                             funds_in_usd=amount_in_usd_to_buy_round_down_two_digits)

                #TODO: put in a method?
                # 2.d - update prices when bought, to be used for future buys
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

                print 'Prices at buy/Sell time {}'.format(datetime.datetime.now())
                print 'litecoin/bitcoincash  : ', price_ratio_at_buy_time['litecoin/bitcoincash']
                print 'litecoin/etherium     : ', price_ratio_at_buy_time['litecoin/etherium']
                print 'litecoin/bitcoin      : ', price_ratio_at_buy_time['litecoin/bitcoin']
                print 'etherium/litecoin     : ', price_ratio_at_buy_time['etherium/litecoin']
                print 'etherium/bitcoincash  : ', price_ratio_at_buy_time['etherium/bitcoincash']
                print 'etherium/bitcoin      : ', price_ratio_at_buy_time['etherium/bitcoin']
                print 'bitcoincash/litecoin  : ', price_ratio_at_buy_time['bitcoincash/litecoin']
                print 'bitcoincash/etherium  : ',price_ratio_at_buy_time['bitcoincash/etherium']
                print 'bitcoincash/bitcoin   : ',price_ratio_at_buy_time['bitcoincash/bitcoin']
                print 'bitcoin/litecoin      : ',price_ratio_at_buy_time['bitcoin/litecoin']
                print 'bitcoin/etherium      : ',price_ratio_at_buy_time['bitcoin/etherium']
                print 'bitcoin/bitcoincash   : ',price_ratio_at_buy_time['bitcoin/bitcoincash']

                print 'Amount bought of {} is {}: '.format(coin_to_buy, gdax_trader.
                                                           get_account_all_products_available_amounts()[coin_to_buy])
                no_of_sell_or_buys += 1
                print('Number of Sell/buys: ', no_of_sell_or_buys)
                print '----------------'

                break
            else:
                print 'no sel!!'


if __name__ == "__main__":
    main(sys.argv[1:])