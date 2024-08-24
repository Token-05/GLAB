# randomライブラリをインポート
import random

# クラス(Cards)を作成
class Cards:

    # トランプの絵柄を表すリスト(suit)に ['♤','♡','♢','♧'] を代入
    suit = ['♤','♡','♢','♧']
    # トランプの数字を表すリスト(number)に ['A','K','Q','J','10','9','8','7','6','5','4','3','2'] を代入
    number = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']

    # コンストラクタを生成 -> 義務的なもの
    def __init__(self):
        # 何も行わない
        pass
    
    # 特殊メソッド(__call__)を定義
    def __call__(self):
        '''
        クラスインスタンスを呼び出し時、山札の作成
        '''
        # トランプのカードを表すリスト(cards)を作成する
        cards = []
        # 絵柄リスト(suit)を変数sに入れてくりかえす
        for s in self.suit:
            # 数字リスト(number)を変数(n)に入れてくりかえす
            for n in self.number:
                # カードリスト(cards)に(s + n)を追加する
                cards.append(s + n)
        # シャッフルされたカードリスト(cards_shuffled)を作成する
        # -> 関数(random.sample)を用いて、リスト(cards)の値から同じ要素数を持つシャッフルされたリストを作成しよう
        cards_shuffled = random.sample(cards,len(cards))
        # リスト(cards_shuffled)を戻り値として返す
        return cards_shuffled

# クラス(Board)を作成
class Board:

    # コンストラクタを生成 -> 引数(cards, player_num)をCards型, int型で設定
    def __init__(self, cards:Cards, player_num:int):
        '''
        cards : Cardsクラス
        player_num : プレイヤーの数
        '''
        # リスト(cards)を山札を表すインスタンス変数(deck)に設定
        self.deck = cards()
        # プレイヤーの手札を表すリスト(player_cards)を作成
        self.player_cards = []
        # プレイヤーの人数を表す引数(player_num)をインスタンス変数に設定
        self.player_num = player_num

    # 山札からカードを引くメソッド(draw_from_deck)を作成 -> 引数(cards_num)をint型で設定
    def draw_from_deck(self,cards_num:int):
        '''
        山札からカードを引く
        '''
        # 新たなリスト(drawn_deck)を作成し、山札リスト(deck)の末尾から引数(cards_num)枚分のカードを取得
        drawn_deck = self.deck[-cards_num:]
        # 取得したカード(cards_num)の枚数分、山札リスト(deck)の末尾から削除
        del self.deck[-cards_num:]
        # カードが引かれた山札リスト(drawn_deck)を返す
        return drawn_deck

    # プレイヤーにカードを配布するメソッド(deal_cards)を作成 -> 引数(cards_num)をint型で設定
    def deal_cards(self,cards_num:int):
        '''
        山札からカードを配布
        '''
        # プレイヤーの人数分(player_num)だけ、変数(_)に入れてくりかえす
        for _ in range(self.player_num):
            # リスト(player_cards)に山札から引いたカードを追加 -> (cards_num)枚分追加しよう
            # ※(このときplayer_cardsは、プレイヤーごとのカードリストとして、二次元配列になるよ！)
            self.player_cards.append(self.draw_from_deck(cards_num))
    
    # 手札に任意のカードを追加するメソッド(add_cards)を作成 -> 引数(get_cards, turn)をlist型,int型で設定
    def add_cards(self,get_cards:list,turn:int):
        '''
        手札に任意のカードを追加
        '''
        # 現在ターンのプレイヤー手札(player_cards[turn])に任意のカードを表す引数(get_cards)を追加
        self.player_cards[turn].extend(get_cards)

    # 手札から任意のカードを捨てるメソッド(trash_cards)を作成 -> 引数(del_cards, turn)をlist[int]型, int型で設定
    def trash_cards(self,del_cards:list[int],turn:int):
        '''
        手札から任意のカードを捨てる
        '''
        # 捨てたいカードの引数(del_cards)を変数(c)に入れてくりかえす
        for c in del_cards:
            # プレイヤー手札(player_cards[現在ターン][c])をNoneに設定 -> 指定したカードを捨てる
            self.player_cards[turn][c] = None 
        # 現在ターンのプレイヤー手札を、捨てられたカード(None)が取り除かれたものにする -> 再代入しよう
        # filter関数を用いると、リストから指定した値の要素を取り除くことができるよ！
        self.player_cards[turn] = list(filter(None, self.player_cards[turn]))

    # 全員の手札を表示するメソッド(open_player_cards)を作成
    def open_player_cards(self):
        '''
        全員の手札を返す
        '''
        # プレイヤー手札(player_cards)を戻り値として返す
        return self.player_cards

