import json
from pathlib import Path

import pygame

player_size = 40
LEVEL_WIDTH, LEVEL_HEIGHT, GROUND_Y = 10000, 7000, 300


class CR:  # ColoredRect
    def __init__(self, rect, color, show=True, can_collide=True):
        self.rect = rect  # pygame.Rect
        self.color = color  # (R, G, B)
        self.show = show
        self.can_collide = can_collide


WHITE, PINK, BLUE, BLUE2, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (0, 0, 200), (200, 100, 50)
GREEN, DARK_GREEN, GRAY, ORANGE2 = (0, 255, 0), (0, 100, 0), (150, 150, 150), (200, 50, 0)
RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)
GOLD, PURPLE, YELLOW2, DARK_GRAY = (255, 215, 0), (128, 0, 128), (180, 180, 0), (90, 90, 90)

# 障礙物
obstacles = [
    CR(pygame.Rect(275, GROUND_Y - 40, 50, 80), GRAY),
    CR(pygame.Rect(480, GROUND_Y - 130, 100, 10), PINK),
    CR(pygame.Rect(240, GROUND_Y - 180, 120, 5), DARK_GRAY),
    CR(pygame.Rect(480, GROUND_Y - 260, 120, 5), DARK_GRAY),
    CR(pygame.Rect(240, GROUND_Y - 350, 100, 10), RED_2),
    CR(pygame.Rect(170, GROUND_Y - 450, 60, 40), ORANGE),
    CR(pygame.Rect(410, GROUND_Y - 500, 200, 50), BLACK),
    CR(pygame.Rect(250, GROUND_Y - 600, 90, 10), WHITE),
    CR(pygame.Rect(200, GROUND_Y - 700, 50, 5), BLACK),
    CR(pygame.Rect(320, GROUND_Y - 700, 80, 5), BLACK),
    CR(pygame.Rect(500, GROUND_Y - 700, 50, 10), BLACK),
    CR(pygame.Rect(1180, GROUND_Y - 670, 50, 10), BLACK),
    CR(pygame.Rect(1300, GROUND_Y - 700, 100, 10), YELLOW),
    CR(pygame.Rect(1470, GROUND_Y - 780, 70, 10), YELLOW),
    CR(pygame.Rect(1300, GROUND_Y - 850, 100, 10), GREEN),
]

peaceful_rects = []

lava = [
    CR(pygame.Rect(780, GROUND_Y - 360, 1000, 10), YELLOW),  # 放個錢幣
]

flow_lava = [
    # {"rect": pygame.Rect(4700, GROUND_Y - 310, 50, 10), "speed": 1, "y_range": (210, 310)},
]

# 紀錄點 & 技能
checkpoint_rects = [CR(pygame.Rect(200, GROUND_Y - 740, 20, 40), YELLOW)]
checkpoint_x, checkpoint_y = 100, GROUND_Y

invisible_checkpoint = []

teleport_point_rects = []

teleport_point_x, teleport_point_y = 100, GROUND_Y

# 敵人 list
enemies = [
    # {"rect": pygame.Rect(1000, GROUND_Y - 30, 40, 30), "speed": 2, "direction": 1, "range": (950, 1150)},
]

# 門(需要鑰匙)
doors = [
    # {"rect": pygame.Rect(1800, GROUND_Y - 140, 40, 60), "is_open": False}
]
# 鑰匙
keys2 = [
    # {"rect": pygame.Rect(1400, GROUND_Y - 300, 20, 20), "collected": False}
]

# 玩家是否持有鑰匙
has_key = False

portal_entrance = [
    # pygame.Rect(6650, GROUND_Y - 310, 50, 50),
]
portal_exit = [
    # pygame.Rect(6650, GROUND_Y - 2200, 50, 50),
]

# 錢幣系統 - 增加更多錢幣
coins = [
    # {"rect": pygame.Rect(525, GROUND_Y - 220, 20, 20), "collected": False},
]

