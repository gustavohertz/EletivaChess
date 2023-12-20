import chessdotcom
import requests
from chessdotcom import get_leaderboards, get_player_stats
import pprint

printer = pprint.PrettyPrinter()

# Configurar o User-Agent
headers = {'User-Agent': 'My Python Application. Contact me at email@example.com'}
chessdotcom.Client.request_config['headers'] = headers

def print_leaderboards():
    response = requests.get('https://api.chess.com/pub/leaderboards', headers=headers)
  
    data = response.json()
    categories = data.keys()
    for category in categories:
        print('Category:', category)
        for idx, entry in enumerate(data[category]):
            print(f'Rank:{idx + 1}| UserName: {entry["username"]} |Rating: {entry["score"]}')

def get_player_rating(username):
    data = get_player_stats(username).json
    try:
        chess_bullet_data = data['stats']['chess_bullet']
        print('Categoria: chess_bullet')
        print(f'Rating atual: {chess_bullet_data["last"]["rating"]}')
        print(f'Maior rating: {chess_bullet_data["best"]["rating"]}')
    except KeyError as e:
        print(f"Erro ao obter dados de rating: {e}")

print_leaderboards()
get_player_rating("GustavoHertz")
