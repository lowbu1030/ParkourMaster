import json
import os

import pygame

import tool

WIDTH, HEIGHT = 600, 450

ACH_FILE = "achievements.json"
# 所有顏色
WHITE, PINK, BLUE, BLUE2, BROWN = (255, 255, 255), (255, 0, 255), (0, 0, 255), (0, 0, 200), (200, 100, 50)
GREEN, DARK_GREEN, GRAY, ORANGE2 = (0, 255, 0), (0, 100, 0), (150, 150, 150), (200, 50, 0)
RED, RED_2, ORANGE, BLACK, YELLOW = (255, 0, 0), (215, 0, 0), (255, 100, 0), (0, 0, 0), (255, 255, 0)
GOLD, PURPLE, DARK_GRAY = (255, 215, 0), (128, 0, 128), (90, 90, 90)

# 🎯 預設成就清單
DEFAULT_ACHIEVEMENTS = {
    "first_jump": {"name": "First Jump!", "desc": "完成第一次跳躍。", "unlocked": False},
    "try it again": {"name": "Try It Again!", "desc": "在第一關第一次死亡。", "unlocked": False},
    "check it out!": {"name": "Check It Out!", "desc": "碰到第一個紀錄點。", "unlocked": False},
    "let's become rich": {"name": "Let's Become Rich", "desc": "拿到第一塊錢。", "unlocked": False},
    "first_try": {"name": "First Try!", "desc": "完成第一關。", "unlocked": False},
    "help!! I can't!!": {"name": "Help!! I can't!!", "desc": "死亡100次。", "unlocked": False},
    "Lv1 coin_master": {"name": "Lv1 Coin Master", "desc": "收集第一關 7 枚金幣。", "unlocked": False},
    "deathless": {"name": "Deathless", "desc": "未死亡完成一關。", "unlocked": False},
    "parkour master": {"name": "Parkour Master", "desc": "再不死亡的情況下且在100秒內通關", "unlocked": False},
    "oops!": {"name": "Oops!", "desc": "在第二關第一次死亡。", "unlocked": False},
    # 通過特殊地點獲得的成就
    "it's hot!": {"name": "It's hot!", "desc": "通過第一關岩漿。", "unlocked": False},
    "where are you going?": {"name": "Where Are You Going?", "desc": "走到-1500以外的地方", "unlocked": False},
    # 特殊模式下可以達成的成就
    "rainbow player": {"name": "Rainbow_Player", "desc": "以彩虹模式完成關卡。", "unlocked": False},
    "rainbow's proud": {"name": "Rainbow's Proud", "desc": "以彩虹模式完成關卡且不死亡。", "unlocked": False},
    "I can't see you!": {"name": "I Can't See You!", "desc": "以隱形模式完成關卡。", "unlocked": False},
    "vague": {"name": "Vague", "desc": "打開困難模式。", "unlocked": False},
    "I'm blind!!": {"name": "I'm Blind!!", "desc": "打開超級困難模式。", "unlocked": False},
}


# ✅ 載入 / 建立成就檔
def load_achievements():
    # 檢查檔案是否存在且不為空
    if not os.path.exists(ACH_FILE) or os.path.getsize(ACH_FILE) == 0:
        save_achievements(DEFAULT_ACHIEVEMENTS)
        return DEFAULT_ACHIEVEMENTS

    try:
        with open(ACH_FILE, encoding="utf-8") as f:
            data = json.load(f)
            # 檢查資料是否為空字典或無效
            if not data:
                save_achievements(DEFAULT_ACHIEVEMENTS)
                return DEFAULT_ACHIEVEMENTS
            return data
    except (json.JSONDecodeError, ValueError):
        # 如果 JSON 格式錯誤，重新建立
        print("⚠️ JSON 格式錯誤，重新建立成就檔案")
        save_achievements(DEFAULT_ACHIEVEMENTS)
        return DEFAULT_ACHIEVEMENTS


def save_achievements(data):
    with open(ACH_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 🏆 解鎖成就
def unlock(data, key):
    if key in data and not data[key]["unlocked"]:
        data[key]["unlocked"] = True
        save_achievements(data)

        # 成就音效
        try:
            pygame.mixer.Sound("sounds/achievement.mp3").play()
        except Exception as e:
            print(f"⚠️ 無法播放成就音效：{e}")

        # 顯示提示框
        popup_message = f"achievements unlock:{data[key]['name']}"
        show_achievement_popup(popup_message)

        print(f"achievements unlock:{data[key]['name']}")


# 💬 成就提示
popup_timer = 0  # 顯示倒數
popup_text = ""  # 顯示內容文字


def show_achievement_popup(text):
    """在解鎖成就時呼叫"""
    global popup_text, popup_timer
    popup_text = text
    popup_timer = 180  # 顯示 3 秒（假設遊戲是 60 FPS）


def draw_popup(p_x, p_y, t_color):
    """在主遊戲循環中每幀呼叫"""
    global popup_timer, popup_text
    if popup_timer > 0:
        popup_timer -= 1
        # 顯示成就提示框（靠 objects.py_button）
        tool.show_text(popup_text, t_color, p_x, p_y, center=True)


def reset_achievements(data, json_path="achievements.json"):
    # 將所有成就的 unlocked 狀態改為 False
    for key in data:
        if isinstance(data[key], dict) and "unlocked" in data[key]:
            data[key]["unlocked"] = False

    # 存回 achievements.json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("✅ 所有成就已重置！")
    return data
