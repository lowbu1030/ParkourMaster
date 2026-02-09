import json
from pathlib import Path

import pygame

player_size = 40
LEVEL_WIDTH, LEVEL_HEIGHT, GROUND_Y = 7500, 7000, 300


class CR:  # ColoredRect
    def __init__(self, rect, color, show=True, can_collide=True):
        self.rect = rect  # pygame.Rect
        self.color = color  # (R, G, B)
        self.show = show
        self.can_collide = can_collide


WHITE, PINK, BLUE, BLUE2, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (0, 0, 200), (200, 100, 50)
GREEN, DARK_GREEN, GRAY, ORANGE2 = (0, 255, 0), (0, 100, 0), (150, 150, 150), (200, 50, 0)
RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)
GOLD, PURPLE, INVISIBLE = (255, 215, 0), (128, 0, 128), (0, 0, 0, 100)

# 障礙物
obstacles = [
    CR(pygame.Rect(500, GROUND_Y - 0, 40, 40), ORANGE),
    CR(pygame.Rect(800, GROUND_Y - 40, 40, 80), ORANGE),
    CR(pygame.Rect(1200, GROUND_Y - 20, 60, 60), ORANGE),
    CR(pygame.Rect(1400, GROUND_Y - 70, 50, 110), ORANGE),
    CR(pygame.Rect(1600, GROUND_Y - 20, 60, 60), ORANGE),
    CR(pygame.Rect(1800, GROUND_Y - 80, 20, 120), ORANGE),
    CR(pygame.Rect(2000, GROUND_Y - 70, 70, 10), ORANGE),
    CR(pygame.Rect(2200, GROUND_Y - 70, 70, 10), ORANGE),
    CR(pygame.Rect(2400, GROUND_Y - 80, 70, 10), ORANGE),
    CR(pygame.Rect(2600, GROUND_Y - 80, 70, 10), ORANGE),
    CR(pygame.Rect(2800, GROUND_Y - 90, 70, 10), ORANGE),
    CR(pygame.Rect(3000, GROUND_Y - 100, 70, 10), ORANGE),
    CR(pygame.Rect(3200, GROUND_Y - 120, 70, 10), ORANGE),
    CR(pygame.Rect(3400, GROUND_Y - 150, 70, 10), ORANGE),
    CR(pygame.Rect(3600, GROUND_Y - 180, 70, 10), ORANGE),
    CR(pygame.Rect(3800, GROUND_Y - 200, 70, 10), ORANGE),
    CR(pygame.Rect(4100, GROUND_Y - 80, 70, 10), ORANGE),
    CR(pygame.Rect(4450, GROUND_Y - 40, 70, 10), ORANGE),
    CR(pygame.Rect(4350, GROUND_Y - 120, 70, 10), ORANGE),
    CR(pygame.Rect(4350, GROUND_Y - 140, 10, 25), ORANGE),
    CR(pygame.Rect(4450, GROUND_Y - 180, 70, 10), ORANGE),
    CR(pygame.Rect(4350, GROUND_Y - 240, 70, 10), ORANGE),
    CR(pygame.Rect(4200, GROUND_Y - 250, 70, 10), ORANGE),
    CR(pygame.Rect(4100, GROUND_Y - 280, 70, 10), ORANGE),
    CR(pygame.Rect(3990, GROUND_Y - 340, 70, 10), ORANGE),
    CR(pygame.Rect(3800, GROUND_Y - 380, 70, 10), ORANGE),
    CR(pygame.Rect(3950, GROUND_Y - 470, 70, 10), ORANGE),
    CR(pygame.Rect(4100, GROUND_Y - 470, 70, 10), ORANGE),
    CR(pygame.Rect(4250, GROUND_Y - 470, 70, 10), ORANGE),
    CR(pygame.Rect(4400, GROUND_Y - 470, 70, 10), ORANGE),
    CR(pygame.Rect(4600, GROUND_Y - 365, 10, 10), ORANGE),
    CR(pygame.Rect(4700, GROUND_Y - 365, 10, 10), ORANGE),
    CR(pygame.Rect(4800, GROUND_Y - 365, 10, 10), ORANGE),
    CR(pygame.Rect(4900, GROUND_Y - 365, 10, 10), ORANGE),
    CR(pygame.Rect(5000, GROUND_Y - 365, 10, 10), ORANGE),
    CR(pygame.Rect(4650, GROUND_Y - 200, 550, 40), ORANGE),
    CR(pygame.Rect(5200, GROUND_Y - 400, 40, 240), ORANGE),
    CR(pygame.Rect(4550, GROUND_Y - 310, 150, 10), ORANGE),
    CR(pygame.Rect(4750, GROUND_Y - 310, 70, 10), ORANGE),
    CR(pygame.Rect(4870, GROUND_Y - 310, 70, 10), ORANGE),
    CR(pygame.Rect(4990, GROUND_Y - 310, 60, 10), ORANGE),
    CR(pygame.Rect(5300, GROUND_Y - 150, 40, 130), ORANGE),
    CR(pygame.Rect(5200, GROUND_Y - 50, 50, 10), ORANGE),
    CR(pygame.Rect(5300, GROUND_Y - 150, 130, 10), ORANGE),
    CR(pygame.Rect(5430, GROUND_Y - 270, 10, 130), ORANGE),
    CR(pygame.Rect(5550, GROUND_Y - 30, 70, 10), ORANGE),
    CR(pygame.Rect(5450, GROUND_Y - 80, 50, 10), ORANGE),
    CR(pygame.Rect(5550, GROUND_Y - 130, 70, 10), ORANGE),
    CR(pygame.Rect(5450, GROUND_Y - 170, 50, 10), ORANGE),
    CR(pygame.Rect(5550, GROUND_Y - 300, 70, 10), ORANGE),
    CR(pygame.Rect(5900, GROUND_Y - 50, 70, 10), ORANGE),
    CR(pygame.Rect(6000, GROUND_Y - 100, 70, 10), ORANGE),
    CR(pygame.Rect(6150, GROUND_Y - 150, 70, 10), ORANGE),
    CR(pygame.Rect(6250, GROUND_Y - 200, 50, 10), ORANGE),
    CR(pygame.Rect(6400, GROUND_Y - 250, 30, 10), ORANGE),
    CR(pygame.Rect(6550, GROUND_Y - 310, 70, 10), ORANGE),
    CR(pygame.Rect(6650, GROUND_Y - 1950, 70, 10), ORANGE),
    CR(pygame.Rect(6500, GROUND_Y - 1600, 70, 10), ORANGE),
    CR(pygame.Rect(6100, GROUND_Y - 1950, 70, 10), ORANGE),
    CR(pygame.Rect(5900, GROUND_Y - 1950, 70, 10), ORANGE),
    CR(pygame.Rect(5700, GROUND_Y - 1800, 50, 10), ORANGE),
    CR(pygame.Rect(5500, GROUND_Y - 1850, 70, 10), ORANGE),
    CR(pygame.Rect(4000, GROUND_Y - 1900, 1400, 10), ORANGE),
    CR(pygame.Rect(3650, GROUND_Y - 1600, 70, 10), ORANGE),
    CR(pygame.Rect(3450, GROUND_Y - 2500, 70, 10), ORANGE),
    CR(pygame.Rect(3050, GROUND_Y - 1200, 80, 80), ORANGE),
    CR(pygame.Rect(2900, GROUND_Y - 5700, 70, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 10000, 50, 10040), ORANGE),
]

