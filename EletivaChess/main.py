import chessdotcom
import requests
import chess
import chess.pgn
from chessdotcom import get_player_stats, get_player_game_archives
from io import StringIO

headers = {'User-Agent': 'My Python Application. Contact me at email@example.com'}
chessdotcom.Client.request_config['headers'] = headers


def get_player_rating(username):
    data = get_player_stats(username).json
    try:
        chess_bullet_data = data['stats']['chess_bullet']
        print('Categoria: chess_bullet')
        print(f'Rating atual: {chess_bullet_data["last"]["rating"]}')
        print(f'Maior rating: {chess_bullet_data["best"]["rating"]}')
        print(f'Maior rating: {chess_bullet_data["record"]}')
    except KeyError as e:
        print(f"Erro ao obter dados de rating: {e}")

def get_last_played_games(username):
    try:
        # Obtendo dados dos jogos atuais
        current_games_url = f'https://api.chess.com/pub/player/{username}/games'
        current_games_response = requests.get(current_games_url, headers=headers)
        current_games_data = current_games_response.json()

        # Verificando se há jogos atuais
        if current_games_data.get('games'):
            print('Jogos Atuais:')
            for game in current_games_data['games']:
                print(f'URL do Jogo: {game["url"]}')
                print(f'Movimentos (PGN): {game["pgn"]}')
                print(f'Regras: {game["rules"]}')
                print(f'Tempo de Controle: {game["time_control"]}')
                print('---')

        # Obtendo dados dos jogos onde é a vez do jogador
        to_move_games_url = f'https://api.chess.com/pub/player/{username}/games/to-move'
        to_move_games_response = requests.get(to_move_games_url, headers=headers)
        to_move_games_data = to_move_games_response.json()

        # Verificando se há jogos onde é a vez do jogador
        if to_move_games_data.get('games'):
            print('Jogos onde é a vez do jogador:')
            for game in to_move_games_data['games']:
                print(f'URL do Jogo: {game["url"]}')
                print(f'Movimentos (PGN): {game["pgn"]}')
                print(f'Draw Offer: {game.get("draw_offer", False)}')
                print('---')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados dos jogos: {e}")


def get_games_with_opening_info(username,year=2023, month=11, num_games=5):
    try:
        # Obtendo dados dos arquivos de jogos mensais de novembro
        archives_url = f'https://api.chess.com/pub/player/{username}/games/archives'
        archives_response = requests.get(archives_url, headers=headers)
        archives_data = archives_response.json()

        # Encontrando o URL do arquivo do mês de novembro
        november_archive_url = next((url for url in archives_data['archives'] if f'/games/{year}/{month}' in url), None)

        # Verificando se o arquivo de novembro foi encontrado
        if november_archive_url:
            november_games_response = requests.get(november_archive_url, headers=headers)
            november_games_data = november_games_response.json()

            # Verificando se há jogos
            if november_games_data.get('games'):
                print(f'Últimos {num_games} jogos de novembro com informações de abertura:')
                count = 0
                for i, game in enumerate(november_games_data['games']):
                    if count >= num_games:
                        break
                    
                    # Analisando a notação PGN para obter informações sobre a abertura
                    pgn = chess.pgn.read_game(StringIO(game["pgn"]))
                    eco_url = pgn.headers.get("ECOUrl")
                    if eco_url:
                        count += 1
                        print(f'\nJogo {count}:')
                        print(f'URL do Jogo: {game["url"]}')
                        print(f'Movimentos (PGN): {game["pgn"]}')
                        print(f'ECO URL da Abertura: {eco_url}')
                        # Obtendo o resultado da partida
                        result = game.get('result', 'N/A')
                        print(f'Resultado da Partida: {result}')
                        print('---')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados dos jogos: {e}")

get_player_rating("GMKrikor")
get_last_played_games("GMKrikor")
get_games_with_opening_info("GMKrikor",year=2023, month=11, num_games=5)
