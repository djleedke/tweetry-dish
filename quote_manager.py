
from quotes import quotes
import random

class QuoteManager:

    def __init__(self):
        print('Quote Manager: Initialized')
        self.current_quote = self.get_random_quote()

        
    def get_random_quote(self):
        return quotes[random.randint(0, len(quotes)-1)]

        
