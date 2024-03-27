class hole:
    def __init__(self,pos:str,num:int,goal:bool) -> None:
        self.pos = pos
        self.num = num
        self.goal = goal

class Mankara:
    def __init__(self):
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
        print("\n [B] #13 #12 #11 #10 #9  #8      ")
        print("---------------------------------")
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in reversed(self.board[7:13])]))
        print(": {} :-----------------------: {} :".format(self.board[13].num,self.board[6].num))
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in self.board[0:6]]))
        print("---------------------------------")
        print(" [A] #1  #2  #3  #4  #5  #6      \n")
    
    def get(self,pocket:int):
        taking_piece = self.board[pocket].num
        self.board[pocket].num = 0
        return taking_piece
    
    def set(self,piece:int,choosen:int):
        for p in range(1,piece+1):
            self.board[(choosen+p)%14].num += 1
        if self.board[(choosen+p)%14].goal : 
            return 1
        else : 
            return 0
    
    def CPU(self,scope:range):
        holes = [self.board[i].num for i in scope]
        return holes.index(max(holes))+7
    
    def judge(self):
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
            if choosen < 0 or choosen > 5:
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