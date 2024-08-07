# マンカラのルール説明 → https://youtu.be/pNZvBn5B3P8?si=um5Scm0egsSTC31I

# クラス(hole)を作成 
class hole:
    # コンストラクタを生成(pos:文字列型, num:整数型, goal:真偽型 と３つのパラメータを取り、戻り値はNone型とする)
    def __init__(self,pos:str,num:int,goal:bool) -> None:
        # コンストラクタ引数(pos, num, goal)をインスタンス変数に設定
        self.pos = pos
        self.num = num
        self.goal = goal

# クラス(Mankara)を作成
class Mankara:
    # コンストラクタを生成
    def __init__(self):
        # インスタンス変数(board)をリストで作成

        """ boaldの作成詳細

        「１ユーザーで６個のポケットと１つのゴールを持っている」状態を
        holeクラスを用いて、リストで作成してみよう！

        ・holeクラスの使い方
        第１引数 pos ... ユーザー -> [A or B] で設定
        第２引数 num ... 各ポケットの石の個数 -> 初期値は[4]で設定
        第３引数 goal ... ポケットがゴールかどうか -> ゴールなら[True], ポケットなら[False]
        """
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
        # ユーザー切替のターン設定 (0 : A, 1 : B)
        self.turn = 0

    # ボードを表示するメソッド(viewBoard)を作成 -> ゲーム画面のためこちらで用意
    def viewBoard(self):
        print("\n [B] #13 #12 #11 #10 #9  #8      ")
        print("---------------------------------")
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in reversed(self.board[7:13])]))
        print(": {} :-----------------------: {} :".format(self.board[13].num,self.board[6].num))
        print(":   : {} : {} : {} : {} : {} : {} :   :".format(*[i.num for i in self.board[0:6]]))
        print("---------------------------------")
        print(" [A] #1  #2  #3  #4  #5  #6      \n")
    
    # ポケットから石を取るメソッド(stone_get)を作成 -> 引数pocketを整数型で設定
    def stone_get(self,pocket:int):
        # 指定したpocketの石の数を変数(taking_piece)に保存
        taking_piece = self.board[pocket].num
        # 指定したpocketの石の数を0にする
        self.board[pocket].num = 0
        # taking_pieceを戻り値として返す
        return taking_piece
    
    # 各ポケットに石を置くメソッド(stone_set)を作成 -> 引数piece, chosenを整数型で設定
    def stone_set(self,piece:int,chosen:int):
        # 1~piece+1 の範囲でくりかえし。変数名はp
        for p in range(1,piece+1):
            # 選択した位置(chosen) + くりかえしの値(p) のポケットに+1する
            self.board[(chosen+p)%14].num += 1
            # もし(先ほどの)選択したポケットがゴールだったら
            if self.board[(chosen+p)%14].goal : 
                # 1 を戻り値で返す
                return 1
            # そうでなければ
            else : 
                # 0 を戻り値で返す
                return 0
    
    # 対戦相手(CPU)が取る石を選択するメソッド(CPU)を作成 -> 引数scopeをrange型で設定
    def CPU(self,scope:range):
        # scopeの範囲で各穴にある石の数をリスト(holes)へ格納
        holes = [self.board[i].num for i in scope]
        # holesリスト内で最も大きい値に+7し、戻り値で返す ※リスト内の値を検索するindex関数を用いよう
        return holes.index(max(holes))+7
    
    # ユーザーの勝敗を判断するメソッド(judge)を作成
    def judge(self):
        # 0~6番ポケットの石の数を、それぞれユーザーのリスト(A)へ格納 
        A = [hole.num for hole in self.board[0:6]]
        # 7~13番ポケットの石の数をCPUのリスト(B)へ格納
        B = [hole.num for hole in self.board[7:13]]
        """ リファクタver
        # 空のリスト(A, B)を作成する
        A, B = [], []

        for hole in self.boald[0:6]:
            A.append(hole.num)

        for hole in self.boald[7:13]:
            B.append(hole.num)
        """
        # リスト(A)の合計値が0だったら (ユーザーのポケットが全て空だったら)
        if sum(A) == 0:
            # Aの勝利メッセージを戻り値で返す -> "win A !!"
            return "win A !!"
        # リスト(B)の合計値が0だったら (CPUのポケットが全て空だったら)
        elif sum(B) == 0:
            # Bの勝利メッセージを戻り値で返す -> "win B !!"
            return "win B !!"
        # そうでなければ
        else:
            # 0 を戻り値で返す
            return 0

# ゲームを実行する関数(main)を作成
def main():

    # クラス(Mankara)をオブジェクト(変数m)に代入
    m = Mankara()

    # 最初のメッセージを出力("\n先攻はあなた(A)です、CPU(B)は後攻です")
    print("\n先攻はあなた(A)です、CPU(B)は後攻です")
    # 最初のメッセージを出力("あなたが操作できるのは#1〜#6の中だけです")
    print("あなたが操作できるのは#1〜#6の中だけです")

    # ずっとくりかえす
    while True:
        # judgeメソッドを呼び出し、結果を変数(t)に代入する
        t = m.judge()

        # もし変数(t)が真だったら
        if t:
            # 変数(t)を出力する
            print(t)
            # ループから抜け出す
            break

        # viewBoardメソッドを呼び出す
        m.viewBoard()

        # もしturn属性がfalse(1)だったら
        if not m.turn:
            # 石を取るポケットをシェルから入力し、変数(chosen)に代入する -> ("A：どこから石を取りますか(1〜6)：") 
            chosen = int(input("A：どこから石を取りますか(1〜6)："))-1
            # もし ①chosenが0より小さい ②chosenが5より大きい ③選択したポケットの石の数が0 のどれかの条件に該当したら
            if chosen < 0 or chosen > 5 or m.board[chosen].num == 0:
                # continueする
                continue
        # そうでなければ
        else :
            # CPUメソッドを(7~13)の範囲で呼び出し、結果(CPUが石を取るポケット)を変数(chosen)に代入する
            chosen = m.CPU(range(7,13))
            # CPUがどのポケットから石を取ったか出力する
            print(f"B：{chosen+1}の石を取りました")

        # stone_getメソッドを呼び出し(引数はchosen)、結果(石の個数)をnumに代入する
        num = m.stone_get(chosen)
        # stone_setメソッドを呼び出し(引数はnum,chosen)、結果(最終ポケットがゴールかどうか)をagainに代入する
        again = m.stone_set(num,chosen)
        # もしagainがtrueだったら
        if again :
            # continueする
            continue
        # turn属性を反転させる
        m.turn = not m.turn

# Pythonファイルが直接実行された場合にのみ処理を実行 -> 義務的なものなのでこちらで用意
if __name__=="__main__":
    main()