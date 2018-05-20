import sys
import time
import logging
import gdax
import os
import datetime

from gdax_helper import GdaxHelper

GDAX_FEE = 0.006  # 0.6 percent fee
BUY_SELL_MARGIN = 0.004  # 0.2 percent profit >>>> NOTE: We round down amount to buy/sell 0.01. see if it affect this


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

    def get_price_ratios_at_buy_time(self,
                               litecoin_price_at_buy_time, bitcoin_cash_price_at_buy_time,
                               etherium_price_at_buy_time, bitcoin_price_at_buy_time):
        """
        get price ratios at buy time, based on initial values
        :return: dictionary consisting the ratios of al coin-to-coins
        """
        price_ratio_at_buy_time = {}
        price_ratio_at_buy_time['litecoin/bitcoincash'] = litecoin_price_at_buy_time / bitcoin_cash_price_at_buy_time
        price_ratio_at_buy_time['litecoin/etherium'] = litecoin_price_at_buy_time / etherium_price_at_buy_time
        price_ratio_at_buy_time['litecoin/bitcoin'] = litecoin_price_at_buy_time / bitcoin_price_at_buy_time

        price_ratio_at_buy_time['etherium/litecoin'] = etherium_price_at_buy_time / litecoin_price_at_buy_time
        price_ratio_at_buy_time['etherium/bitcoincash'] = etherium_price_at_buy_time / bitcoin_cash_price_at_buy_time
        price_ratio_at_buy_time['etherium/bitcoin'] = etherium_price_at_buy_time / bitcoin_price_at_buy_time

        price_ratio_at_buy_time['bitcoincash/litecoin'] = bitcoin_cash_price_at_buy_time / litecoin_price_at_buy_time
        price_ratio_at_buy_time['bitcoincash/etherium'] = bitcoin_cash_price_at_buy_time / etherium_price_at_buy_time
        price_ratio_at_buy_time['bitcoincash/bitcoin'] = bitcoin_cash_price_at_buy_time / bitcoin_price_at_buy_time

        price_ratio_at_buy_time['bitcoin/litecoin'] = bitcoin_price_at_buy_time / litecoin_price_at_buy_time
        price_ratio_at_buy_time['bitcoin/etherium'] = bitcoin_price_at_buy_time / etherium_price_at_buy_time
        price_ratio_at_buy_time['bitcoin/bitcoincash'] = bitcoin_price_at_buy_time / bitcoin_cash_price_at_buy_time
        return price_ratio_at_buy_time

    def update_price_ratios_at_buy_time_based_on_current_ratios(self, price_ratio_at_buy_time, current_price_ratios):
        """
        update the dictionary for coin-to-coin prices, based on currecnt prices (at but time)
        :return: dictionary consisting updated values for coin-to-coin ratios
        """
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

        return price_ratio_at_buy_time