# クラス(Role)を作成
class Role:

    # @@ ポーカーの役を表すリスト(ranks)を作成
    ranks = [
        "RF",   # Royal Flush
        "SF",   # Straight Flush
        "4K",   # Four of a Kind
        "FH",   # Full House
        "F",    # Flush
        "S",    # Straight
        "3K",   # Three of a Kind
        "2P",   # Two Pair
        "OP",   # One Pair
        "HC"    # High Card
    ] # @@

    # コンストラクタを生成 -> 引数(target)をlist[str]型で設定
    def __init__(self, target:list[str]):
        '''
        target : 役を確認する対象のカードリスト
        '''
        # Cardクラス変数(number)を変数(n_list)に代入する
        self.n_list = Cards().number
        # 役を確認するために用いる辞書(st_of_num_dict)を作成
        self.st_of_num_dict = {}
        # 変数(self.n_list)の要素数分だけ、変数(n)をくりかえす
        for n in range(len(self.n_list)):
            # 辞書(st_of_num_dict)にキー(n_list)と値(n)を設定する
            self.st_of_num_dict[self.n_list[n]] = n 

        # 一時的な関数(get_sort_key)を作成 -> 引数(card)をstr型として設定
        def get_sort_key(card:str):
            # 辞書(st_of_num_dict)のキーに引数(card)の2文字目以降を指定し、戻り値として返す
            return self.st_of_num_dict[card[1:]]

        # 役を確認したいカードリスト(target)の特定要素で(get_sort_key) 昇順に並び替え、新たなリスト(tar_sorted)に代入
        # -> sorted関数(対象リスト, (対象要素))を用いてみよう！
        self.tar_sorted = sorted(target, key=get_sort_key)

    # 絵柄が揃っているか確認するメソッド(pairs_suit)を作成
    def pairs_suit(self):
        '''
        "スート"が揃っているかを確認
        '''
        # 比較する絵柄リスト(pairs)を作成
        pairs = []
        # 確認したい役リスト(tar_sorted)を変数(t)に入れてくりかえす
        for t in self.tar_sorted:
            # リスト(pairs)に変数(t)の1文字目(絵柄)を追加する -> t[:1]と参照しよう！
            pairs.append(t[:1])

        # 比較する絵柄リスト(pairs)の[重複を除いた]要素数が １ だったら
        if len(set(pairs)) == 1:
            # リスト(tar_sorted)を戻り値として返す
            return self.tar_sorted
        # そうでなければ
        else:
            # False を戻り値として返す
            return False
    
    # 数字が揃っているか確認するメソッド(pairs_num)を作成
    def pairs_nums(self):
        '''
        "数字"が揃っているかを確認
        '''
        # 比較する数字リスト(pairs)を作成
        pairs = []
        # 数字の出現回数を表す辞書(pairs_dict)を作成
        pairs_dict = {}

        # 確認したい役リスト(tar_sorted)を変数(t)に入れてくりかえす
        for t in self.tar_sorted:
            # リスト(pairs)に変数(t)の2文字目以降(数字)を追加する -> t[1:]と参照しよう！
            pairs.append(t[1:])
            
            # もし辞書(pairs_dict)に変数(t)の2文字目以降(数字)が含まれていたら
            if t[1:] in pairs_dict:
                # 辞書(pairs_dict)のキー(t[1:])部分を +1する
                pairs_dict[t[1:]] += 1
            # そうでなければ
            else:
                # 辞書(pairs_dict)のキー(t[1:])部分を 1にする
                pairs_dict[t[1:]] = 1
        
        # 辞書(pairs_dict)のすべてのキー(.items)と値をの特定要素(key=lambda x:x[1] -> 各タプルの2文字目(カードの数字))を基準に、降順で並び替え、新たなリスト(pairs_sorted_list)に代入
        # -> sorted関数(対象リスト, (対象要素), (降順オプション))を用いてみよう！
        pairs_sorted_list = sorted(pairs_dict.items(), key=lambda x:x[1], reverse=True)
        
        # 並び替えられた、確認したい役リスト(tar_sorted)と数字リスト(pairs_sorted_list)を戻り値として返す
        return self.tar_sorted, pairs_sorted_list
    
    # 数字が連番か確認するメソッド(serial_num)を作成
    def serial_num(self):
        '''
        "数字"が連番であるかを確認
        '''
        # 一時的なリスト(temp_list)を作成
        temp_list = []
        # 確認したい役リスト(tar_sorted)を変数(t)に入れてくりかえす
        for t in self.tar_sorted:
            # 一時的な変数(value)に辞書(st_of_num_dict)をキー(変数(t)の2文字目以降 -> 数字部分)指定して代入
            value = self.st_of_num_dict[t[1:]]
            # リスト(temp_list)に変数(value)を追加
            temp_list.append(value)
        # リスト(temp_list)を昇順に並び替え、新たなリスト(serial)に代入
        serial = sorted(temp_list)

        # 連番の数字を格納するリスト(renban)を作成
        renban = []
        # 確認したい役リストの数字部分を示すリスト(serial)の要素数から1引いた値の分だけ、xをくりかえす
        for x in range(len(serial) - 1):
            # リスト(serial)の[x+1]から[x]を引いた値を変数(difference)に代入
            difference = serial[x + 1] - serial[x]
            # リスト(renban)に変数(difference)を追加
            renban.append(difference)
        
        # リスト(renban)の[重複を除いた]要素がすべて 1 だったら
        if set(renban)=={1}:
            # リスト(tar_sorted)を返す
            return self.tar_sorted
        # そうでなければ
        else:
            # False を戻り値として返す
            False
    
    # 実際に役を判定するメソッド(role_judge)を作成
    def role_judge(self):
        '''
        役の判定
        '''
        # 絵柄が揃っているか確認するメソッド(pairs_suit)の結果を変数(ps)に代入
        ps = self.pairs_suit()
        # 数字が揃っているか確認するメソッド(pairs_nums)の結果を変数(pn, pn_list)に代入
        pn, pn_list = self.pairs_nums()
        # 数字が連番か確認するメソッド(serial_num)の結果を変数(sn)に代入
        sn = self.serial_num()
        # 役を保存するリスト(roles)を作成
        roles = []

        # 変数(ps)がTrueだったら -> 絵柄が揃っていたら
        if ps:
            # 変数(sn)がTrueだったら -> 数字が連番だったら
            if sn:
                # 変数(sn)の[0][1:]が'A'だったら -> 手札の最初のカード(数字部分)がAだったら(snは降順で並んでいるので、[A,K,Q,J,10]が判定できる)
                if sn[0][1:] == 'A':
                    # リスト(roles)に'RF'を追加する
                    roles.append('RF')
                # そうでなければ -> [J,10,9,8,7]などを判定
                else: 
                    # リスト(roles)に'SF'を追加する
                    roles.append('SF')
            # そうでなければ -> 絵柄のみが揃っていたら
            else:
                # リスト(roles)に'F'を追加する
                roles.append('F')

        # 変数(pn)がTrueだったら -> 数字が揃っていたら
        if pn:
            # 手札の数字の出現回数を示すリスト(pn_list)の要素数が 2 だったら -> 手札に2種類の異なる数字が含まれていたら
            if len(pn_list) == 2:
                # リスト(pn_list)の[0][1]が 4 だったら -> 手札に4枚同じカードが存在したら
                if pn_list[0][1] == 4:
                    # リスト(roles)に'4K'を追加する
                    roles.append('4K')
                # そうでなければ -> 手札に2枚,3枚同じカードが存在したら ex(A,A,3,3,3)
                else:
                    # リスト(roles)に'FH'を追加する
                    roles.append('FH')
            # 手札の数字の出現回数を示すリスト(pn_list)の要素数が 3 だったら -> 手札に3種類の異なる数字が含まれていたら
            elif len(pn_list) == 3:
                # リスト(pn_list)の[0][1]が 3 だったら -> 手札に3枚同じカードが存在したら
                if pn_list[0][1] == 3:
                    # リスト(roles)に'3K'を追加する
                    roles.append('3K')
                # そうでなければ -> 手札に2枚,2枚同じカードが存在したら ex(A,A,3,3,7)
                else:
                    # リスト(roles)に'2P'を追加する
                    roles.append('2P')
            # 手札の数字の出現回数を示すリスト(pn_list)の要素数が 4 だったら -> 手札に4種類の異なる数字が含まれていたら
            elif len(pn_list) == 4:
                # リスト(roles)に'OP'を追加する
                roles.append('OP')
            # そうでなければ -> 手札のカードがすべて異なっていたら 
            else:
                # リスト(roles)に'HC'を追加する
                roles.append('HC')

        # 変数(sn)がTrueだったら -> 数字が連番だったら
        if sn:
            # リスト(roles)に'S'を追加する
            roles.append('S')

        # リスト(roles)を役の強さ(key=lambda x: self.ranks.index(x))を基準に並び替える
        #  -> リスト自体を変更するsort関数(対象要素)を用いてみよう！
        roles.sort(key=lambda x: self.ranks.index(x))
        
        # リストの最初の値(roles[0])を戻り値として返す -> リストの中で最も強い役を返す
        return roles[0]

