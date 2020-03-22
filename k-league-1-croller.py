from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymssql

DB_SERVER = ""
DB_PORT = ""
DB_USER = ""
DB_PASSWORD = ""
DB_DATABASE = ""


# DB 저장
def insert_football_game_data(G_ID, G_DT, H_T_ID, A_T_ID):
    conn = pymssql.connect(server=DB_SERVER, port=DB_PORT, user=DB_USER, password=DB_PASSWORD,
                           database=DB_DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO FOOTBALL_GAME (LE_ID, SR_ID, G_ID, SEASON_ID, G_DT, H_T_ID, A_T_ID, STATUS_CD) ' +
                   f"VALUES(1, 0 , '{G_ID}', 2020, '{G_DT}', '{H_T_ID}', '{A_T_ID}', 0)")
    conn.commit()
    conn.close()


teams = {
    '수원' : 'SW',
    '울산' : 'US',
    '전북' : 'JB',
    '상주' : 'SJ',
    '대구' : 'DG',
    '성남' : 'SN',
    '광주' : 'GJ',
    '부산' : 'BS',
    '인천' : 'IC',
    '포항' : 'PH',
    '강원' : 'GW',
    '서울' : 'SL'
}


def get_team_id(team_nm):
    if(teams.__contains__(team_nm)):
        return teams[team_nm]
    else:
        return 'NO' # 국제전

def get_date(dateString):
    pattern = '[^0-9]'
    repl = ''

    onlydate = re.sub(pattern=pattern, repl=repl, string=dateString)

    return onlydate

def make_g_id(date, h_t_id, a_t_id):
    return f'{date}{h_t_id}{a_t_id}'

def convertMonth(i):
    if i < 10:
        return '0' + str(i)
    else:
        return str(i)


for i in range(1, 13):
    month = convertMonth(i)

    print(f'----------------------{month}월 일정 INSERT 시작-----------------------------')

    html = urlopen(f"http://www.kleague.com/schedule/get_lists?datatype=html&month={month}&select_league=1&select_league_year=2020&select_club=&select_reserve=&_=1583890352626")
    bsObject = BeautifulSoup(html, "html.parser")

    tables = bsObject.select('.table')

    for table in tables:
        gamedate = get_date(table.select('thead.thead-light > tr > th')[0].text)
        matches = table.select('tbody > tr > td.team-match')
        print(f'----------------------{gamedate} 일정 INSERT ----------------------------')
        for match in matches:
            team1 = get_team_id(match.select('div.team-1 > span.club')[0].text)
            team2 = get_team_id(match.select('div.team-2 > span.club')[0].text)
            # print(team1, team2)
            # insert_football_game_data(make_g_id(gamedate, team1, team2), gamedate, team1, team2)

    print(f'----------------------{month}월 일정 INSERT 완료-----------------------------')