peaceful_rects = [
    CR(pygame.Rect(4550, GROUND_Y - 450, 40, 490), ORANGE),
    CR(pygame.Rect(4500, GROUND_Y - 0, 60, 20), ORANGE),
    CR(pygame.Rect(4550, GROUND_Y - 310, 450, 10), ORANGE),
    CR(pygame.Rect(5750, GROUND_Y - 260, 50, 300), ORANGE),
]

lava = [
    CR(pygame.Rect(680, GROUND_Y - 0, 30, 40), RED),
    CR(pygame.Rect(1900, GROUND_Y - 0, 40, 40), RED),
    CR(pygame.Rect(2300, GROUND_Y - 0, 2000, 40), RED),
    CR(pygame.Rect(4550, GROUND_Y - 450, 40, 490), RED),
    CR(pygame.Rect(4550, GROUND_Y - 350, 500, 40), RED),
    CR(pygame.Rect(5750, GROUND_Y - 260, 50, 300), RED),
    CR(pygame.Rect(5800, GROUND_Y - 10, 950, 50), RED),
    CR(pygame.Rect(4500, GROUND_Y - 0, 60, 20), RED),
]

flow_lava = [
    {"rect": CR(pygame.Rect(4700, GROUND_Y - 310, 50, 10), RED_2), "speed": 1, "y_range": (210, 310)},
    {"rect": CR(pygame.Rect(4820, GROUND_Y - 310, 50, 10), RED_2), "speed": 1, "y_range": (210, 310)},
    {"rect": CR(pygame.Rect(4940, GROUND_Y - 310, 50, 10), RED_2), "speed": 1, "y_range": (210, 310)},
    {"rect": CR(pygame.Rect(5360, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1900, 2130)},
    {"rect": CR(pygame.Rect(5200, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1800, 2100)},
    {"rect": CR(pygame.Rect(5080, GROUND_Y - 2500, 50, 10), RED_2), "speed": 2, "y_range": (1890, 2110)},
    {"rect": CR(pygame.Rect(4980, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1840, 2050)},
    {"rect": CR(pygame.Rect(4890, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1850, 2110)},
    {"rect": CR(pygame.Rect(4840, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1870, 2080)},
    {"rect": CR(pygame.Rect(4750, GROUND_Y - 2500, 50, 10), RED_2), "speed": 2, "y_range": (1860, 2210)},
    {"rect": CR(pygame.Rect(4700, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1850, 2050)},
    {"rect": CR(pygame.Rect(4620, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1870, 2110)},
    {"rect": CR(pygame.Rect(4570, GROUND_Y - 2500, 50, 10), RED_2), "speed": 1, "y_range": (1870, 2080)},
    {"rect": CR(pygame.Rect(4490, GROUND_Y - 2500, 50, 10), RED_2), "speed": 2, "y_range": (1810, 2210)},
]

# 紀錄點 & 技能
checkpoint_rects = [
    CR(pygame.Rect(1500, GROUND_Y, 20, 40), YELLOW),
    CR(pygame.Rect(4400, GROUND_Y, 20, 40), YELLOW),
    CR(pygame.Rect(5200, GROUND_Y, 20, 40), YELLOW),
    CR(pygame.Rect(6670, GROUND_Y - 1990, 20, 40), YELLOW),
    CR(pygame.Rect(4300, GROUND_Y - 1940, 20, 40), YELLOW),
]
checkpoint_x, checkpoint_y = 100, GROUND_Y

invisible_checkpoint = [pygame.Rect(2505, GROUND_Y - 1000, 20, 40)]

teleport_point_rects = []
# 敵人 list
enemies = [
    {"rect": CR(pygame.Rect(1000, GROUND_Y + player_size - 30, 40, 30), BLACK), "speed": 2, "direction": 1, "range": (950, 1150)},
    {
        "rect": CR(pygame.Rect(4800, GROUND_Y + player_size - 30, 40, 30), BLACK),
        "speed": 3,
        "direction": -1,
        "range": (4750, 5150),
    },
]

animals = []

# 門(需要鑰匙)
doors = [
    {"rect": CR(pygame.Rect(5300, GROUND_Y + player_size - 60, 39, 60), BROWN), "is_open": False},
]
# 鑰匙
keys2 = [{"rect": CR(pygame.Rect(5400, GROUND_Y + player_size - 220, 20, 20), PINK), "collected": False}]

# 玩家是否持有鑰匙
has_key = False

portal_entrance = [
    CR(pygame.Rect(6650, GROUND_Y - 310, 50, 50), DARK_GREEN),
    CR(pygame.Rect(2700, GROUND_Y - 5700, 50, 50), DARK_GREEN),
]
portal_exit = [
    CR(pygame.Rect(6650, GROUND_Y - 2200, 50, 50), DARK_GREEN),
    CR(pygame.Rect(7000, GROUND_Y - 50, 50, 50), DARK_GREEN),
]
coins = [
    {"rect": CR(pygame.Rect(-500, GROUND_Y - 50, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(820, GROUND_Y - 140, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(3900, GROUND_Y - 320, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(5350, GROUND_Y - 320, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(6700, GROUND_Y - 1500, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(3900, GROUND_Y - 2700, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(4520, GROUND_Y + 20, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(3500, GROUND_Y - 450, 20, 20), GOLD), "collected": False},
]

finish_rect = CR(pygame.Rect(7300, GROUND_Y - 400, 10, 440), YELLOW)

decorations = []

invisible_rects = [CR(pygame.Rect(3600, GROUND_Y - 420, 70, 10), BLACK), CR(pygame.Rect(4350, GROUND_Y - 180, 10, 65), BLACK)]

game_state = "start screen"
gravity = 1
screen_color = WHITE
settings_color = BLACK
hint_color = BLACK
settings_hint_color = WHITE
floor_color = GREEN
pull_rect_color = RED
coins_count = 0
is_rainbow = []
start_text = "LEVEL 1 - On The Ground!"


def rect_to_list(rect):
    """將 pygame.Rect 轉為 [x, y, w, h] 清單"""
    return [rect.x, rect.y, rect.width, rect.height]


data = {
    "config": {
        "width": LEVEL_WIDTH,
        "height": LEVEL_HEIGHT,
        "ground_y": GROUND_Y,
        "gravity": 1,
        "screen_color": WHITE,
        "settings_color": BLACK,
        "hint_color": BLACK,
        "settings_hint_color": WHITE,
        "floor_color": GREEN,
        "pull_rect_color": RED,
    },
    "obstacles": [],
    "invisible_rects": [],
    "coins": [],
    "lava": [],
    "flow_lava": [],
    "portals_in": [],
    "portals_out": [],
}

# 轉換障礙物 (假設障礙物存在 lv1.obstacles 列表)
for ob in obstacles:
    data["obstacles"].append({"rect": rect_to_list(ob.rect), "color": list(ob.color), "collide": ob.can_collide, "show": ob.show})

for inr in invisible_rects:
    data["invisible_rects"].append(
        {"rect": rect_to_list(inr.rect), "color": list(inr.color), "collide": inr.can_collide, "show": False}
    )

# 轉換金幣
for c in coins:
    data["coins"].append({"rect": rect_to_list(c["rect"].rect), "color": list(c["rect"].color), "collected": c["collected"]})

# 轉換岩漿
for lv in lava:
    data["lava"].append({"rect": rect_to_list(lv.rect), "color": list(lv.color), "collide": lv.can_collide, "show": lv.show})

# 1. 取得資料夾路徑
folder_path = Path(__file__).parent.resolve()

# 2. 指定完整的「檔案路徑」（加上檔名）
# 使用 / 符號可以輕鬆連接路徑與檔名
file_path = folder_path / "lv1.json"

print(f"正在儲存至: {file_path}")

# 3. 開啟檔案路徑，而不是資料夾路徑
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
