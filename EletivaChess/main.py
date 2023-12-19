import requests
from chessdotcom import get_leaderboards
import pprint

printer = pprint.PrettyPrinter()

def print_leaderboards():
    user_agent = 'My Python Application. Contact me at gustavo.hertz@al.infnet.edu.br'
    
    headers = {'User-Agent': 'chess.com analysis app / contact: gustavo.hertz@al.infnet.edu.br'}
    response = requests.get('https://api.chess.com/pub/leaderboards', headers=headers)
  
    data = response.json()
    categories = data.keys()
    for category in categories:
            print('Category:',category)
            for idx, entry in enumerate(data[category]):
                print(f'Rank:{idx + 1}| UserName: {entry["username"]} |Rating: {entry["score"]}')
 
print_leaderboards()