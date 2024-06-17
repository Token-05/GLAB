import tkinter as tk
from random import randint

root = tk.Tk()
root.title("mine sweeper")

sqr = 50  # ますの大きさ
pdg = 10  # パディング（画面周りの空白の大きさ）
width = 30  # x方向のますの数
height = 15  # y方向のますの数
level = 1  # レベル

map_state = {'space': 0, 'bomb': 1}  # マップのステータス
btn_state = {'pressed': 0, 'not_pressed': 1, 'flagged': 2}  # ボタンのステータス

screen_WIDTH = sqr * width + pdg * 2
screen_HEIGHT = sqr * height + pdg * 2

root.geometry(f"{screen_WIDTH}x{screen_HEIGHT}")
canvas = tk.Canvas(root, width=screen_WIDTH, height=screen_HEIGHT, bg="#f0f85f")

def hide_button(event):
    event.widget.place_forget()

def flag_button(event):
    event.widget.config(bg="red")

maps = []
for _ in range(height):
    maps_col = []
    for _ in range(width):
        if randint(level, 50) < 45:
            maps_col.append(map_state['space'])
        else:
            maps_col.append(map_state['bomb'])
    maps.append(maps_col)

for i in range(height):
    for j in range(width):
        b = tk.Button(
            root,
            text=None,
            bg="#222222",
            padx=pdg,
            pady=pdg
        )
        b.bind("<Button-1>", hide_button)
        b.bind("<Button-3>", flag_button)
        b.place(
            x=sqr * j + pdg,
            y=sqr * i + pdg,
            width=50,
            height=50,
        )

root.mainloop()
print(maps)
