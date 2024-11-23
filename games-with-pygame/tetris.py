import pygame
from pygame.locals import *
import random

"""
# テトリス - 2024/11/23 - T.Ichiyanagi

- Board: ボードを管理するクラス、動かせないミノとボードに関する情報を持つ
- MINO: ミノを管理するクラス、動くミノについての情報を持つ
"""

class Board:
    """
    ボードクラス
    """
    
    def __init__(self):
        """
        ボードを管理するリストを定義
        """
        self.board = []
    
    def initBoard(self):
        """
        ボードを初期化
        """
        # 縦方向に繰り返す
        for _ in range(GRID_HEIGHT):
            temp = []
            # 横方向に繰り返す
            for _ in range(GRID_WIDTH):
                # 横方向の全要素に黒色を追加
                temp.append(BLACK)
            # 縦方向にも同じく追加
            self.board.append(temp)
    
    def add_mino(self, mino_class):
        """
        動かせなくなったミノをボードに追加

        Args:
            mino_class (MINO): ミノインスタンス
        """
        # ミノインスタンスに対して、x,y座標とミノ情報を取り出す
        x, y = mino_class.x, mino_class.y
        mino = mino_class.mino
        # ミノ形状リストの縦方向について繰り返す
        for i, row in enumerate(mino['shape']):
            # ミノ形状リストの横方向について繰り返す
            for j, value in enumerate(row):
                # ボードの範囲内であることを確認する
                if 0 <= y + i < len(self.board) and 0 <= x + j < len(self.board[0]) and value:
                    # ボードにミノを追加（実際には色情報を変更するだけ）
                    self.board[y + i][x + j] = mino['color']

    def draw(self):
        """
        グリッドおよびミノを描画
        """
        # 縦方向に繰り返す
        for y in range(GRID_HEIGHT):
            # 横方向に繰り返す
            for x in range(GRID_WIDTH):
                # ボードリストの色情報に従って四角く塗りつぶす
                pygame.draw.rect(SCREEN, self.board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                # 太さ1でグレーの枠線で囲む
                pygame.draw.rect(SCREEN, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    def line_check_and_drop(self):
        """
        行をチェックし消せるなら消す
        """
        # 消せる行インデックスを格納するためリスト
        waste = []
        # 縦方向に繰り返す
        for y in range(GRID_HEIGHT):
            # 横方向についてブロックが隙間なく詰まっていれば以下へ続く
            if BLACK not in self.board[y]:
                # 消せる行として登録
                waste.append(y)
        # 消せる行として登録したものについて、全て削除
        for w in waste:
            self.board.pop(w)
            # 先頭に空の行（つまり全部BLACKの要素）を追加
            self.board.insert(0,[BLACK for _ in range(GRID_WIDTH)])


class MINO:
    """
    ミノクラス
    """
    
    # ミノの形状と色についてそれぞれ辞書で定義
    minos = {
        "I": {
            'shape': [[1, 1, 1, 1]],
            'color': (0, 255, 255)
        },
        "O": {
            'shape': [[1, 1],[1, 1]],
            'color': (255, 255, 0)
        },
        "T": {
            'shape': [[0, 1, 0],[1, 1, 1]],
            'color': (128, 0, 128)
        },
        "S": {
            'shape': [[0, 1, 1],[1, 1, 0]],
            'color': (0, 255, 0)
        },
        "Z": {
            'shape': [[1, 1, 0],[0, 1, 1]],
            'color': (255, 0, 0)
        },
        "J": {
            'shape': [[1, 0, 0],[1, 1, 1]],
            'color': (0, 0, 255)
        },
        "L": {
            'shape': [[0, 0, 1],[1, 1, 1]],
            'color': (255, 165, 0)
        }
    }
    
    def __init__(self, shape, x, y):
        """
        形状とx,y座標をそれぞれ変数として定義

        Args:
            shape (str): 形状を挿入
            x (int): x座標、0~9
            y (int): y座標、0~19
        """
        self.mino = self.minos[shape]
        self.x = x
        self.y = y

    def move(self, board, dx, dy):
        """
        ミノを移動

        Args:
            board (Board): ボードクラス
            dx (int): x方向の移動量
            dy (int): y方向の移動量
        """
        # 移動時に重なりがないかをチェックし、なければ移動
        self.x, self.y = self._movement_overlap_correction(board, dx, dy)
        # 枠外判定もちゃんとするよ
        self._out_of_box_correction()

    def rotate(self, board):
        """
        ミノを回転（時計回り）

        Args:
            board (Board): ボードクラス
        """
        # 回転時に重なりがないかをチェックし、なければ回転
        self.mino['shape'] = self._rotational_overlap_correction(board)
        # 枠外判定〜
        self._out_of_box_correction()
    
    def _movement_overlap_correction(self, board, dx, dy):
        """
        移動時における衝突チェック

        Args:
            board (Board): ボードクラス
            dx (int): x方向の移動量
            dy (int): y方向の移動量

        Returns:
            tuple: 移動できそうれあれば `(x,y)` 座標を更新して返す
        """
        # 更新したい暫定の座標
        temp_x = self.x + dx
        temp_y = self.y + dy
        # 下に到達したかを確定するためのフラグ
        global FLAG
        # ミノ形状の縦方向について繰り返す
        for i, row in enumerate(self.mino['shape']):
            # ミノ形状の横方向について繰り返す
            for j, cell in enumerate(row):
                # もし領域内がセルであればいかに続く
                if cell:
                    # ボードの範囲内であることを確認できなければ更新せずに返す
                    if not (0 <= temp_y + i < len(board.board) and 0 <= temp_x + j < len(board.board[0])):
                        return self.x, self.y
                    # すでにブロックが存在するなら更新せずに返す
                    if board.board[temp_y + i][temp_x + j] != BLACK:
                        # dyの更新があればフラグを立てておく ⇨ これがないとブロックが落ちてこないぜー
                        if dy > 0:
                            FLAG = True
                        return self.x, self.y
        # 特に何もなければ更新して返す
        return temp_x, temp_y

    def _rotational_overlap_correction(self, board):
        """
        回転時における衝突チェック

        Args:
            board (Board): 親の顔より見たボードクラス

        Returns:
            list: 移動できそうであれば回転して返す
        """
        # 回転したい暫定の形状（興味あればなぜ1行で回転できるかを調べてもいいかも）
        temp = [list(row) for row in zip(*self.mino['shape'][::-1])]
        # ミノ形状の縦方向について繰り返す
        for i, row in enumerate(temp):
            # ミノ形状の横方向について繰り返す
            for j, cell in enumerate(row):
                # もし領域内がセルであればいかに続く
                if cell:
                    # ボードの範囲内であることを確認できなければ更新せずに返す
                    if not (0 <= self.x + j < len(board.board[0]) and 0 <= self.y + i < len(board.board)):
                        return self.mino['shape']
                    # すでにブロックが存在するなら更新せずに返す
                    if board.board[self.y + i][self.x + j] != BLACK:
                        return self.mino['shape']
        # 特に何もなければ更新して返す
        return temp
    
    def _out_of_box_correction(self):
        """
        枠外補正（回転や移動の際にチェック）
        """
        # ミノの幅
        yoko = len(self.mino['shape'][0])
        # ミノの高さ
        tate = len(self.mino['shape'])
        
        # 右端から出た時の処理（基本maxに寄せる）
        if self.x + yoko > GRID_WIDTH:
            self.x = GRID_WIDTH - yoko
        # 左端から出た時の処理
        elif self.x < 0:
            self.x = 0
        # 下端から出た時の処理
        if self.y + tate > GRID_HEIGHT:
            self.y = GRID_HEIGHT - tate
        # 上端から出た時の処理（これは普通起きない現象）
        elif self.y < 0:
            self.y = 0
    
    def draw(self):
        """
        ミノを描画
        """
        # ミノ形状の縦方向について繰り返す
        for row_idx, row in enumerate(self.mino['shape']):
            # ミノ形状の横方向について繰り返す
            for col_idx, cell in enumerate(row):
                # もし領域内がセルであればいかに続く
                if cell:
                    # セルの描画（ミノクラスに指定された色と座標に気をつける）
                    pygame.draw.rect(
                        SCREEN,
                        self.mino['color'],
                        ((self.x + col_idx) * BLOCK_SIZE, (self.y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    # セルの枠描画（色はグレー、座標は上と同じ、width引数に気をつける(1にしとけばOK)）
                    pygame.draw.rect(
                        SCREEN,
                        GRAY,
                        ((self.x + col_idx) * BLOCK_SIZE, (self.y + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                        1
                    )



def main():
    """
    メイン処理
    """
    # 初期設定
    pygame.init()
    
    # 変数設定（メイン関数ないで定義したけど外でも使いそうな変数はここに入れとけばOK）
    global GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, WHITE, GRAY, BLACK, FLAG

    ## 画面設定（グローバル設定も行う）
    # 盤面の縦・横それぞれのブロック数
    GRID_WIDTH, GRID_HEIGHT = 10, 20
    # セル1つのサイズ
    BLOCK_SIZE = 30
    # スクリーンの横幅、何かと何かをかけるよ
    SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
    # スクリーンの縦幅、何かと何かをかけるよ
    SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
    # スクリーンをセット！
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # キャプションを定義
    pygame.display.set_caption("Tetris")
    
    # 色設定（白と黒とグレー。設定した理由：何度か使うから）
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (50, 50, 50)
    
    # 下に到達したかを確定するためのフラグ
    FLAG = False
    
    # 初期化
    clock = pygame.time.Clock()
    
    # タイマーイベント（1秒ごとにイベント発生）
    DROP_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(DROP_EVENT, 1000)
    
    # ボードをインスタンス化する
    board = Board()
    # さらにボードを初期化
    board.initBoard()
    # ミノをランダムに選ぶ
    shape = random.choice(['I','O','T','S','Z','L','J'])
    # 選んだミノを中央上部に配置
    mino = MINO(shape, 3, 0)

    # runnning変数を定義、Trueである間はループし、止めたくなったらFalseにすれば良い
    running = True
    while running:
        
        # 行チェックを実行する
        board.line_check_and_drop()

        ## イベント処理
        # 長押し限定：下ボタンが押されている間はブロックが早く降りるようにする
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_DOWN]: mino.move(board, 0, 1)
        # 1度押し限定：下ボタン以外
        for event in pygame.event.get():
            # 止めるボタン（左上の❌）
            if event.type == pygame.QUIT:
                running = False
            # キーが押された時の処理
            elif event.type == pygame.KEYDOWN:
                # 左ボタンの時は左にミノを移動
                if event.key == pygame.K_LEFT:
                    mino.move(board, -1, 0)
                # 右ボタンの時は右にミノを移動
                elif event.key == pygame.K_RIGHT:
                    mino.move(board, 1, 0)
                # 上ボタンの時はミノを回転
                elif event.key == pygame.K_UP:
                    mino.rotate(board)
            # 1秒経ったらミノを1ブロック分落とす（自然落下イベント）
            elif event.type == DROP_EVENT:
                mino.move(board, 0, 1)

        # ボード・ミノを両方描画
        board.draw()
        mino.draw()
        
        # 下に到達したかを確定するためのフラグがTrueであればいかに続く
        if FLAG or mino.y + len(mino.mino['shape']) >= GRID_HEIGHT:
            # ミノをボードに追加（もう動けないからね）
            board.add_mino(mino)
            # ミノをランダムに選ぶ
            shape = random.choice(['I','O','T','S','Z','L','J'])
            # 選んだミノを中央上部に配置
            mino = MINO(shape, 3, 0)
            # フラグは戻しておく
            FLAG = False

        # ディスプレイを更新する（30msごとに）
        pygame.display.flip()
        clock.tick(30)

    # whileから抜けるということはゲーム自体を閉じるということ
    pygame.quit()

# おまじない
if __name__ == "__main__":
    main()
