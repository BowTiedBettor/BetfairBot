import flumine
from flumine import BaseStrategy
from flumine.order.trade import Trade
from flumine.order.order import LimitOrder
from flumine.markets.market import Market
from betfairlightweight.resources import MarketBook
from tradingroutines import update_anchor_prices, send_to_telegram
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class BetfairBeacons(BaseStrategy):
    def start(self, flumine) -> None:
        """
        Executed at launch of The Strategy
        """
        logger.info("Starting Strategy 'BetfairBeacons'")

    def check_market_book(self, market: Market, market_book: MarketBook) -> bool:
        """
        Checks basic Race & MarketBook info to decide whether the market should be processed or not.
        """
        market_catalogue = market.market_catalogue
        if market_catalogue is None:
            # wait for flumine to fetch market catalogues
            return False
        
        return True

    def process_market_book(self, market: Market, market_book: MarketBook) -> None:
        """
        Processes Order Book updates if the MarketBook passed the check_market_book filter above
        
        Loops through each runner, ignores scratched horses
        Continously checks for new anchor prices & sends 'threshold orders' as they [the anchor prices] arrive/are determined
        Before initializing a trade it verifies that there isn't a trade for the horse in the blotter already

        Order reports are automatically sent to an Order Report Channel
        """
        market_catalogue = market.market_catalogue
        post_time = market_catalogue.market_start_time.strftime("%H:%M")

        logger.info(f"Processing Market Book - {market_catalogue.event.name} - {market_catalogue.market_name} - {post_time}")
        for runner_book, runner_info in zip(market_book.runners, market.market_catalogue.runners):
            # skip scratched horses
            if runner_book.status != 'ACTIVE':
                continue

            updated_anchor_prices = update_anchor_prices(current_anchor_prices=self.context['anchor_prices'], 
                                                         runner_book_ex=runner_book.ex, 
                                                         historical_trades=runner_book.ex.traded_volume, 
                                                         )
            self.context['anchor_prices'] = updated_anchor_prices

            try:
                anchor_price = self.context['anchor_prices'][runner_book.selection_id]
            except KeyError:
                # no anchor price determined yet for the horse
                continue
            else:
                trades = self.get_runner_context(market_book.market_id, runner_book.selection_id, handicap=runner_book.handicap).trades
                upper_threshold_price = anchor_price * 1.075
                lower_threshold_price = anchor_price * 0.925

                if len(trades) == 0: 
                    # initialize a Trade by sending 'threshold orders' to Betfair
                    # ...

                    # log & send information
                    trade_info = """ ... """
                    logger.info(f"Trade Initialized - {market_catalogue.event.name} - {market_catalogue.market_name} - {post_time} - {runner_info.runner_name} - {runner_book.selection_id}")
                    send_to_telegram(message=trade_info,
                                     bot_token="", 
                                     channel="", 
                                     markdown=False)
                    pass
                
                else:
                    # monitor where the current price is & adjust orders accordingly
                    # ...
                    pass
            
    def process_orders(self, market: Market, orders: list) -> None:
        """
        Loops through & handles all orders
        """
        market_catalogue = market.market_catalogue
        if market_catalogue is None:
            # wait for flumine to fetch market catalogues
            processing_orders = False
        else:
            processing_orders = True
            post_time = market_catalogue.market_start_time.strftime("%H:%M")

        if processing_orders:
            for order in orders:
                if not order.complete:
                    relevant_trade = order.trade
                    trade_orders = relevant_trade.orders
                    # either implement the removal of outstanding orders/closure of the trade here 
                    # [or potentially better in process_market_book at say 15 mins to post]
                    pass

                else:
                    continue