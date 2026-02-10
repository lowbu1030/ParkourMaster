import json
from pathlib import Path

import pygame

player_size = 40
LEVEL_WIDTH, LEVEL_HEIGHT, GROUND_Y = 10000, 7000, 300


#                          ↑GROUND_Y
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
F = False
# 障礙物
obstacles = [
    CR(pygame.Rect(275, GROUND_Y - 40, 50, 80), GRAY),  # 0
    CR(pygame.Rect(480, GROUND_Y - 130, 100, 10), PINK),
    CR(pygame.Rect(240, GROUND_Y - 180, 120, 5), DARK_GRAY),
    CR(pygame.Rect(480, GROUND_Y - 260, 120, 5), DARK_GRAY),
    CR(pygame.Rect(240, GROUND_Y - 350, 100, 10), RED_2),
    CR(pygame.Rect(170, GROUND_Y - 450, 60, 40), ORANGE),
    CR(pygame.Rect(410, GROUND_Y - 500, 200, 50), BLACK),
    CR(pygame.Rect(250, GROUND_Y - 600, 90, 10), WHITE),
    CR(pygame.Rect(200, GROUND_Y - 700, 50, 5), BLACK),
    CR(pygame.Rect(320, GROUND_Y - 700, 80, 5), BLACK),
    CR(pygame.Rect(500, GROUND_Y - 700, 50, 10), BLACK),  # 10
    CR(pygame.Rect(1180, GROUND_Y - 670, 50, 10), BLACK),
    CR(pygame.Rect(1300, GROUND_Y - 700, 100, 10), YELLOW),
    CR(pygame.Rect(1470, GROUND_Y - 780, 70, 10), YELLOW),
    CR(pygame.Rect(1300, GROUND_Y - 850, 100, 10), GREEN),
    CR(pygame.Rect(950, GROUND_Y - 980, 150, 50), WHITE),  # 雲1
    CR(pygame.Rect(900, GROUND_Y - 930, 250, 50), WHITE),
    CR(pygame.Rect(950, GROUND_Y - 880, 150, 50), WHITE),  # 到這
    CR(pygame.Rect(1900, GROUND_Y - 20, 30, 60), ORANGE, F, F),  # 要隱藏的
    CR(pygame.Rect(1900, GROUND_Y + 20, 60, 20), ORANGE, F, F),  #
    CR(pygame.Rect(2180, GROUND_Y - 20, 60, 20), BROWN, F, F),  #  20
    CR(pygame.Rect(2050, GROUND_Y - 120, 120, 10), WHITE, F, F),  #
    CR(pygame.Rect(1900, GROUND_Y - 200, 150, 10), WHITE, F, F),  #
    CR(pygame.Rect(2150, GROUND_Y - 200, 150, 10), WHITE, F, F),  #
    CR(pygame.Rect(1900, GROUND_Y - 380, 40, 10), ORANGE, F, F),  #
    CR(pygame.Rect(1900, GROUND_Y - 460, 400, 10), WHITE, F, F),  #
    CR(pygame.Rect(2050, GROUND_Y - 380, 100, 20), YELLOW, F, F),  #
    CR(pygame.Rect(2100, GROUND_Y - 650, 10, 200), WHITE, F, F),  #
    CR(pygame.Rect(1800, GROUND_Y - 300, 100, 40), BLUE),
    CR(pygame.Rect(1800, GROUND_Y - 340, 20, 60), BLUE),
    # CR(pygame.Rect(1900, GROUND_Y - 1000,  400, 1040),  BLACK),#house4
]

