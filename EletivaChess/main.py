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


def get_games_with_opening_info(username,year=2023,num_games=50):
    try:
        # Obtendo dados dos arquivos de jogos mensais de novembro
        archives_url = f'https://api.chess.com/pub/player/{username}/games/archives'
        archives_response = requests.get(archives_url, headers=headers)
        archives_data = archives_response.json()

        # Encontrando o URL do arquivo do mês de novembro
        november_archive_url = next((url for url in archives_data['archives'] if f'/games/{year}' in url), None)

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


    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados dos jogos: {e}")

def calculate_opening_win_percentage(username, year=2023, month=11, num_games=30):
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
                opening_stats = {}  # Dicionário para armazenar estatísticas de aberturas

                for i, game in enumerate(november_games_data['games'][:num_games]):
                    # Analisando a notação PGN para obter informações sobre a abertura
                    pgn = chess.pgn.read_game(StringIO(game["pgn"]))
                    eco_url = pgn.headers.get("ECOUrl")

                    # Obtendo o resultado da partida
                    result = game.get('result', 'N/A')

                    # Atualizando estatísticas de aberturas
                    if eco_url and result in ['1-0', '0-1']:
                        opening_stats[eco_url] = opening_stats.get(eco_url, {'wins': 0, 'total': 0})
                        opening_stats[eco_url]['total'] += 1
                        if result == '1-0':
                            opening_stats[eco_url]['wins'] += 1

                # Calculando e imprimindo porcentagens de vitória por abertura
                print('Porcentagem de Vitória por Abertura:')
                for eco_url, stats in opening_stats.items():
                    win_percentage = (stats['wins'] / stats['total']) * 100
                    print(f'{eco_url}: {win_percentage:.2f}% (Total de Jogos: {stats["total"]})')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados dos jogos: {e}")

# Exemplo de uso
calculate_opening_win_percentage("GMKrikor",year=2023, month=11, num_games=30)

#get_player_rating("GMKrikor")
#get_games_with_opening_info("GMKrikor",year=2023,num_games=50)
