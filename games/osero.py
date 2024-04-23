import random

class boards:

    def __init__(self):
        '''
        frame : 盤面の縁を表すステータス
        air : 何も置かれていないことを表すステータス
        pieces_status : 2種類の駒のステータス
        board : 盤面の状況
        turn : どちらのターンかを表すステータス
        dir : 走査方向に対応する単位ベクトル、全8方向
        ---
        '''

        self.frame = "×"
        self.air = "."
        self.pieces_status = {0:"○", 1:"●"}

        self.board = []
        for i in range(10):
            tentative = []
            for j in range(10):
                if i in (0,9) or j in (0,9):
                    tentative.append(self.frame)
                else:
                    tentative.append(self.air)
            self.board.append(tentative)

        self.turn = 0
        self.dir = [
            [1,-1],
            [1,0],
            [1,1],
            [0,1],
            [-1,1],
            [-1,0],
            [-1,-1],
            [0,-1]
        ]

        self.board[4][4] = self.pieces_status[0]
        self.board[5][5] = self.pieces_status[0]
        self.board[5][4] = self.pieces_status[1]
        self.board[4][5] = self.pieces_status[1]

    def view_bord(self):
        '''
        盤面を表示する関数
        '''
        print(" ", " ".join(map(str, range(8))))
        for i, bo in enumerate(self.board[1:9]):
            print(i, " ".join(bo[1:9]))

    def set(self,koma:int,x:int,y:int):
        '''
        駒を配置・更新する関数
        
        koma : 駒の種類
        x : x座標
        y : y座標
        ---
        '''
        self.board[x][y] = self.pieces_status[koma]
    
    def check_st_line(self,x:int,y:int,d:int,swapable:list):
        '''
        指定座標を始点として直線状に走査する関数
        
        x : x座標
        y : y座標
        d : 方向
        swapable : ひっくり返し可能な座標
        ---
        swapable : ひっくり返し可能な座標
        '''
        next = self.board[x][y]
        if next not in (self.frame,self.air):
            if self.pieces_status[self.turn] == next:
                return swapable
            else:
                swapable.append((x,y))
                self.check_st_line(x+self.dir[d][0],y+self.dir[d][1],d,swapable)
        else: 
            swapable.clear()
        return swapable

    def check_radiation(self,x:int,y:int):
        '''
        指定座標を中心として放射状に走査する関数
        
        x : x座標
        y : y座標
        ---
        swapable : ひっくり返し可能な座標
        '''
        swapables = []
        for index,d in enumerate(self.dir):
            swapable = self.check_st_line(x+d[0],y+d[1],index,[])
            swapables.extend(swapable)
        return swapables
    
    def swap(self,x:int,y:int):
        '''
        駒をひっくり返す関数
        
        x : x座標
        y : y座標
        '''
        swap_list = self.check_radiation(x,y)
        for s in swap_list:
            self.set(self.turn,s[0],s[1])

    def setable(self,x:int,y:int):
        '''
        指定座標に駒を置けるか否かを返す関数
        
        x : x座標
        y : y座標
        ---
        1 : 配置可能
        0 : 配置不可能
        '''
        swapable_list = self.check_radiation(x,y)
        if swapable_list and self.board[x][y] == self.air:
            return 1  
        else:
            return 0
    
    def check_bord(self):
        '''
        盤面上に関する情報を返す関数
        
        ---
        hint : 配置可能な座標
        air_exists : 駒の置き場所
        white : 白の駒の数
        black : 黒の駒の数
        '''
        hint = []
        air_exists = False
        white = 0
        black = 0

        for i,col in enumerate(self.board[1:9]):
            for j,d in enumerate(col[1:9]):
                if self.setable(i+1,j+1):
                    hint.append((j,i))
                if d == self.air:
                    air_exists = True
                elif d == self.pieces_status[0]:
                    black+=1
                elif d == self.pieces_status[1]:
                    white+=1

        random.shuffle(hint)
        return hint,air_exists,black,white
    
    def screen_win_or_lose(self,bk:int,wh:int):
        '''
        勝敗を表示する関数
        
        bk : 黒の駒数
        wh : 白の駒数
        ---
        '''
        if bk > wh:
            t = f"「{self.pieces_status[0]}」の勝利でした"
        elif bk < wh:
            t = f"「{self.pieces_status[1]}」の勝利でした"
        else :
            t = "両者引き分けでした"
        print(f"黒{bk}、白{wh}により、"+t)


def main(player:bool=True): 

    error_message = ""
    b = boards()

    while True:

        b.view_bord()
        print("\n")
        hint,exists,bk,wh = b.check_bord()

        if not exists:
            b.screen_win_or_lose(bk,wh)
            break

        if player and b.turn:
            if hint:
                b.set(b.turn,hint[-1][1]+1,hint[-1][0]+1)
                b.swap(hint[-1][1]+1,hint[-1][0]+1)
                b.turn = not b.turn
                error_message = ""
                continue

        if not hint:
            error_message="置くことができません、再び"
            b.turn = not b.turn
            hint,_,_,_ = b.check_bord()
            if not hint:
                b.screen_win_or_lose(bk,wh)
                break
            continue

        print(f'{error_message}「{b.pieces_status[b.turn]}」の番です')
        print("ヒント：",*hint)
        i = list(map(int, input('「横 縦」のように入力してください：').split()))
        print("\n\n")

        if not b.setable(i[1]+1,i[0]+1):
            error_message = '置くことができません、'
            continue

        b.set(b.turn,i[1]+1,i[0]+1)
        b.swap(i[1]+1,i[0]+1)
        b.turn = not b.turn
        error_message = ""

if __name__=="__main__":
    main()