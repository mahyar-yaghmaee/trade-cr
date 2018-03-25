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

    initial_ratio = {}
    initial_ratio['litecoin/bitcoincash'] = litecoin_initial_price/bitcoin_cash_initial_price
    initial_ratio['litecoin/etherium'] = litecoin_initial_price/etherium_initial_price
    initial_ratio['litecoin/bitcoin'] = litecoin_initial_price/bitcoin_initial_price
    print( initial_ratio)

    while True:
        time.sleep(int(period))

        print '-------'
        # check all price ratios
        for coin_to_coin_pair_name, initial_price_ratio_for_selected_coins in initial_ratio.iteritems():
            current_price_ratios, current_individual_prices =  gdax_helper.get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
            current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]
            print 'init: ', coin_to_coin_pair_name,initial_price_ratio_for_selected_coins
            print 'current_price_ratio', current_price_ratio_for_selected_coins
            print 'current_individual_prices: ' , current_individual_prices
            print('========')

            # for now we are only looking at litecoin
            # #TODO: put a marigin for buy/sell
            # put a marigin on top of actual fee to make some profit!
            buy_sell_marigin = 0.005 #0.5 percent profit
            gdax_fee = 0.006 # 0.6 percent fee
            fee_coefficient = 1 - init_amount_of_litecoin_bought*(gdax_fee + buy_sell_marigin)
            print 'price_ratio_with_fee:   ', current_price_ratio_for_selected_coins*fee_coefficient

            if initial_price_ratio_for_selected_coins < current_price_ratio_for_selected_coins*fee_coefficient:
                print 'SELLLLL'
            else:
                print 'no sel!!'
            print('00000000000000')


if __name__ == "__main__":
    main(sys.argv[1:])