# randomモジュールをインポート
import random

# boardsクラスの作成
class boards:

    # コンストラクタを作成 -> 
    def __init__(self):

        '''
        イニシャライザの設定

        self.frame : str
            - 枠、設置不可の場所
            - 初期値："×"
        
        self.air : str
            - 駒が置かれていない場所
            - 初期値："."
        
        self.status : dict
            - 駒の種類を保持
            - 初期値：0を"○"、1を"●"、とした辞書

        self.turn : int
            - ターンを保持
            - 初期値：0を設定(0か1のint型)

        self.board : list
            - 盤面データを保持
            - 初期値：以下のような二次元配列、サイズは10x10
            × × × × × × × × × ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × . . . . . . . . ×
            × × × × × × × × × ×
        
        self.dir : list
            - 探索方向を保持
            - 初期値：8方向の単位ベクトルを用意
        '''
        
        # 盤面の枠を表す変数(frame)に"x"を代入する
        self.frame = "×"
        # 駒の置かれてない状態を表す変数(air)に"."を代入する
        self.air = "."
        # 置かれている駒の白黒状態を表す変数(status)に辞書型として{0:"○", 1:"●"}を代入する
        self.status = {0:"○", 1:"●"}
        # プレイヤーのターンを表す変数(turn)に 0 を代入する
        self.turn = 0

        # ボードを作成するリスト(board)を初期化
        self.board = []
        # 変数(j)を10回くりかえす -> ボードの10行部分を作成する
        for j in range(10):
            # 列を表すリスト(row)を初期化
            row = []
            # 変数(i)を10回くりかえす -> ボードの10列部分を作成する
            for i in range(10):
                # もし ①iが0か9, ②jが0か9 だったら -> ボードの外側部分を作成する
                if i in [0, 9] or j in [0, 9]:
                    # 列を表すリスト(row)にself.frameを追加
                    row.append(self.frame)
                # そうでなければ
                else:
                    # 列を表すリスト(row)にself.airを追加 -> ボードの内側部分を作成する
                    row.append(self.air)
            
            # リスト(board)に列を表すリスト(row)を追加する -> 作成した列をボードに追加する
            self.board.append(row)
        
        # @@ マスの置ける方向を表す変数(dir)に単位ベクトルを設定 -> こちらで用意
        self.dir = [
            [1,-1],
            [1,0],
            [1,1],
            [0,1],
            [-1,1],
            [-1,0],
            [-1,-1],
            [0,-1]
        ] # @@

        """ 最初の盤面を設定 -> 下記のように、白黒駒が交互に置かれている状態にしよう

          0 1 2 3 4 5 6 7
        0 . . . . . . . .
        1 . . . . . . . .
        2 . . . . . . . .
        3 . . . ○ ● . . .
        4 . . . ● ○ . . .
        5 . . . . . . . .
        6 . . . . . . . .
        7 . . . . . . . .

        ex) 右下の角に黒駒を置く場合
        self.board[8][8] = self.status[0]

        """

        # 上記を参考に、最初の駒を設定しよう
        self.board[4][4] = self.status[0]
        self.board[5][5] = self.status[0]
        self.board[5][4] = self.status[1]
        self.board[4][5] = self.status[1]

    # 盤面を表示するメソッド(view_board)を作成
    def view_board(self):
        # 列番号を文字列で表示 -> [0 1 2 3 4 5 6 7]のような形
        # join関数で" "(空白)と数字を結合する。　数字部分は、map関数に引数として(1.str関数 / 2.range関数(列))を設定しよう
        print(" ", " ".join(map(str, range(8))))

        # enumerate関数を用いて、2つの変数(i, bo)をくりかえす。
        # enumerate関数の引数は、盤面を表すリスト(board)の駒部分[1:9]を指定する
        for i, bo in enumerate(self.board[1:9]):
            # 最初に行番号(i)を表示し、join関数で" "(空白)と駒部分(bo[1:9])を結合する。
            print(i, " ".join(bo[1:9]))

    # 駒を配置・更新するメソッド(set)を作成 -> 引数(koma, x, y)をint型で設定
    def set(self,koma:int,x:int,y:int):
        '''
        駒を配置・更新する

        koma : 駒の種類
        x : x座標
        y : y座標
        '''

        # 駒を配置する
        self.board[x][y] = self.status[koma]
    
    # ひっくり返せる駒を【直線で】調べるメソッド(check_st_line)を作成 -> 引数(x, y, d)をint型、(swapable)をlist型で設定
    def check_st_line(self,x:int,y:int,d:int,swapable:list):
        '''
        指定座標を始点として直線状に走査する
        
        x : x座標
        y : y座標
        d : 方向
        swapable : ひっくり返し可能な座標
        '''

        # 現在の座標(x, y)にある駒を変数(next)に保存する
        next = self.board[x][y]

        # 保存した駒の座標が("x", ".")でなかったら -> 無効マス, 空マスでないかチェック
        if next not in ("×","."):
            # 現在のターンのプレイヤーの駒と変数(next)が一致する場合
            if self.status[self.turn] == next:
                # リスト(swapable)を戻り値として返す -> 隣マスが自駒と同じ駒ということはひっくり返せないため、ここで処理を終了する
                return swapable
            # そうでなければ
            else:
                # swapableリストに(x,y)を追加する
                swapable.append((x,y))
                # メソッド(check_st_line)を再帰的に呼び出す -> 次の座標をチェックするため
                # 引数は(x+self.dir[d][0], y+self.dir[d][1], d, swapable)と指定する
                self.check_st_line(x+self.dir[d][0],y+self.dir[d][1],d,swapable)
        
        # そうでなければ -> 例外処理
        else: 
            # リスト(swapable)をクリア
            swapable.clear()
        # リスト(swapable)を戻り値として返す
        return swapable

    # ひっくり返せる駒を【周囲で】調べるメソッド(check_radiation)を作成 -> 引数(x, y)をint型で設定
    def check_radiation(self,x:int,y:int):
        '''
        指定座標を中心として放射状に走査する
        
        x : x座標
        y : y座標
        ---
        swapables : ひっくり返し可能な座標
        '''

        # 空のリスト(swapbles)を作成する
        swapables = []
        # enumerate関数を用いて引数に方向ベクトルのリスト(dir)を設定し、index, d をくりかえす -> 方向ベクトルをインデックス番号と合わせて取得する
        for index,d in enumerate(self.dir):
            # リスト(swapable)にcheck_st_line(x+d[0],y+d[1],index,[])の結果を代入する -> 現在の座標に方向ベクトルを加えた座標を調べ、駒が返せるか否かを返す
            swapable = self.check_st_line(x+d[0],y+d[1],index,[])
            # リスト(swapable)の要素をリスト(swapables)にそれぞれ追加する -> {.extend} を用いよう！
            swapables.extend(swapable)
        # リスト(swapables)を返す
        return swapables
    
    # 駒をひっくり返すメソッド(swap)を作成 -> 引数(x, y)をint型で設定
    def swap(self,x:int,y:int):
        '''
        駒をひっくり返す
        
        x : x座標
        y : y座標
        '''
        # ひっくり返せる駒のリスト(swap_list)にcheck_radiation(x,y)の結果を代入する
        swap_list = self.check_radiation(x,y)
        # リスト(swap_list)を変数(s)に入れて繰り返す
        for s in swap_list:
            # setメソッドを用いて、駒を配置する
            self.set(self.turn,s[0],s[1])

    # 返したい駒のマスに駒が置けるのかを調べるメソッド(setable)を作成 -> 引数(x, y)をint型で設定
    def setable(self,x:int,y:int):
        '''
        指定座標に駒を置けるか否かを返す
        
        x : x座標
        y : y座標
        ---
        1 : 配置可能
        0 : 配置不可能
        '''
        # チェックしたい駒のリスト(swapable_list)にcheck_radiation(x,y)の結果を代入する
        swapable_list = self.check_radiation(x,y)

        # もしswapableリストが存在したら
        if swapable_list:
            # board[x][y]が駒を置ける状態だったら
            if self.board[x][y] is self.air:
                # 1 を戻り値として返す
                return 1
            # そうでなかったら
            else:
                # 0 を戻り値として返す
                return 0
        # そうでなかったら
        else:
            # 0 を戻り値として返す
            return 0
    
    # 盤面についての情報を返すメソッド(check_board)を作成
    def check_board(self):
        '''
        盤面上に関する情報を返す
        
        ---
        hint : 配置可能な座標
        air_exists : 駒の置き場所が残っているかどうか
        white : 白の駒の数
        black : 黒の駒の数
        '''
        # 空のリスト(hint), 真偽値(air_exists)に、それぞれ [] と False を代入する
        hint,air_exists = [],False
        # 各駒数を表す変数(white, black)に、それぞれ 0 を代入する
        white, black = 0, 0

        # enumerate関数を用いて盤面を表すリスト(board)の駒部分[1:9]を指定し、i, col をくりかえす
        for i,col in enumerate(self.board[1:9]):
            # enumerate関数を用いてcol[1:9]を指定し、j, d をくりかえす
            for j,d in enumerate(col[1:9]):
                # もし(i+1, j+1)の座標に駒が置けるのなら
                if self.setable(i+1,j+1):
                    # リスト(hint)にその座標(j, i)を加える -> hintリストは(x,y)を逆転しているが、これは行と列を視覚的に分かりやすくするためである
                    hint.append((j,i))
                # 変数(d)が空きマスだったら
                if d == self.air:
                    # 空きマスの存在を表す変数(air_exists)の状態をTrueにする
                    air_exists = True
                # そうではなく、変数(d)が黒駒が配置されているマスだったら
                elif d == self.status[0]:
                    # 黒駒数を表す変数(black)を+1する
                    black+=1
                # そうではなく、変数(d)が白駒が配置されているマスだったら
                elif d == self.status[1]:
                    # 白駒数を表す変数(white)を+1する
                    white+=1

        # リスト(hint)をシャッフルする -> 配置可能な座標をランダムにすることで、予測不能な展開や公平性の担保が期待できる
        random.shuffle(hint)
        # hint, air_exists, black, white を戻り値として返す
        return hint,air_exists,black,white
    
    # 勝敗をチェックし表示するメソッド(judgment)を作成 -> 引数(black, wh)をint型で設定
    def judgment(self,black:int,white:int):
        '''
        勝敗を表示する関数
        
        black : 黒の駒数
        white : 白の駒数
        ---
        '''
        # もし黒駒数が白駒数より多かったら
        if black > white:
            # 変数(t)に f"「{self.status[0]}」の勝利です！」" と代入する
            t = f"「{self.status[0]}」の勝利です！」"
        # そうではなく、もし黒駒数が白駒数より少なかったら
        elif black < white:
            # 変数(t)に f"「{self.status[1]}」の勝利です！」" と代入する
            t = f"「{self.status[1]}」の勝利です！」"
        # そうでなければ
        else :
            # 変数(t)に "「両者引き分けでした...。」" と代入する
            t = "「両者引き分けでした...。」"
        # (f"黒{black}、白{white}により、"+t) と出力する
        print(f"黒{black}、白{white}により、"+t)