decorations = [
    CR(pygame.Rect(200, GROUND_Y - 700, 200, 740), BLACK),  # house1
    CR(pygame.Rect(450, GROUND_Y - 500, 160, 540), BLACK),  # house2
    CR(pygame.Rect(1250, GROUND_Y - 1300, 250, 1340), BLACK),  # house3
    CR(pygame.Rect(500, GROUND_Y - 40, 50, 80), GRAY),
    CR(pygame.Rect(480, GROUND_Y - 180, 100, 10), PINK),  # 窗戶
    CR(pygame.Rect(480, GROUND_Y - 180, 10, 100), PINK),
    CR(pygame.Rect(480, GROUND_Y - 80, 100, 10), PINK),
    CR(pygame.Rect(530, GROUND_Y - 180, 10, 100), PINK),
    CR(pygame.Rect(580, GROUND_Y - 180, 10, 110), PINK),  # 到這
    CR(pygame.Rect(240, GROUND_Y - 180, 120, 50), DARK_GRAY),
    CR(pygame.Rect(480, GROUND_Y - 260, 120, 50), DARK_GRAY),
    CR(pygame.Rect(240, GROUND_Y - 400, 100, 10), RED_2),  # 窗戶
    CR(pygame.Rect(240, GROUND_Y - 400, 10, 100), RED_2),
    CR(pygame.Rect(240, GROUND_Y - 300, 100, 10), RED_2),
    CR(pygame.Rect(290, GROUND_Y - 400, 10, 100), RED_2),
    CR(pygame.Rect(340, GROUND_Y - 400, 10, 110), RED_2),  # 到這
    CR(pygame.Rect(520, GROUND_Y - 700, 10, 200), BLACK),
    CR(pygame.Rect(500, GROUND_Y - 670, 50, 10), BLACK),
    CR(pygame.Rect(500, GROUND_Y - 640, 50, 10), BLACK),
    CR(pygame.Rect(500, GROUND_Y - 670, 700, 10), YELLOW),
    CR(pygame.Rect(800, GROUND_Y - 400, 10, 440), BLACK),  # 電線桿1
    CR(pygame.Rect(780, GROUND_Y - 400, 50, 10), BLACK),  #
    CR(pygame.Rect(780, GROUND_Y - 360, 50, 10), BLACK),  #
    CR(pygame.Rect(780, GROUND_Y - 320, 50, 10), BLACK),  #
    CR(pygame.Rect(1750, GROUND_Y - 400, 10, 440), BLACK),  # 電線桿2
    CR(pygame.Rect(1730, GROUND_Y - 400, 50, 10), BLACK),  #
    CR(pygame.Rect(1730, GROUND_Y - 360, 50, 10), BLACK),  #
    CR(pygame.Rect(1730, GROUND_Y - 320, 50, 10), BLACK),  #
    CR(pygame.Rect(1200, GROUND_Y - 700, 10, 740), BLACK),
    CR(pygame.Rect(1180, GROUND_Y - 640, 50, 10), BLACK),
    CR(pygame.Rect(1180, GROUND_Y - 700, 50, 10), BLACK),
    CR(pygame.Rect(1300, GROUND_Y - 950, 100, 10), GREEN),  # 窗戶
    CR(pygame.Rect(1300, GROUND_Y - 950, 10, 100), GREEN),
    CR(pygame.Rect(1300, GROUND_Y - 900, 100, 10), GREEN),
    CR(pygame.Rect(1350, GROUND_Y - 950, 10, 100), GREEN),
    CR(pygame.Rect(1400, GROUND_Y - 950, 10, 110), GREEN),  # 到這
    CR(pygame.Rect(1470, GROUND_Y - 780, 70, 50), ORANGE),
]
invisible_rects = [
    CR(pygame.Rect(500, GROUND_Y - 670, 100, 10), BLACK),
    CR(pygame.Rect(670, GROUND_Y - 670, 70, 10), BLACK),
    CR(pygame.Rect(800, GROUND_Y - 740, 70, 10), BLACK),
    CR(pygame.Rect(900, GROUND_Y - 670, 100, 10), BLACK),
]
animals = []

finish_rect = CR(pygame.Rect(20000, 400, 10, 440), YELLOW)

game_state = "start screen"
gravity = 1.2
screen_color = BLACK
settings_color = DARK_GREEN
hint_color = YELLOW
settings_hint_color = WHITE
floor_color = WHITE
pull_rect_color = RED
coins_count = 0
is_rainbow = []
start_text = "LEVEL 3 - City Parkour!"


def rect_to_list(rect):
    """將 pygame.Rect 轉為 [x, y, w, h] 清單"""
    return [rect.x, rect.y, rect.width, rect.height]


data = {
    "config": {
        "width": LEVEL_WIDTH,
        "height": LEVEL_HEIGHT,
        "ground_y": GROUND_Y,
        "gravity": 1.2,
        "screen_color": BLACK,
        "settings_color": DARK_GREEN,
        "hint_color": YELLOW,
        "settings_hint_color": WHITE,
        "floor_color": WHITE,
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
file_path = folder_path / "lv4.json"

print(f"正在儲存至: {file_path}")

# 3. 開啟檔案路徑，而不是資料夾路徑
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
