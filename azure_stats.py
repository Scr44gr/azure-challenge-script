__author__ = 'Scr44gr'
from requests import get
from typing import Dict, List
from sys import stdout

UUID : str = "2cceec57-42f9-4350-8b82-1fc4fe0034fa"
URL : str = f"https://docs.microsoft.com/api/challenges/{UUID}/leaderboard"
OK : int = 200
WIN_SCORE : int = 17

def get_challenge_data(top: int, **kwargs) -> Dict:

    data = {'$top':top}
    if ((skip:=kwargs.get('skip'))):
      data.update({'$skip':skip})

    r = get(URL, params=data)

    if r.status_code == OK:
        return r.json()

def get_leaderboard(data: List) -> Dict:
    users_completed_challenge = {}

    for user in data:
        if user['score'] == WIN_SCORE:
            username = user['userDisplayName']
            rank = user['rank']
            users_completed_challenge[username] = {'name':username, 'rank':rank}
    return users_completed_challenge

def main() -> None:
    top : int = 50
    count = get_challenge_data(0)['count']
    users = []
    for skip in range(0, count, top):
        data = get_challenge_data(top, skip=skip)
        users += data['results']
        if users[-1]['score'] < WIN_SCORE: break

    leaderboard = get_leaderboard(users)
    total = len(leaderboard)
    print(f'TOTAL DE USUARIOS QUE HAN COMPLETADO EL RETO: {total}')

if __name__ == '__main__':
    main()