# ゲームを実行する関数(main)を作成
def main():

    # 変数(player_num)にシェルから文字列("人数を入力してください：")を入力させる
    player_num = int(input("人数を入力してください："))
    # ターンをカウントする変数(turn_count)を作成 -> 初期値は0
    turn_count = 0

    # クラス(Cards)をオブジェクト(cards)に代入
    cards = Cards()
    # クラス(Board(cards,player_num))をオブジェクト(board)に代入
    board = Board(cards,player_num)

    # カードを配布するメソッド(board.deal_cards)を呼び出す -> 引数は5
    board.deal_cards(5)

    # 変数(turn_count)とプレイヤー人数(player_num)の２倍の値が[等しくなかったら]くりかえす
    while turn_count != player_num*2:
        # 現在ターンを示す変数(turn)に変数(turn_count)プレイヤー人数(player_num)の余りを代入する
        turn = turn_count % player_num

        # 手札を表示するメソッド(open_player_cards)を呼び出し、要素番号(idx)と値(hand)をそれぞれくりかえす
        # -> enumerate関数を用いてみよう！
        for idx, hand in enumerate(board.open_player_cards()):
            # 文字列を表示(f"Player {idx + 1}: {' '.join(hand)}")
            print(f"Player {idx + 1}: {' '.join(hand)}")

        # 捨てるカードリスト(del_cards)に [list(map(int,input(f"\nPlayer {turn + 1}: どれを捨てますか？\n").split()))] と代入する
        del_cards = list(map(int,input(f"\nPlayer {turn + 1}: どれを捨てますか？\n").split()))
        # もしリスト(del_cards)が空になったら
        if not del_cards:
            # 次に進む
            continue

        # カードを捨てるメソッド(board.trash_cards)を呼び出す -> 引数は(del_cards,turn)と設定
        board.trash_cards(del_cards,turn)
        # リスト(get_cards)に山札からカードを引くメソッド(draw_from_deck(len(del_cards)))の結果を代入
        get_cards = board.draw_from_deck(len(del_cards))
        # カードを手札に加えるメソッド(board.add_cards(get_cards,turn))を呼び出す
        board.add_cards(get_cards,turn)

        # turn_countを +1 する
        turn_count += 1
    
    # 結果(result)に [map(Role, board.open_player_cards())] を代入
    result = map(Role, board.open_player_cards())
    # 結果(result)を 要素番号(idx)と値(r)に切り分け、それぞれくりかえす
    # -> enumerate関数を用いてみよう！
    for idx, r in enumerate(result):
        # 文字列を出力(f"\nPlayer {idx + 1} の役: {r.role_judge()}")
        print(f"\nPlayer {idx + 1} の役: {r.role_judge()}")

# @@ Pythonファイルが直接実行された場合にのみ処理を実行 -> 義務的なものなのでこちらで用意
if __name__ == "__main__":
    main() # @@