def main(argv):

    # Todo :get initial price and ratios regarding the fee I paid (market fee)
    period = 1
    gdax_helper = GdaxHelper()
    gdax_trader = GdaxTrader()
    no_of_sell_or_buys = 0

    litecoin_price_at_buy_time = 136.38
    bitcoin_cash_price_at_buy_time = 779.8
    bitcoin_price_at_buy_time = 8138.82
    etherium_price_at_buy_time = 517.80
    usd = 38.62
   # litecooin_amount_of_coin_bought = 0.25734077
   # bitcoin_amount_at_buy_time = 0.00405080
    bitcoin_amount = 0.0040327174740541
   # eth_amount = 0.06376998
    # TODO: MAKE SURE TO GEt THIS AS ARGUMENT!!!!!!!! <<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>
    selected_coin_to_buy = 'bitcoin'

    price_ratio_at_buy_time = gdax_trader.get_price_ratios_at_buy_time(
        litecoin_price_at_buy_time=litecoin_price_at_buy_time,
        bitcoin_cash_price_at_buy_time=bitcoin_cash_price_at_buy_time,
        etherium_price_at_buy_time=etherium_price_at_buy_time,
        bitcoin_price_at_buy_time=bitcoin_price_at_buy_time)

    account_available_amounts_at_buy_time = gdax_trader.get_account_all_products_available_amounts()

    result_file_name = 'buy_result.txt'

    # Remove the file if already exist, to ignore previous results
    try:
        os.remove(result_file_name)
    except OSError:
        pass

    with open(result_file_name, 'a') as result_file:

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
                print 'coin_to_coin_pair_name: ' , coin_to_coin_pair_name
                print 'initial_price_ratio_for_selected_coins: ', initial_price_ratio_for_selected_coins

                # 1- get current coin to other coins ratio
                current_price_ratios, current_individual_prices = gdax_helper.\
                    get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
                print 'current_price_ratios: ' , current_price_ratios
                print 'coin_to_coin_pair_name: ', coin_to_coin_pair_name
                current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]

                print 'current_price_ratio_for_selected_coins:  ', current_price_ratio_for_selected_coins

                # put a margin on top of actual fee to make some profit!
                fee_coefficient = 1 - (GDAX_FEE + BUY_SELL_MARGIN)
                print 'fee_coefficient: ' , fee_coefficient
               # fee_coefficient = 1 - amount_of_coin_bought * (GDAX_FEE + BUY_SELL_MARGIN)
                print 'current_price_ratio_for_selected_coins*fee_coefficient: ', current_price_ratio_for_selected_coins*fee_coefficient
                print 'initial_price_ratio_for_selected_coins:   ', initial_price_ratio_for_selected_coins

                # 2- if this formula is true for coin1/coin2 need to sell coin1, and buy coin2
                if initial_price_ratio_for_selected_coins < current_price_ratio_for_selected_coins*fee_coefficient:
                    # 2.a - round down 0.01 of coin to be able to sell sometimes gdax has error , mnostly with doller!)
                    # TODO: llook at this!
                    result_file.write('initial_price_ratio_for_selected_coins: {}\n'.format(initial_price_ratio_for_selected_coins))
                    result_file.write('current_price_ratio_for_selected_coins: {}\n'.format(current_price_ratio_for_selected_coins))
                    result_file.write('current_price_ratio_for_selected_coins*fee_coefficient: {}\n'.format(current_price_ratio_for_selected_coins*fee_coefficient))

                    amount_coin_to_sell = float(account_available_amounts_at_buy_time[coin_to_sell])
                    amount_coin_to_sell_rounded_down = round(amount_coin_to_sell - 0.00000001, 8)
                    print 'SEL {} in amount of {}'.format(coin_to_sell, amount_coin_to_sell_rounded_down)

                    # 2.a - Sell the product (coin1) with market value
                    sell_result = gdax_trader.sell_market_value(
                        size_to_sell_coin_size=amount_coin_to_sell_rounded_down,
                        coin_type=coin_to_sell
                    )
                    print 'Result of Sell: {} '.format(sell_result)

                    # 2.b - Buy coin2 in market value
                    # new coin to buy: selected_pair-'previous coin'
                    selected_coin_to_buy = coin_to_coin_pair_name.replace(selected_coin_to_buy + '/', '')
                    print 'New selected coin to buy: {}'.format(selected_coin_to_buy)

                    # 2.c update account avaialble amount sto to how much USD we have
                    account_available_amounts_at_buy_time = gdax_trader.get_account_all_products_available_amounts()

                    # 2.d - need to round down 0.01$ so we can buy, gdax can not buy for example 3.123124124125$
                    amount_in_usd_to_buy = float(account_available_amounts_at_buy_time['usd'])
                    amount_in_usd_to_buy_round_down_two_digits = round(amount_in_usd_to_buy - 0.01, 2)
                    print 'BUY {} for {} USD'.format(coin_to_buy, amount_in_usd_to_buy_round_down_two_digits)

                    buy_result = gdax_trader.buy_market_value(coin_type=coin_to_buy,
                                                 funds_in_usd=amount_in_usd_to_buy_round_down_two_digits)

                    print 'Result of Buy: {} '.format(buy_result)

                    #TODO: put in a method?
                    # 2.e - Update Account amounts after buying
                    account_available_amounts_at_buy_time = gdax_trader.get_account_all_products_available_amounts()

                    # 2.f - update prices when bought, to be used for future buys
                    price_ratio_at_buy_time = gdax_trader.update_price_ratios_at_buy_time_based_on_current_ratios(
                        price_ratio_at_buy_time, current_price_ratios)

                    print 'Prices at buy/Sell time {}'.format(datetime.datetime.now())
                    print 'Price ratio at buy time:  {}'.format(price_ratio_at_buy_time)
                    result_file.write('Prices at buy/Sell time {}\n'.format(datetime.datetime.now()))
                    result_file.write('Price ratio at buy time:  {}\n'.format(price_ratio_at_buy_time))
                    result_file.write('account_available_amounts_at_buy_time: {}\n'.format(account_available_amounts_at_buy_time))
                    result_file.write('Prices at buy time: {}\n'.format(current_individual_prices))

                    print 'Prices price_ratio_at_buy_time at buy time: {}'.format(price_ratio_at_buy_time)

                    amount_of_coin_bought = gdax_trader.get_account_all_products_available_amounts()[coin_to_buy]
                    print 'Amount bought of {} is {}: '.format(coin_to_buy, amount_of_coin_bought)
                    no_of_sell_or_buys += 1
                    print('Number of Sell/buys: ', no_of_sell_or_buys)
                    print '----------------'

                    # 2.g sleep for transaction
                    time.sleep(1)
                    result_file.write('no_of_sell_or_buys: {}\n'.format(no_of_sell_or_buys))
                    result_file.write('------------------\n')

                    # 2.f break the loop to go to newcoin/othercoins ratio
                    break
                else:
                    print 'no sel!!'
                    print '-----'


if __name__ == "__main__":
    main(sys.argv[1:])