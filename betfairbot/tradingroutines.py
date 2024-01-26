import flumine
from flumine.events.events import TerminationEvent
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

def update_anchor_prices(current_anchor_prices: dict, runner_book_ex, historical_trades) -> dict:
    """
    Takes a dict of anchor prices & returns an updated version [append-only]
    """
    pass

# Function that stops the Flumine Instance at the end of the day
def terminate(context: dict, flumine, time_to_quit: str) -> None:
    """
    Terminate Framework if past 'time to quit'.
    """
    now = datetime.now().time()
    datetime_to_quit = datetime.strptime(time_to_quit, '%H:%M').time()

    if now > datetime_to_quit:
        logger.info("Flumine Bot done for the day, shutting down processes & terminating the Framework...")
        flumine.handler_queue.put(TerminationEvent(flumine))

def send_to_telegram(message, bot_token, channel, markdown=False):
    """
    Posts a message in a Telegram Channel
    """
    apiToken = bot_token
    chatID = channel
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        if not markdown: 
            response = requests.post(apiURL, json={'chat_id': chatID, 
                                                'text': message, 
                                                'disable_web_page_preview': True, 
                                                }).json()
            return response['ok']
        else: 
            response = requests.post(apiURL, json={'chat_id': chatID, 
                                                'text': message, 
                                                'disable_web_page_preview': True,
                                                'parse_mode': 'Markdown',
                                                }).json()
            return response['ok']
    except: 
        return False
