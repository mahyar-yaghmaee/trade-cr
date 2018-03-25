import sys
import time
import logging

from gdax_helper import GdaxHelper

GDAX_FEE = 0.006  # 0.6 percent fee
BUY_SELL_MARGIN = 0.005  # 0.5 percent profit


def main(argv):
    period = 1
    gdax_helper = GdaxHelper()

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

    while True:
        time.sleep(int(period))

        # check all price ratios
        # pattern for selected coin is 'coin_name/*'
        # get a subset dictionary of all ratios for the coin we actually bought
        selected_coin_to_other_coins_initial_price_ratios_dict = dict(
            (key, value) for key, value in price_ratio_at_buy_time.items() if selected_coin_to_buy + '/' in key.lower())
        print 'Selected coin to other coins price at buy time: {}'.format(selected_coin_to_other_coins_initial_price_ratios_dict)

        for coin_to_coin_pair_name, initial_price_ratio_for_selected_coins in selected_coin_to_other_coins_initial_price_ratios_dict.iteritems():

            current_price_ratios, current_individual_prices = gdax_helper.get_current_coin_to_coin_price_ratio_for_all_coins_and_individual_prices()
            current_price_ratio_for_selected_coins = current_price_ratios[coin_to_coin_pair_name]

            # TODO: for now we are only looking at litecoin
            # put a margin on top of actual fee to make some profit!
            fee_coefficient = 1 - init_amount_of_litecoin_bought*(GDAX_FEE + BUY_SELL_MARGIN)

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