# ゲームを実行する関数(main)を作成 -> 引数(player)をbool型(初期値はTrue)で設定
def main(player:bool=True): 

    # error_message に空の文字列("")を代入する
    error_message = ""
    # クラス(boards)をオブジェクト(変数b)に代入
    b = boards()

    # ずっと繰り返す
    while True:

        # メソッド(view_board)を呼び出す
        b.view_board()
        # 改行コード("\n")を出力する
        print("\n")
        # メソッド(check_board)を呼び出し、その結果を4つの値(hint,air_exists,black,white)で受け取る
        hint,air_exists,black,white = b.check_board()

        # もし駒の置き場所が残っていなかったら
        if not air_exists:
            # メソッド(judgment)を呼び出し、勝敗判定に移る
            b.judgment(black,white)
            # ループから抜け出す
            break

        # プレイヤーが存在し、かつ現在プレイヤーのターンだったら
        if player and b.turn:
            # リスト(hint)が存在したら
            if hint:
                # リスト(hint)を用いて、駒を配置する -> 指定するxy座標はhintリストに+1する(要素番号を座標系に変換)
                b.set(b.turn,hint[-1][1]+1,hint[-1][0]+1)
                # 駒をひっくり返す -> 指定するxy座標はhintリストに+1する(要素番号を座標系に変換)
                b.swap(hint[-1][1]+1,hint[-1][0]+1)
                # ターンを切り替える
                b.turn = not b.turn
                # error_message を空にする
                error_message = ""
                # ループの残りをスキップし、ループ冒頭に戻る
                continue

        # リスト(hint)が存在しなかったら -> 駒を置ける場所が無かったら
        if not hint:
            # error_message に f"駒を置けるマスがありません。{b.status[b.turn]}のターンをスキップします。" と代入する
            error_message=f"駒を置けるマスがありません。{b.status[b.turn]}のターンをスキップします。"
            # ターンを切り替える
            b.turn = not b.turn
            # メソッド(check_board)を呼び出し、その結果を4つの値(hint,_,_,_)で受け取る -> ボードを再チェックしているよ！
            hint,_,_,_ = b.check_board()

            # リスト(hint)が存在しなかったら -> 駒を置ける場所が無かったら
            if not hint:
                # メソッド(judgment)を呼び出し、勝敗判定に移る
                b.judgment(black,white)
                # ループから抜け出す
                break
            # ループの残りをスキップし、ループ冒頭に戻る
            continue

        # f'{error_message}「{b.status[b.turn]}」の番です' と文字列を表示する
        print(f'{error_message}「{b.status[b.turn]}」の番です')
        # ("ヒント：",*hint) と文字列を出力する
        print("ヒント：",*hint)
        # ユーザーに「横 縦」の形式で入力を求め、その入力を受け取る
        # input関数でユーザーからの入力を取得し、split関数で空白で分割する
        # 分割された文字列をmap関数でint型に変換し、list関数でリストに変換する

        """ 
        1. map関数を用いる。第1引数は(int)
            - 2. 第2引数は('「横 縦」のように入力してください：')と表示し、input関数でシェルから値を受け取る
            - 3. このinput関数に対して、split関数を用い、空白を基準に値を分割する -> (x y) が (x,y)となる
        4. 1~3で作成したmap関数をlist関数で括り、iをlist型にする
        """
        # ユーザーが駒を置きたい座標を示す変数(select)を用意し、上記の手順で代入をする
        select = list(map(int, input('「横 縦」のように入力してください：').split()))
        # 改行コードを2つ("\n\n")と出力する
        print("\n\n")

        # もしiが駒の置けない座標だったら -> 指定するxy座標は逆転させ(x -> select[1], y -> select[0])、+1する(要素番号を座標系に変換)
        if not b.setable(select[1]+1,select[0]+1):
            # error_message に "このマスには駒を置けません" と代入する
            error_message = "このマスには駒を置けません"
            # ループの残りをスキップし、ループ冒頭に戻る
            continue

        # 変数(select)を用いて駒を配置する -> 指定するxy座標は逆転させ(x -> select[1], y -> select[0])、+1する(要素番号を座標系に変換)
        b.set(b.turn,select[1]+1,select[0]+1)
        # 駒をひっくり返す -> 指定するxy座標は逆転させ(x -> select[1], y -> select[0])、+1する(要素番号を座標系に変換)
        b.swap(select[1]+1,select[0]+1)
        # ターンを切り替える
        b.turn = not b.turn
        # error_message を空にする
        error_message = ""

# @@ Pythonファイルが直接実行された場合にのみ処理を実行 -> 義務的なものなのでこちらで用意
if __name__=="__main__":
    main() # @@