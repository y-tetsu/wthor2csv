import datetime
import csv


FORMAT = 'iso-8859-2'
HEADER_BYTES = 16
JOU_BYTES = 20
TRN_BYTES = 26
WTB_BYTES = 68
MAX_MOVES = 60


class Wthor:
    def __init__(self, jou='WTHOR.JOU', trn='WTHOR.TRN', wtb='WTH_2022.wtb'):
        self.players = self.get_players(jou)
        self.tournaments = self.get_tournaments(trn)
        self.games = self.get_games(wtb)

    def get_players(self, jou):
        ret = []
        header = self.decode_header(jou)
        with open(jou, 'rb') as f:
            f.read(HEADER_BYTES)
            for _ in range(header['records']):
                player = f.read(JOU_BYTES).decode(FORMAT).replace('\x00', '')
                ret.append(player)
        return ret

    def get_tournaments(self, trn):
        ret = []
        header = self.decode_header(trn)
        with open(trn, 'rb') as f:
            f.read(HEADER_BYTES)
            for _ in range(header['records']):
                tournament = f.read(TRN_BYTES).decode(FORMAT)
                tournament = tournament.replace('\x00', '')
                ret.append(tournament)
        return ret

    def get_games(self, wtb):
        ret = []
        header = self.decode_header(wtb)
        board_size = header['board_size']
        match_year = header['match_year']
        depth = header['depth']
        with open(wtb, 'rb') as f:
            f.read(HEADER_BYTES)
            for _ in range(header['game_count']):
                tournament_no = self._byte_to_int(f.read(2))
                black_no = self._byte_to_int(f.read(2))
                white_no = self._byte_to_int(f.read(2))
                black_score = self._byte_to_int(f.read(1))
                theoretical = self._byte_to_int(f.read(1))
                tournament = self.tournaments[tournament_no]
                black = self.players[black_no]
                white = self.players[white_no]
                moves = []
                for _ in range(MAX_MOVES):
                    move = str(self._byte_to_int(f.read(1)))
                    if len(move) != 2:
                        continue
                    row = chr(ord('a') + int(move[1]) - 1)
                    col = move[0]
                    moves.append(row + col)
                record = ''.join(moves)
                ret.append({
                    'board_size': board_size,
                    'match_year': match_year,
                    'tournament': tournament,
                    'black': black,
                    'white': white,
                    'black_score': black_score,
                    'theoretical': theoretical,
                    'depth': depth,
                    'record': record,
                })
        return ret

    def decode_header(self, dbname):
        with open(dbname, 'rb') as f:
            created_date = self._get_created_date(f)
            game_count = self._byte_to_int(f.read(4))
            records = self._byte_to_int(f.read(2))
            match_year = self._byte_to_int(f.read(2))
            board_size = self._byte_to_int(f.read(1))
            match_type = self._byte_to_int(f.read(1))
            depth = self._byte_to_int(f.read(1))
        return {
            'created_date': created_date,
            'game_count': game_count,
            'records': records,
            'match_year': match_year,
            'board_size': board_size,
            'match_type': match_type,
            'depth': depth,
        }

    def _get_created_date(self, f):
        year = ""
        for _ in range(2):
            year += str(self._byte_to_int(f.read(1)))
        month = str(self._byte_to_int(f.read(1)))
        day = str(self._byte_to_int(f.read(1)))
        date = year + '-' + month + '-' + day
        return datetime.datetime.strptime(date, '%Y-%m-%d')

    def _byte_to_int(self, byte, byteorder='little'):
        return int.from_bytes(byte, byteorder=byteorder)

    def to_csv(self, csv_file='output.csv'):
        header = [
            'Match Year',
            'Tournament Name',
            'Black Player Name',
            'White Player Name',
            'Board Size',
            'Black Score',
            'Black Theoretical Score',
            'Depth',
            'Record',
        ]
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for game in self.games:
                line = [
                    game['match_year'],
                    game['tournament'],
                    game['black'],
                    game['white'],
                    game['board_size'],
                    game['black_score'],
                    game['theoretical'],
                    game['depth'],
                    game['record'],
                ]
                writer.writerow(line)


if __name__ == '__main__':
    Wthor().to_csv()
