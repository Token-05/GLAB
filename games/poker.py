import random

class Cards:

    # スート
    suit = ['♤','♡','♢','♧']
    # 数
    number = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']

    def __init__(self):
        pass
    
    def __call__(self):
        '''
        クラスインスタンスを呼び出し時、山札の作成
        '''
        cards = [s+n for s in self.suit for n in self.number]
        cards_shuffled = random.sample(cards,len(cards))
        return cards_shuffled

class Board:

    def __init__(self, cards:Cards, users:int):
        '''
        cards : Cardsクラス
        users : ユーザーの数
        '''
        self.deck = cards()
        self.users_list = []
        self.users = users

    def deal_cards(self,dtb_sheets:int):
        '''
        山札からカードを配布
        '''
        self.users_list = [self.draw_from_deck(dtb_sheets) for _ in range(self.users)]
    
    def trash_cards(self,del_cards:list[int],turn:int):
        '''
        手札から任意のカードを捨てる
        '''
        for c in del_cards:
            self.users_list[turn][c] = None 
        self.users_list[turn] = list(filter(None, self.users_list[turn]))

    def draw_from_deck(self,del_sheets):
        '''
        山札からカードを引く
        '''
        get_sheets = self.deck[-del_sheets:]
        del self.deck[-del_sheets:]
        return get_sheets
    
    def add_cards(self,get_cards:list,turn:int):
        '''
        手札に任意のカードを追加
        '''
        self.users_list[turn].extend(get_cards)

    def show_hands_all(self):
        '''
        全員の手札を返す
        '''
        return self.users_list

class Role:

    # ランク（強い順）
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
    ]

    def __init__(self, target:list[str]):
        '''
        target : 役を確認する対象のカードリスト
        '''
        self.n_list = Cards().number
        self.st_of_num_dict = {self.n_list[n]: n for n in range(len(self.n_list))}
        self.tar_sorted = sorted(target, key=lambda x: self.st_of_num_dict[x[1:]])
    
    def pairs_suit(self):
        '''
        "スート"が揃っているかを確認
        '''
        pairs = [t[:1] for t in self.tar_sorted]
        return self.tar_sorted if len(set(pairs))==1 else False
    
    def pairs_nums(self):
        '''
        "数字"が揃っているかを確認
        '''
        pairs = [t[1:] for t in self.tar_sorted]
        pairs_dict = {}
        
        for t in self.tar_sorted:
            if t[1:] in pairs_dict:
                pairs_dict[t[1:]] += 1
            else:
                pairs_dict[t[1:]] = 1
        
        pairs_sorted_list = sorted(pairs_dict.items(), key=lambda x:x[1], reverse=True)
        
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

        # 判定は基本ゴリ押し
        # もっと効率的な方法あるかも
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

    users = int(input("人数を入力してください："))
    num_of_times = 0

    cards = Cards()
    board = Board(cards,users)

    board.deal_cards(5)

    while num_of_times != users*2:

        turn = num_of_times % users

        for idx, hand in enumerate(board.show_hands_all()):
            print(f"Player {idx + 1}: {' '.join(hand)}")

        del_cards = list(map(int,input(f"\nPlayer {turn + 1}: どれを捨てる？\n").split()))
        if not del_cards:
            continue

        board.trash_cards(del_cards,turn)
        get_cards = board.draw_from_deck(len(del_cards))
        board.add_cards(get_cards,turn)

        num_of_times += 1
    
    result = map(Role, board.show_hands_all())
    for idx, r in enumerate(result):
        print(f"\nPlayer {idx + 1} の役: {r.role_judge()}")

if __name__ == "__main__":
    main()