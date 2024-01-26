# Betfair Betting Bot
An example project illustrating how to build & deploy a trading bot at Betfair. Built in [Flumine](https://github.com/betcode-org/flumine).

More information available at [BowTiedBettor - Building & Deploying a Betfair Bot](https://www.blog.bowtiedbettor.com/p/building-and-deploying-a-betfair).

# Idea/Angle
Exploit the new 'Betfair Price Beacon'-feature. [Beacon FAQ](https://support.betfair.com/app/answers/detail/a_id/10315/).

# Code Design
- tradingroutines.py contains necessary/helpful functions, for instance **update_anchor_prices**.

- **strategies.py** defines & implements the strategy.

- **bot.py** sets required parameters & launches the bot.

# Strategy Design
Detailed breakdown available at [BowTiedBettor - Building & Deploying a Betfair Bot](https://www.blog.bowtiedbettor.com/p/building-and-deploying-a-betfair).

# How To Get It Up & Running
1. Clone the repo. 
2. pip install -r requirements.txt.
3. Add a /logs directory & a .env file. Define BETFAIR_USERNAME, BETFAIR_PASSWORD & BETFAIR_APPKEY_LIVE in the .env file.
4. Launch the bot.py program.