decorations = [
    CR(pygame.Rect(200, GROUND_Y - 700, 200, 740), BLACK),  # house1
    CR(pygame.Rect(450, GROUND_Y - 500, 160, 540), BLACK),  # house2
    CR(pygame.Rect(1250, GROUND_Y - 1300, 250, 1340), BLACK),  # house3
    CR(pygame.Rect(1900, GROUND_Y - 1000, 400, 1040), BLACK),  # house4
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
    CR(pygame.Rect(1900, GROUND_Y - 200, 400, 10), WHITE, F, F),  # 要隱藏的
    CR(pygame.Rect(2050, GROUND_Y - 120, 120, 80), WHITE, F, F),  #
    CR(pygame.Rect(2200, GROUND_Y - 20, 20, 60), BROWN, F, F),  # 桌子
    CR(pygame.Rect(2090, GROUND_Y - 460, 20, 80), YELLOW, F, F),  # 吊燈
    CR(pygame.Rect(2150, GROUND_Y - 480, 80, 20), WHITE, F, F),  # 床
    CR(pygame.Rect(2150, GROUND_Y - 480, 10, 40), WHITE, F, F),  #  設計好床
]
invisible_rects = [
    CR(pygame.Rect(500, GROUND_Y - 670, 100, 10), BLACK),
    CR(pygame.Rect(670, GROUND_Y - 670, 70, 10), BLACK),
    CR(pygame.Rect(800, GROUND_Y - 740, 70, 10), BLACK),
    CR(pygame.Rect(900, GROUND_Y - 670, 100, 10), BLACK),
    CR(pygame.Rect(1890, GROUND_Y - 1000, 10, 1040), BLACK, F, F),
    CR(pygame.Rect(2300, GROUND_Y - 1000, 10, 1040), BLACK, F, F),
    CR(pygame.Rect(2110, GROUND_Y - 650, 200, 200), WHITE, F, F),
    CR(pygame.Rect(1800, GROUND_Y - 420, 20, 110), BLUE),
    CR(pygame.Rect(1580, GROUND_Y - 360, 150, 10), YELLOW),
]

peaceful_rects = [CR(pygame.Rect(780, GROUND_Y - 360, 1000, 10), YELLOW)]
# 熔岩區域

lava = [
    CR(pygame.Rect(780, GROUND_Y - 360, 1000, 10), YELLOW),  # 放個錢幣
]

flow_lava = [
    # {"rect": pygame.Rect(4700, GROUND_Y - 310, 50, 10), "speed": 1, "y_range": (210, 310)},
]

# 紀錄點 & 技能
checkpoint_rects = [
    CR(pygame.Rect(200, GROUND_Y - 740, 20, 40), YELLOW),
    CR(pygame.Rect(1850, GROUND_Y - 340, 20, 40), YELLOW),
]
checkpoint_x, checkpoint_y = 100, GROUND_Y

invisible_checkpoint = []

teleport_point_rects = []

teleport_point_x, teleport_point_y = 100, GROUND_Y

# 敵人 list
enemies = [
    # {"rect": pygame.Rect(1000, GROUND_Y - 30, 40, 30), "speed": 2, "direction": 1, "range": (950, 1150)},
]

# 門(需要鑰匙)
doors = [{"rect": CR(pygame.Rect(2050, GROUND_Y - 60, 60, 100), BROWN), "is_open": False}]
# 鑰匙
keys2 = [{"rect": CR(pygame.Rect(800, GROUND_Y - 1050, 20, 20), PINK), "collected": False}]

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
    {"rect": CR(pygame.Rect(1500, GROUND_Y - 400, 20, 20), GOLD), "collected": False},
]
animals = []

finish_rect = CR(pygame.Rect(20000, 400, 10, 440), YELLOW)

game_state = "start screen"
gravity = 0.9
screen_color = DARK_GRAY
settings_color = RED_2
hint_color = WHITE
settings_hint_color = WHITE
floor_color = YELLOW
pull_rect_color = GREEN
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
        "gravity": 0.9,
        "screen_color": DARK_GRAY,
        "settings_color": RED_2,
        "hint_color": WHITE,
        "settings_hint_color": WHITE,
        "floor_color": YELLOW,
        "pull_rect_color": GREEN,
    },
    "obstacles": [],
    "decorations": [],
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

# 轉換移動岩漿
for flv in flow_lava:
    data["flow_lava"].append(
        {
            "rect": rect_to_list(flv["rect"].rect),
            "color": list(flv["rect"].color),
            "collide": flv["rect"].can_collide,
            "show": flv["rect"].show,
            "speed": flv["speed"],
            "y_range": flv["y_range"],
        }
    )

# 1. 取得資料夾路徑
folder_path = Path(__file__).parent.resolve()

# 2. 指定完整的「檔案路徑」（加上檔名）
# 使用 / 符號可以輕鬆連接路徑與檔名
file_path = folder_path / "lv3.json"

print(f"正在儲存至: {file_path}")

# 3. 開啟檔案路徑，而不是資料夾路徑
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
