"""
版本：v0.0.4.5
"""

import os
import pathlib
import platform as plat
import subprocess as sub
import time
from math import cos, radians, sin

import pygame as p

# 初始化 Pygame (必須先初始化才能使用字體)
p.init()

# 設定全域變數
W, H = 700, 600
T, F = True, False
s = p.display.set_mode((W, H))


def set_screen(screen: p.Surface):
    global W, H, s
    W, H = screen.get_size()
    s = screen


class CR:  # ColoredRect
    def __init__(self, rect, color, show=True, can_collide=True):
        self.rect = rect  # pygame.Rect
        self.color = color  # (R, G, B)
        self.show = show
        self.can_collide = can_collide

    def draw(self, surface):
        import pygame

        if self.show:
            pygame.draw.rect(surface, self.color, self.rect)


class Range:
    def __init__(self, start, end, num):
        self.start = start
        self.end = end
        self.num = num

    def upgrade_range(self, start, end):
        self.start = start
        self.end = end

    def upgrade_num(self, num):
        self.num = num

    def upgrade(self, start, end, num):
        self.start = start
        self.end = end
        self.num = num

    def in_range(self):
        return max(self.start, min(self.end, self.num))

    def is_in_range(self):
        return self.start <= self.num <= self.end


def num_range(min_val, max_val, num):
    """確保 num 落在 min_val 與 max_val 之間"""
    return max(min_val, min(max_val, num))


def in_range(min_val, max_val, num):
    """回傳是否在範圍內 (支援浮點數)"""
    return min_val <= num <= max_val


class Colors:
    """提供各種顏色"""

    WHITE, PINK, BLUE, BLUE2, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (0, 0, 150), (200, 100, 50)
    GREEN, DARK_GREEN, GRAY, ORANGE2 = (0, 255, 0), (0, 100, 0), (150, 150, 150), (200, 50, 0)
    RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)
    GOLD, PURPLE, DARK_GRAY, CYAN = (255, 215, 0), (128, 0, 128), (90, 90, 90), (135, 206, 235)
    BLACK2, DARK_RED = (30, 30, 30), (180, 0, 0)


def draw_rect(color, x, y, width=100, height=50, center=False, show=True):
    """單純方塊"""
    if not center:
        button_rect = p.Rect(x, num_range(y // 4, y, H // 8), width, height)
    else:
        button_rect = p.Rect(W // 2 - width // 2, y, width, height)
    p.draw.rect(s, color, button_rect)
    if show:
        return button_rect


def show_text(text, text_color, x_ratio, y_ratio, size=24, center=F, screen_center=T, font_type=""):
    """
    x_ratio, y_ratio: 傳入 0.0 ~ 1.0 的比例 (例如 0.5 代表中間)
    """
    # 1. 根據目前視窗面積動態計算字體大小 (以 600x500 為基準縮放)
    base_area = 600 * 500
    current_area = W * H
    scale_factor = (current_area / base_area) ** 0.5  # 開根號是為了讓大小隨寬高線性增長
    dynamic_size = int(size * scale_factor)
    if dynamic_size <= 0:
        dynamic_size = 1

    # 2. 設定字體
    root = pathlib.Path(__file__).parent.resolve()
    try:
        if font_type == "":
            font = p.font.Font(str(root / "Ubuntu.ttf"), dynamic_size)
        else:
            font = p.font.SysFont(font_type, dynamic_size)
    except FileNotFoundError:
        font = p.font.SysFont("arial", dynamic_size)  # 備用字體

    t_surf = font.render(text, True, text_color)
    t_rect = t_surf.get_rect()

    # 3. 根據比例計算位置
    pos_x = W * x_ratio
    pos_y = H * y_ratio

    if screen_center:
        t_rect.center = (W // 2, pos_y)
    elif center:
        t_rect.center = (pos_x, pos_y)
    else:
        t_rect.topleft = (pos_x, pos_y)

    s.blit(t_surf, t_rect)
    return t_rect


def text_button(text, text_color, color, x_ratio, y_ratio, w_ratio=0.2, h_ratio=0.1, size=24, b_center=True, font_type=""):
    """
    w_ratio: 佔螢幕寬度的比例 (0.2 = 20%)
    h_ratio: 佔螢幕高度的比例
    """
    # 1. 先計算按鈕矩形的正確位置與大小
    btn_w = int(W * w_ratio)
    btn_h = int(H * h_ratio)

    if b_center:
        # 如果要置中，x 指的是螢幕中心
        btn_x = int(W * 0.5 - btn_w // 2)
    else:
        # 如果不置中，x 依照比例計算
        btn_x = int(W * x_ratio)

    btn_y = int(H * y_ratio - btn_h // 2)
    button_rect = p.Rect(btn_x, btn_y, btn_w, btn_h)

    # 2. 畫出按鈕背景
    p.draw.rect(s, color, button_rect, border_radius=5)

    # 3. 關鍵修正：計算按鈕中心點的比例，傳給 show_text
    # 我們不再使用 show_text 的 screen_center 功能，而是直接給它中心座標
    center_x_ratio = button_rect.centerx / W
    center_y_ratio = button_rect.centery / H

    show_text(text, text_color, center_x_ratio, center_y_ratio, size=size, center=True, screen_center=False, font_type=font_type)

    return button_rect


def screen_vague(vague):
    """要放在此函式上的物件才會被模糊"""
    snapshot = s.copy()

    small = p.transform.smoothscale(snapshot, (W // vague, H // vague))
    blurred = p.transform.smoothscale(small, (W, H))
    s.blit(blurred, (0, 0))

    overlay = p.Surface((W, H))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    s.blit(overlay, (0, 0))


def os_open_file(pt):
    if plat.system() == "Windows":
        os.startfile(pt)
    elif plat.system() == "Darwin":
        sub.call(["open", pt])
    else:
        sub.call(["xdg-open", pt])


collision_time = None
start_time = None
elapsed_time = 0
paused_time = 0


def sec_timer(update=False):
    """只在遊玩時(update=True)才持續更新時間，否則保持暫停。"""
    global start_time, elapsed_time, paused_time

    if update:
        # 如果遊戲剛開始，初始化起始時間（扣除暫停過的時間）
        if start_time is None:
            start_time = time.time() - paused_time
        # 計算遊戲時間
        elapsed_time = time.time() - start_time
    else:
        # 暫停時，記錄目前經過時間（不繼續累加）
        if start_time is not None:
            paused_time = time.time() - start_time
        start_time = None
    return int(elapsed_time)


def reset_timer():
    global start_time, elapsed_time, paused_time
    start_time = None
    elapsed_time = 0
    paused_time = 0


def angle(angle):
    """
    angle 是角度 \n
    輸入angle會回傳一組dx, dy \n
    要用兩個變數來接
    """
    a = radians(angle)
    dx = cos(a)
    dy = sin(a)
    return dx, dy


def show_time_hrs(seconds):
    """
    輸入：秒數 \n
    輸出："小時：分鐘：秒數"
    """
    hrs = seconds // 3600
    mins = seconds // 60
    sec = seconds % 60
    return f"{hrs}:" + ("0" if mins % 60 < 10 else "") + f"{mins % 60}:" + ("0" if sec < 10 else "") + f"{sec}"


def show_time_min(seconds: str | float):
    """
    輸入：秒數 \n
    輸出："分鐘：秒數"
    """
    mins = seconds // 60  # type:ignore
    sec = seconds % 60
    return f"{mins}:" + ("0" if sec < 10 else "") + f"{sec}"  # type:ignore
