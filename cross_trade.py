import sys
import time

from gdax_helper import GdaxHelper

GDAX_FEE = 0.006  # 0.6 percent fee
BUY_SELL_MARGIN = 0.005  # 0.5 percent profit


def main(argv):
    period = 1
    gdax_helper = GdaxHelper()

    litecoin_initial_price = 160.21
    bitcoin_cash_initial_price = 979.38
    bitcoin_initial_price = 8521.00
    etherium_initial_price = 521.18
    usd = 52.60
    init_amount_of_litecoin_bought = 0.32733706
    selected_coin_to_buy = 'litecoin'

    initial_ratio = {}
    # Since we have litecoin in bank,I should buy/sell based on litecoin first
    initial_ratio['litecoin/bitcoincash'] = litecoin_initial_price/bitcoin_cash_initial_price
    initial_ratio['litecoin/etherium'] = litecoin_initial_price/etherium_initial_price
    initial_ratio['litecoin/bitcoin'] = litecoin_initial_price/bitcoin_initial_price

    initial_ratio['etherium/litecoin'] = etherium_initial_price/litecoin_initial_price
    initial_ratio['etherium/bitcoincash'] = etherium_initial_price/bitcoin_cash_initial_price
    initial_ratio['etherium/bitcoin'] = etherium_initial_price/bitcoin_initial_price

    initial_ratio['bitcoincash/litecoin'] = bitcoin_cash_initial_price/litecoin_initial_price
    initial_ratio['bitcoincash/etherium'] = bitcoin_cash_initial_price/etherium_initial_price
    initial_ratio['bitcoincash/bitcoin'] = bitcoin_cash_initial_price/bitcoin_initial_price

    initial_ratio['bitcoin/litecoin'] = bitcoin_initial_price/litecoin_initial_price
    initial_ratio['bitcoin/etherium'] = bitcoin_initial_price/etherium_initial_price
    initial_ratio['bitcoin/bitcoincash'] = bitcoin_initial_price/bitcoin_cash_initial_price

    while True:
        time.sleep(int(period))

        # check all price ratios
        # pattern for selected coin is 'coin_name/*'
        # get a subset dictionary of all ratios for the coin we actually bought
        selected_coin_to_other_coins_initial_price_ratios_dict = dict(
            (key, value) for key, value in initial_ratio.items() if selected_coin_to_buy + '/' in key.lower())
        print 'SSSselected_coin_to_other_coins_initial_price_ratios_dict:    ', selected_coin_to_other_coins_initial_price_ratios_dict

        for coin_to_coin_pair_name, initial_price_ratio_for_selected_coins in selected_coin_to_other_coins_initial_price_ratios_dict.iteritems():

            current_price_ratios, current_individual_prices = gdax_helper.get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
            current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]
            print 'init: ', coin_to_coin_pair_name
            print 'initial_price_ratio_for_selected_coins: ' , initial_price_ratio_for_selected_coins
            print 'current_individual_prices: ' , current_individual_prices

            # TODO: for now we are only looking at litecoin
            # put a margin on top of actual fee to make some profit!
            fee_coefficient = 1 - init_amount_of_litecoin_bought*(GDAX_FEE + BUY_SELL_MARGIN)
            print 'price_ratio_with_fee:   ', current_price_ratio_for_selected_coins*fee_coefficient


            print 'coin_to_coin_pair_name: ', coin_to_coin_pair_name
            if initial_price_ratio_for_selected_coins < current_price_ratio_for_selected_coins*fee_coefficient:
                print 'SELLLLL'
                # new coin to buy: selected_pair-'previous coin'
                # TODO: sell previous coin!
                selected_coin_to_buy = coin_to_coin_pair_name.replace(selected_coin_to_buy + '/', '')
                print 'new coin: ', selected_coin_to_buy
                #TODO: buy new coin!
                break
            else:
                print 'no sel!!'

            print('------')
        print('=========')


if __name__ == "__main__":
    main(sys.argv[1:])