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
        "P",    # Pair
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
    
    def serial_num(self):
        '''
        "数字"が連番であるかを確認
        '''
        serial = sorted([self.st_of_num_dict[t[1:]] for t in self.tar_sorted])
        renban = [serial[x+1] - serial[x] for x in range(len(serial)-1)]
        return self.tar_sorted if set(renban)=={1} else False
    
    def role_judge(self):
        '''
        役の判定
        '''
        ps = self.pairs_suit()
        pn, pn_list = self.pairs_nums()
        sn = self.serial_num()

        roles = []
        if ps:
            if sn:
                if sn[0][1:] == 'A':
                    roles.append('RF')
                else: 
                    roles.append('SF')
            else:
                roles.append('F')
        if pn:
            if len(pn_list) == 2:
                if pn_list[0][1] == 4:
                    roles.append('4K')
                else:
                    roles.append('FH')
            elif len(pn_list) == 3:
                if pn_list[0][1] == 3:
                    roles.append('3K')
                else:
                    roles.append('2P')
            elif len(pn_list) == 4:
                roles.append('P')
            else:
                roles.append('HC')
        if sn:
            roles.append('S')

        roles.sort(key=lambda x: self.ranks.index(x))
        
        return roles[0]

def main():

    player_num = int(input("人数を入力してください："))
    num_of_times = 0

    cards = Cards()
    board = Board(cards,player_num)

    board.deal_cards(5)

    while num_of_times != player_num*2:

        turn = num_of_times % player_num

        for idx, hand in enumerate(board.open_player_cards()):
            print(f"Player {idx + 1}: {' '.join(hand)}")

        del_cards = list(map(int,input(f"\nPlayer {turn + 1}: どれを捨てる？\n").split()))
        if not del_cards:
            continue

        board.trash_cards(del_cards,turn)
        get_cards = board.draw_from_deck(len(del_cards))
        board.add_cards(get_cards,turn)

        num_of_times += 1
    
    result = map(Role, board.open_player_cards())
    for idx, r in enumerate(result):
        print(f"\nPlayer {idx + 1} の役: {r.role_judge()}")

if __name__ == "__main__":
    main()