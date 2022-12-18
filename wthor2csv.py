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
        self.players = self.get_records(jou, JOU_BYTES)
        self.tournaments = self.get_records(trn, TRN_BYTES)
        self.games = self.get_games(wtb)

    def get_records(self, filename, record_bytes):
        ret = []
        header = self.decode_header(filename)
        with open(filename, 'rb') as f:
            f.read(HEADER_BYTES)  # discard
            for _ in range(header['records']):
                record = f.read(record_bytes).decode(FORMAT)
                ret.append(record.replace('\x00', ''))
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
        y = ""
        for _ in range(2):
            y += str(self._byte_to_int(f.read(1)))
        m = str(self._byte_to_int(f.read(1)))
        d = str(self._byte_to_int(f.read(1)))
        return datetime.datetime.strptime('-'.join([y, m, d]), '%Y-%m-%d')

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
