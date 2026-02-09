import json
from pathlib import Path
from random import randint

import pygame

player_size = 40
LEVEL_WIDTH, LEVEL_HEIGHT, GROUND_Y = 12000, 7000, 300


class CR:  # ColoredRect
    def __init__(self, rect, color, show=True, can_collide=True):
        self.rect = rect  # pygame.Rect
        self.color = color  # (R, G, B)
        self.show = show
        self.can_collide = can_collide


WHITE, PINK, BLUE, BLUE2, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (0, 0, 200), (200, 100, 50)
GREEN, DARK_GREEN, GRAY, ORANGE2 = (0, 255, 0), (0, 100, 0), (150, 150, 150), (200, 50, 0)
RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)
GOLD, PURPLE, YELLOW2 = (255, 215, 0), (128, 0, 128), (180, 180, 0)

# 障礙物
obstacles = [
    CR(pygame.Rect(500, GROUND_Y - 0, 20, 40), BLUE),
    CR(pygame.Rect(600, GROUND_Y - 100, 20, 40), BLUE),
    CR(pygame.Rect(700, GROUND_Y - 140, 20, 40), BLUE),
    CR(pygame.Rect(600, GROUND_Y - 210, 20, 40), BLUE),
    CR(pygame.Rect(700, GROUND_Y - 260, 20, 20), BLUE),
    CR(pygame.Rect(760, GROUND_Y - 260, 10, 300), BLUE),
    CR(pygame.Rect(520, GROUND_Y - 210, 40, 20), BLUE),
    CR(pygame.Rect(1300, GROUND_Y - 80, 40, 20), BLUE),
    CR(pygame.Rect(1800, GROUND_Y - 80, 100, 10), BLUE),
    CR(pygame.Rect(1800, GROUND_Y - 150, 100, 10), BLUE),
    CR(pygame.Rect(1900, GROUND_Y - 150, 10, 80), BLUE),
    CR(pygame.Rect(1950, GROUND_Y - 200, 70, 10), BLUE),
    CR(pygame.Rect(2100, GROUND_Y - 110, 40, 10), BLUE),
    CR(pygame.Rect(2200, GROUND_Y - 150, 40, 10), BLUE),
    CR(pygame.Rect(2300, GROUND_Y - 150, 40, 10), BLUE),
    CR(pygame.Rect(2400, GROUND_Y - 180, 40, 10), BLUE),
    CR(pygame.Rect(2500, GROUND_Y - 200, 40, 10), BLUE),
    CR(pygame.Rect(2600, GROUND_Y - 240, 40, 10), BLUE),
    CR(pygame.Rect(2710, GROUND_Y - 330, 40, 10), BLUE),
    CR(pygame.Rect(2600, GROUND_Y - 400, 40, 10), BLUE),
    CR(pygame.Rect(2500, GROUND_Y - 460, 40, 10), BLUE),
    CR(pygame.Rect(2400, GROUND_Y - 530, 40, 10), BLUE),
    CR(pygame.Rect(2290, GROUND_Y - 590, 50, 10), BLUE),
    CR(pygame.Rect(2200, GROUND_Y - 640, 50, 10), BLUE),
    CR(pygame.Rect(2100, GROUND_Y - 680, 50, 10), BLUE),
    CR(pygame.Rect(2000, GROUND_Y - 700, 50, 10), BLUE),
    CR(pygame.Rect(2100, GROUND_Y - 780, 50, 10), BLUE),
    CR(pygame.Rect(2200, GROUND_Y - 800, 50, 10), BLUE),
    CR(pygame.Rect(2300, GROUND_Y - 840, 50, 10), BLUE),
    CR(pygame.Rect(2400, GROUND_Y - 840, 50, 10), BLUE),
    CR(pygame.Rect(2500, GROUND_Y - 840, 50, 10), BLUE),
    CR(pygame.Rect(2600, GROUND_Y - 840, 50, 10), BLUE),
    CR(pygame.Rect(2900, GROUND_Y - 150, 20, 10), BLUE),
    CR(pygame.Rect(3000, GROUND_Y - 150, 20, 10), BLUE),
    CR(pygame.Rect(3190, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(3380, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(3380, GROUND_Y - 1300, 130, 10), BLUE),
    CR(pygame.Rect(3500, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(3500, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(3700, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(3700, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(3800, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(3800, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(4000, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(4000, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4100, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(4100, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4300, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(4300, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4400, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4400, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(4600, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(4600, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4700, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(4700, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(4900, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(4900, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(5000, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(5000, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(5200, GROUND_Y - 1300, 110, 10), BLUE),
    CR(pygame.Rect(5200, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(5300, GROUND_Y - 1400, 10, 100), BLUE),
    CR(pygame.Rect(5300, GROUND_Y - 1400, 700, 10), BLUE),
    CR(pygame.Rect(6200, GROUND_Y - 1400, 500, 10), BLUE),
    CR(pygame.Rect(6800, GROUND_Y - 1400, 200, 10), BLUE),
    CR(pygame.Rect(7000, GROUND_Y - 1490, 10, 100), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1500, 80, 10), YELLOW),
    CR(pygame.Rect(7080, GROUND_Y - 1600, 10, 110), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1610, 90, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1710, 10, 110), YELLOW),
    CR(pygame.Rect(6880, GROUND_Y - 1550, 70, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 1670, 80, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 1780, 10, 110), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 1790, 80, 10), ORANGE),
    CR(pygame.Rect(6820, GROUND_Y - 2000, 10, 200), ORANGE),
    CR(pygame.Rect(7000, GROUND_Y - 1500, 80, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1800, 10, 200), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1610, 90, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1710, 10, 110), YELLOW),
    CR(pygame.Rect(6750, GROUND_Y - 1670, 80, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 1780, 10, 110), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 1790, 80, 10), ORANGE),
    CR(pygame.Rect(6820, GROUND_Y - 1890, 10, 110), ORANGE),
    CR(pygame.Rect(6880, GROUND_Y - 1700, 70, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1800, 90, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 1910, 90, 10), YELLOW),
    CR(pygame.Rect(7080, GROUND_Y - 1910, 10, 110), YELLOW),
    CR(pygame.Rect(6880, GROUND_Y - 1890, 70, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 2000, 80, 10), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 2110, 10, 110), ORANGE),
    CR(pygame.Rect(6750, GROUND_Y - 2110, 80, 10), ORANGE),
    CR(pygame.Rect(6820, GROUND_Y - 2300, 10, 200), ORANGE),
    CR(pygame.Rect(6880, GROUND_Y - 2050, 70, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 2100, 10, 200), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 2100, 90, 10), YELLOW),
    CR(pygame.Rect(7000, GROUND_Y - 2200, 90, 10), YELLOW),
    CR(pygame.Rect(7080, GROUND_Y - 2200, 10, 110), YELLOW),
    CR(pygame.Rect(6650, GROUND_Y - 1850, 40, 10), BLUE),
    CR(pygame.Rect(6370, GROUND_Y - 1850, 50, 10), BLUE),
    CR(pygame.Rect(6150, GROUND_Y - 1950, 50, 10), ORANGE2),
    CR(pygame.Rect(6000, GROUND_Y - 1800, 70, 10), ORANGE2),
    CR(pygame.Rect(5900, GROUND_Y - 1850, 70, 10), BLUE),
    CR(pygame.Rect(5800, GROUND_Y - 1950, 50, 10), RED),
    CR(pygame.Rect(7400, GROUND_Y - 4000, 50, 4040), GREEN),
    CR(pygame.Rect(6000, GROUND_Y - 2200, 10, 200), GREEN),
]

peaceful_rects = []

lava = [
    CR(pygame.Rect(800, GROUND_Y - 0, 90, 40), RED),
    CR(pygame.Rect(960, GROUND_Y + 20, 130, 20), RED),
    CR(pygame.Rect(2780, GROUND_Y - 500, 50, 540), RED),
    CR(pygame.Rect(3100, GROUND_Y - 150, 50, 190), RED),
    CR(pygame.Rect(3100, GROUND_Y - 10, 4000, 50), RED),
    CR(pygame.Rect(5600, GROUND_Y - 1480, 300, 50), RED),
    CR(pygame.Rect(6370, GROUND_Y - 1650, 300, 10), RED),
    CR(pygame.Rect(6000, GROUND_Y - 1950, 70, 10), BLUE),
    CR(pygame.Rect(9200, GROUND_Y - 10, 800, 50), BLACK),
]

flow_lava = [
    {"rect": CR(pygame.Rect(3300, GROUND_Y - 1700, 2000, 10), RED_2), "speed": 1, "y_range": (1430, 1600)},
    {"rect": CR(pygame.Rect(6830, GROUND_Y - 2400, 170, 10), RED_2), "speed": 2, "y_range": (1430, 2400)},
    {"rect": CR(pygame.Rect(6830, GROUND_Y - 1400, 170, 10), RED_2), "speed": 1, "y_range": (1430, 2400)},
    {"rect": CR(pygame.Rect(7600, GROUND_Y - 300, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7650, GROUND_Y - 100, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7700, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7750, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7800, GROUND_Y - 215, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7850, GROUND_Y - 301, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7900, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(7950, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8000, GROUND_Y - 100, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8050, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8100, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8150, GROUND_Y - 215, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8200, GROUND_Y - 301, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8250, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8300, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8350, GROUND_Y - 215, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8400, GROUND_Y - 301, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8450, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8500, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8550, GROUND_Y - 100, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8600, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8650, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8700, GROUND_Y - 215, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8750, GROUND_Y - 301, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8800, GROUND_Y - 250, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
    {"rect": CR(pygame.Rect(8850, GROUND_Y - 352, 50, 10), RED_2), "speed": 1, "y_range": (-20, randint(90, 320))},
]

# 紀錄點 & 技能
checkpoint_rects = [
    CR(pygame.Rect(3000, GROUND_Y - 190, 20, 40), YELLOW),
    CR(pygame.Rect(5950, GROUND_Y - 1440, 20, 40), YELLOW),
    CR(pygame.Rect(6650, GROUND_Y - 1890, 20, 40), YELLOW),
    CR(pygame.Rect(7550, GROUND_Y - 0, 20, 40), YELLOW),
]
checkpoint_x, checkpoint_y = 100, GROUND_Y

invisible_checkpoint = [CR(pygame.Rect(1920, GROUND_Y - 820, 20, 40), BLACK), CR(pygame.Rect(9100, GROUND_Y - 0, 20, 40), BLACK)]

teleport_point_rects = []

# 敵人 list
enemies = [
    {"rect": CR(pygame.Rect(6250, GROUND_Y - 1430, 40, 30), PURPLE), "speed": 1, "direction": 1, "range": (6200, 6700)},
    {"rect": CR(pygame.Rect(6500, GROUND_Y - 1430, 40, 30), PURPLE), "speed": 2, "direction": 1, "range": (6200, 6700)},
]

animals = [
    {"rect": CR(pygame.Rect(9500, GROUND_Y - 140, 40, 30), ORANGE), "speed": 1, "direction": 1, "range": (9500, 9680)},
]

# 門(需要鑰匙)
doors = [{"rect": CR(pygame.Rect(1800, GROUND_Y - 140, 40, 60), BROWN), "is_open": False}]
# 鑰匙
keys2 = [{"rect": CR(pygame.Rect(1400, GROUND_Y - 250, 20, 20), PINK), "collected": False}]

# 玩家是否持有鑰匙
has_key = False

portal_entrance = [
    CR(pygame.Rect(3200, GROUND_Y - 150, 50, 50), PURPLE),
    CR(pygame.Rect(7050, GROUND_Y - 2300, 50, 50), YELLOW2),
    CR(pygame.Rect(5900, GROUND_Y - 2100, 50, 50), PURPLE),
]

portal_exit = [
    CR(pygame.Rect(3200, GROUND_Y - 1500, 50, 50), PURPLE),
    CR(pygame.Rect(6750, GROUND_Y - 1850, 50, 50), YELLOW2),
    CR(pygame.Rect(7490, GROUND_Y - 10, 50, 50), PURPLE),
]

# 錢幣系統 - 增加更多錢幣
coins = [
    {"rect": CR(pygame.Rect(525, GROUND_Y - 220, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(1850, GROUND_Y - 120, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(2000, GROUND_Y - 400, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(3245, GROUND_Y - 600, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(6700, GROUND_Y - 1700, 20, 20), GOLD), "collected": False},
    {"rect": CR(pygame.Rect(9640, GROUND_Y - 230, 20, 20), BLACK), "collected": False},
]

decorations = [
    CR(pygame.Rect(6420, GROUND_Y - 1850, 50, 10), ORANGE2),
    CR(pygame.Rect(6150, GROUND_Y - 1750, 50, 10), BLUE),
]

invisible_rects = [
    CR(pygame.Rect(9250, GROUND_Y - 80, 70, 10), GRAY),
    CR(pygame.Rect(9400, GROUND_Y - 120, 70, 10), GRAY),
    CR(pygame.Rect(9500, GROUND_Y - 140, 180, 10), GRAY),
    CR(pygame.Rect(9730, GROUND_Y - 140, 68, 10), GRAY),
    CR(pygame.Rect(9850, GROUND_Y - 170, 50, 10), GRAY),
]

finish_rect = CR(pygame.Rect(10500, GROUND_Y - 400, 10, 440), YELLOW)

gravity = 0.8
screen_color = BLACK
settings_color = BLUE2
hint_color = BLUE2
settings_hint_color = WHITE
floor_color = ORANGE2
pull_rect_color = RED
coins_count = 0
is_rainbow = []
start_text = "LEVEL 2 - Space Adventure!"


def rect_to_list(rect):
    """將 pygame.Rect 轉為 [x, y, w, h] 清單"""
    return [rect.x, rect.y, rect.width, rect.height]


data = {
    "config": {
        "width": LEVEL_WIDTH,
        "height": LEVEL_HEIGHT,
        "ground_y": GROUND_Y,
        "gravity": 0.8,
        "screen_color": BLACK,
        "settings_color": BLUE2,
        "hint_color": BLUE2,
        "settings_hint_color": WHITE,
        "floor_color": ORANGE2,
        "pull_rect_color": RED,
    },
    "obstacles": [],
    "decorations": [],
    "invisible_rects": [],
    "coins": [],
    "lava": [],
    "portals_in": [],
    "portals_out": [],
}

# 轉換障礙物 (假設障礙物存在 lv1.obstacles 列表)
for ob in obstacles:
    data["obstacles"].append({"rect": rect_to_list(ob.rect), "color": list(ob.color), "collide": ob.can_collide, "show": ob.show})

for dc in decorations:
    data["decorations"].append({"rect": rect_to_list(dc.rect), "color": list(dc.color), "collide": False, "show": dc.show})

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
file_path = folder_path / "lv2.json"

print(f"正在儲存至: {file_path}")

# 3. 開啟檔案路徑，而不是資料夾路徑
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
