class hole:

    def __init__(self,pos:str,num:int,goal:bool) -> None:
        '''
        pos : A・Bどちらかを保持する陣地ステータス
        num : 入っている石の数
        goal : goalであるか否かを保持するステータス
        ---
        '''
        self.pos = pos
        self.num = num
        self.goal = goal

class Mankara:

    def __init__(self):
        '''
        board : 盤面の状況
        turn : どちらのターンかを表すステータス
        ---
        '''
        self.board = [
            hole("A",4,False),
            hole("A",4,False),
            hole("A",4,False),
            hole("A",4,False),
            hole("A",4,False),
            hole("A",4,False),
            hole("A",0,True),
            hole("B",4,False),
            hole("B",4,False),
            hole("B",4,False),
            hole("B",4,False),
            hole("B",4,False),
            hole("B",4,False),
            hole("B",0,True),
        ]
        # 0 : A, 1 : B
        self.turn = 0

    def viewBoard(self):
        '''
        盤面を表示する関数
        '''
        print("\n [B] #13 #12 #11 #10 #9  #8      ")
        print("---------------------------------")
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in reversed(self.board[7:13])]))
        print(": {} :-----------------------: {} :".format(self.board[13].num,self.board[6].num))
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in self.board[0:6]]))
        print("---------------------------------")
        print(" [A] #1  #2  #3  #4  #5  #6      \n")
    
    def get(self,pocket:int):
        '''
        指定した位置の石を取る関数

        pocket : 指定位置

        ---
        taking_piece : 取った石の数
        '''
        taking_piece = self.board[pocket].num
        self.board[pocket].num = 0
        return taking_piece
    
    def set(self,piece:int,choosen:int):
        '''
        指定した位置に石を置く関数

        piece : 取った石の数
        choosen : 石を取った箇所
        
        ---
        1 : 最後においた場所がgoal
        0 : それ以外
        '''
        for p in range(1,piece+1):
            self.board[(choosen+p)%14].num += 1
        if self.board[(choosen+p)%14].goal : 
            return 1
        else : 
            return 0
    
    def CPU(self,scope:range):
        '''
        CPUが石を取る箇所を決定する関数

        scope : 石を取ることができる範囲
        
        ---
        place : CPUが石を取る箇所
        '''
        holes = [self.board[i].num for i in scope]
        place = holes.index(max(holes))+7
        return place
    
    def judge(self):
        '''
        勝敗を返す関数
        
        ---
        "win A !!" : Aの勝利
        "win B !!" : Bの勝利
        0 : ゲーム継続
        '''
        a = [hole.num for hole in self.board[0:6]]
        b = [hole.num for hole in self.board[7:13]]
        if sum(a) == 0:
            return "win A !!"
        elif sum(b) == 0:
            return "win B !!"
        else:
            return 0

def main():

    m = Mankara()
    print("\n先攻はあなた(A)です、CPU(B)は後攻です")
    print("あなたが操作できるのは#1〜#6の中だけです")

    while True:
        t = m.judge()

        if t:
            print(t)
            break

        m.viewBoard()

        if not m.turn:
            choosen = int(input("A：どこから石を取りますか(1〜6)："))-1
            if choosen < 0 or choosen > 5 or m.board[choosen].num == 0:
                continue
        else :
            choosen = m.CPU(range(7,13))
            print(f"B：{choosen+1}の石を取りました")

        num = m.get(choosen)
        chance = m.set(num,choosen)
        if chance :
            continue
        m.turn = not m.turn

if __name__=="__main__":
    main()