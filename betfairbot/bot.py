from flumine import Flumine, clients
from flumine.worker import BackgroundWorker
import betfairlightweight
from betfairlightweight.filters import streaming_market_filter
from strategies import BetfairBeacons
from dotenv import load_dotenv
from tradingroutines import terminate
import logging
import os

load_dotenv()

BETFAIR_USERNAME = os.getenv("BETFAIR_USERNAME")
BETFAIR_PASSWORD = os.getenv("BETFAIR_PASSWORD")
BETFAIR_APPKEY = os.getenv("BETFAIR_APPKEY_LIVE")

def setup_logging():
    # Configure logging + sets it up for the console
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # info level
    file_handler_info = logging.FileHandler('./logs/fluminebotinfo.log')
    file_handler_info.setLevel(logging.INFO)

    # warning level
    file_handler_warning = logging.FileHandler('./logs/fluminebotwarning.log')
    file_handler_warning.setLevel(logging.WARNING)

    # critical level
    file_handler_critical = logging.FileHandler('./logs/fluminebotcritical.log')
    file_handler_critical.setLevel(logging.CRITICAL)

    # defines the log format for the handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler_info.setFormatter(log_format)
    file_handler_warning.setFormatter(log_format)
    file_handler_critical.setFormatter(log_format)

    # add file handlers to the root logger
    logging.getLogger('').addHandler(file_handler_info)
    logging.getLogger('').addHandler(file_handler_warning)
    logging.getLogger('').addHandler(file_handler_critical)

# activate logging
setup_logging()
logger = logging.getLogger(__name__)

trading = betfairlightweight.APIClient(
                    username=BETFAIR_USERNAME,
                    password=BETFAIR_PASSWORD,
                    app_key=BETFAIR_APPKEY,
                    )

trading.login_interactive()

betfairclient = clients.BetfairClient(betting_client=trading, interactive_login=True)
framework = Flumine(client=betfairclient)

beacon_strategy = BetfairBeacons(
    market_filter=streaming_market_filter(
        event_type_ids=["7"],
        country_codes=["UK"],
        market_types=["WIN"],
    ), 
    market_data_filter={}, 
    max_selection_exposure=100, 
    max_order_exposure=50,
    max_trade_count=5,
    max_live_trade_count=5,
)

# equip the framework with our BetfairBeacons strategy
framework.add_strategy(beacon_strategy)

# add termination info to the framework (quit 23:00 each day)
framework.add_worker(
        BackgroundWorker(
            framework,
            terminate,
            func_kwargs={'time_to_quit': '23:00'},
            interval=60,
            start_delay=10,
        )
    )

logger.info("Launching Flumine Instance")

framework.run()