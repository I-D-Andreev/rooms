import random
import string
from datetime import datetime

class UniqueCode:
    @staticmethod
    def generate_unique_code(random_part_length = 10): 
        now = datetime.now().astimezone()
        timestamp = now.strftime("%d%M%S")
        string_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range (random_part_length))

        return (string_code + timestamp)
