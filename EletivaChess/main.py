import chessdotcom
import requests
import chess
import chess.pgn
from chessdotcom import get_player_stats, get_player_game_archives
from io import StringIO

headers = {'User-Agent': 'My Python Application. Contact me at email@example.com'}
chessdotcom.Client.request_config['headers'] = headers

def calculate_opening_win_percentage(username, month=11, num_games=30):
    try:
        archives_url = f'https://api.chess.com/pub/player/{username}/games/archives'
        archives_response = requests.get(archives_url, headers=headers)
        archives_data = archives_response.json()

        year = archives_data.get('archives')[-1].split('/')[-2]

        november_archive_url = next((url for url in archives_data['archives'] if f'/games/{year}/{month}' in url), None)

        if november_archive_url:
            november_games_response = requests.get(november_archive_url, headers=headers)
            november_games_data = november_games_response.json()

            if november_games_data.get('games'):
                opening_stats = {}

                for i, game in enumerate(november_games_data['games'][:num_games]):
                    print(f'\nAnalisando Jogo {i + 1}...')

                    pgn = chess.pgn.read_game(StringIO(game["pgn"]))
                    eco_url = pgn.headers.get("ECOUrl")

                    if not eco_url:
                        board = pgn.board()
                        for move in pgn.mainline_moves():
                            board.push(move)
                            eco_url = board.variation_san([move])[0]
                            if eco_url:
                                break

                    print(f'ECO URL da Abertura: {eco_url}')

                    board = pgn.end().board()
                    result = board.result(claim_draw=True)
                    print(f'Resultado da Partida: {result}')

                    if eco_url and result != "1/2-1/2":
                        opening_stats[eco_url] = opening_stats.get(eco_url, {'wins': 0, 'losses': 0, 'total': 0})
                        opening_stats[eco_url]['total'] += 1
                        if result == "1-0":
                            opening_stats[eco_url]['wins'] += 1
                        elif result == "0-1":
                            opening_stats[eco_url]['losses'] += 1

                print('\nPorcentagem de Vitória por Abertura:')
                for eco_url, stats in opening_stats.items():
                    win_percentage = (stats['wins'] / stats['total']) * 100
                    print(f'{eco_url}: {win_percentage:.2f}% (Total de Jogos: {stats["total"]})')

    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados dos jogos: {e}")

calculate_opening_win_percentage("GMKrikor", month=11, num_games=50)
