"""
重做跑酷大師：
 把關卡變成json檔  OK
 畫面可調整  OK
 解決tool的text_button文字至中問題  OK
 修正載入問題  OK
 岩漿碰撞  OK
 修正碰到方塊抖動問題  OK
 修正物件偏移問題
 刪掉一些不必要的變數
 把一些為載入的方塊都載入
記得把這個檔案傳到GitHub
錄一個影片(預告片)給煜煬看
"""

import json
import sys
from pathlib import Path

import pygame

import config
import tool

# 初始化
pygame.init()
running = True
game_state = "menu"
WIDTH, HEIGHT = 700, 600
new_width, new_height = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(config.TITLE)
clock = pygame.time.Clock()
old_w, old_h = tool.W, tool.H

inr_debug = False
level_config = {"gravity": 1.0, "screen_color": [255, 255, 255], "floor_color": [200, 50, 0], "hint_color": [0, 0, 0]}

key_die = False


def load_level(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
        print(f"成功載入檔案！{filename}")
    except FileNotFoundError as e:
        print(f"找不到檔案：{e}")

    obstacles = []
    decorations = []
    invisible_rect = []
    lava_rect = []
    flow_lava = []
    for obs in data["obstacles"]:
        # 將 JSON 的 list 轉回 pygame.Rect
        rect = pygame.Rect(obs["rect"])
        # 這裡重建你的物件邏輯
        obstacles.append({"rect": rect, "color": tuple(obs["color"]), "collide": obs["collide"], "show": obs["show"]})
    for dc in data.get("decorations", []):
        rect = pygame.Rect(dc["rect"])
        decorations.append({"rect": rect, "color": tuple(dc["color"]), "collide": dc["collide"], "show": obs["show"]})
    for inr in data.get("invisible_rects", []):
        rect = pygame.Rect(inr["rect"])
        invisible_rect.append({"rect": rect, "color": tuple(inr["color"]), "collide": inr["collide"], "show": inr["show"]})
    for lv in data["lava"]:
        rect = pygame.Rect(lv["rect"])
        lava_rect.append({"rect": rect, "color": tuple(lv["color"]), "collide": lv["collide"], "show": lv["show"]})
    for flv in data["flow_lava"]:
        rect = pygame.Rect(flv["rect"])
        flow_lava.append(
            {
                "rect": rect,
                "color": tuple(flv["color"]),
                "collide": flv["collide"],
                "show": flv["show"],
                "speed": flv["speed"],
                "range": flv["y_range"],
            }
        )
    return obstacles, decorations, invisible_rect, lava_rect, data["config"]


root = Path(__file__).parent.resolve()
LEVELS_PATH = root / "levels"
LV1_PATH = str(LEVELS_PATH / "lv1.json")
LV2_PATH = str(LEVELS_PATH / "lv2.json")
LV3_PATH = str(LEVELS_PATH / "lv3.json")
LV4_PATH = str(LEVELS_PATH / "lv4.json")

jump_timer = 0
max_jump_hold = 12  # 允許持續按住增加高度的幀數 (約 0.25 秒)

# 按鍵偵測
is_pressing = [False] * 10


def reset_pressing():
    is_pressing[:] = [False] * len(is_pressing)


# 紀錄舊的螢幕尺寸，用來計算比例
old_h = tool.H

# 其他變數
levels = "Lv1"
OFFSET_Y = 140


def screen_resets(is_init=False):
    global \
        ground_y, \
        gravity, \
        jump_power, \
        jump_timer, \
        max_jump_hold, \
        player_size, \
        player_y, \
        player_x, \
        old_w, \
        old_h, \
        move_speed, \
        fast_move_speed, \
        scroll_x, \
        scroll_y, \
        x_scale, \
        y_scale, \
        level_config

    # 1. 優先計算縮放比例 (這是一切的基礎)
    y_scale = tool.H / 600
    # x_scale = tool.W / 700 # 若以後需要橫向縮放可開啟

    # 2. 更新基礎物理量 (使用新的 y_scale)
    ground_y = 480 * y_scale  # 固定比例基準點
    player_size = int(tool.H * 0.05)
    gravity = tool.H * 0.0019 * level_config.get("gravity", 1.0)
    jump_power = tool.H * -0.025
    move_speed = 5 * y_scale
    fast_move_speed = 7 * y_scale
    max_jump_hold = 12

    # 3. 根據情況調整玩家位置
    if is_init:
        # 遊戲開始或死亡：重置位置與攝影機
        player_x = tool.W * 0.1
        player_y = ground_y - player_size
        scroll_x, scroll_y = 0, 0
    else:
        # 僅視窗縮放：僅清空跳躍計時，不強制移動玩家，但要更新紀錄
        jump_timer = 0

    # 4. 更新歷史紀錄
    old_w = tool.W
    old_h = tool.H


def reset_game():
    global ground_y, vel_y, player_x, player_y, player_size, is_jumping, is_moving, has_jumped

    # 初始化物理狀態
    vel_y = 0
    is_jumping = False
    is_moving = False
    has_jumped = False

    # 執行畫面與位置設定 (會呼叫 screen_resets 並設定 player_y)
    screen_resets(is_init=True)


def die_resets():
    global player_x, player_y, key_die, vel_y, on_ground, is_jumping, has_jumped

    # 死亡重置：回到起點並恢復物理狀態
    key_die = False
    vel_y = 0
    on_ground = True
    is_jumping = False
    has_jumped = False

    # 使用畫面設定來精準定位
    screen_resets(is_init=True)


while running:
    screen.fill(tool.Colors.WHITE)
    # 重要變數
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos(False)

    # 基礎事件
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        # --- 核心邏輯：當視窗大小改變時 ---
        if event.type == pygame.VIDEORESIZE:
            # 更新目前的視窗寬高變數
            new_width, new_height = event.w, event.h
            # 重新呼叫 set_mode 來更新畫布大小
            screen = pygame.display.set_mode(
                (tool.num_range(400, 1300, new_width), tool.num_range(300, 800, new_height)), pygame.RESIZABLE
            )
            tool.set_screen(screen)
            screen_resets(is_init=False)

    if game_state == "menu":
        screen.fill(tool.Colors.BLUE2)
        tool.show_text("Parkour Master!", tool.Colors.WHITE, 0.5, 0.15, size=40)
        lv_btn = tool.text_button("Levels", tool.Colors.BLACK, tool.Colors.WHITE, 0, 0.28)
        settings_btn = tool.text_button("Settings", tool.Colors.BLACK, tool.Colors.WHITE, 0, 0.45)
        about_this_game_btn = tool.text_button("About This Game", tool.Colors.BLACK, tool.Colors.DARK_GRAY, 0, 0.62, 0.4)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if lv_btn.collidepoint(mouse_pos):
                    is_pressing[0] = True
                if settings_btn.collidepoint(mouse_pos):
                    is_pressing[1] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if lv_btn.collidepoint(mouse_pos) and is_pressing[0]:
                    game_state = "levels_select"
                if settings_btn.collidepoint(mouse_pos) and is_pressing[1]:
                    game_state = "setting_p1"
                reset_pressing()

    elif game_state == "levels_select":
        screen.fill(tool.Colors.ORANGE)
        tool.show_text("Level Select", tool.Colors.WHITE, 0.5, 0.1, size=40)
        lv1_btn = tool.text_button("Lv.1", tool.Colors.BLACK, tool.Colors.RED, 0.1, 0.25, 0.15, b_center=False)
        lv2_btn = tool.text_button("Lv.2", tool.Colors.BLACK, tool.Colors.ORANGE2, 0.32, 0.25, 0.15, b_center=False)
        lv3_btn = tool.text_button("Lv.3", tool.Colors.BLACK, tool.Colors.YELLOW, 0.54, 0.25, 0.15, b_center=False)
        lv4_btn = tool.text_button("Lv.4", tool.Colors.BLACK, tool.Colors.GREEN, 0.76, 0.25, 0.15, b_center=False)
        back_btn = tool.text_button("Back To Menu", tool.Colors.BLACK, tool.Colors.GREEN, 0, 0.8, 0.3)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if lv1_btn.collidepoint(mouse_pos):
                    is_pressing[0] = True
                if lv2_btn.collidepoint(mouse_pos):
                    is_pressing[1] = True
                if lv3_btn.collidepoint(mouse_pos):
                    is_pressing[2] = True
                if lv4_btn.collidepoint(mouse_pos):
                    is_pressing[3] = True
                if back_btn.collidepoint(mouse_pos):
                    is_pressing[4] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if lv1_btn.collidepoint(mouse_pos) and is_pressing[0]:
                    # 載入第一關資料
                    all_obstacles, all_decorations, all_invisible_rects, lava_rects, level_config = load_level(LV1_PATH)
                    LEVEL_WIDTH, LEVEL_HEIGHT = level_config["width"], level_config["height"]
                    levels = "Lv1"
                    game_state = "start_game"
                    reset_game()
                if lv2_btn.collidepoint(mouse_pos) and is_pressing[1]:
                    # 載入第二關資料
                    all_obstacles, all_decorations, all_invisible_rects, lava_rects, level_config = load_level(LV2_PATH)
                    LEVEL_WIDTH, LEVEL_HEIGHT = level_config["width"], level_config["height"]
                    levels = "Lv1"
                    levels = "Lv2"
                    game_state = "start_game"
                    reset_game()
                if lv3_btn.collidepoint(mouse_pos) and is_pressing[2]:
                    # 載入第三關資料
                    all_obstacles, all_decorations, all_invisible_rects, lava_rects, level_config = load_level(LV3_PATH)
                    LEVEL_WIDTH, LEVEL_HEIGHT = level_config["width"], level_config["height"]
                    levels = "Lv1"
                    levels = "Lv3"
                    game_state = "start_game"
                    reset_game()
                if lv4_btn.collidepoint(mouse_pos) and is_pressing[3]:
                    # 載入第四關資料
                    all_obstacles, all_decorations, all_invisible_rects, lava_rects, level_config = load_level(LV4_PATH)
                    LEVEL_WIDTH, LEVEL_HEIGHT = level_config["width"], level_config["height"]
                    levels = "Lv1"
                    levels = "Lv4"
                    game_state = "start_game"
                    reset_game()
                if back_btn.collidepoint(mouse_pos) and is_pressing[4]:
                    game_state = "menu"
                reset_pressing()

    elif game_state == "setting_p1":
        screen.fill(tool.Colors.GRAY)
        tool.show_text("Settings", tool.Colors.WHITE, 0.5, 0.1, size=40)
        back_btn = tool.text_button("Back To Menu", tool.Colors.BLACK, tool.Colors.GREEN, 0, 0.8, 0.3)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(mouse_pos):
                    is_pressing[2] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if back_btn.collidepoint(mouse_pos) and is_pressing[2]:
                    game_state = "menu"
                reset_pressing()

    elif game_state == "start_game":
        screen.fill(tuple(level_config["screen_color"]))  # 背景
        screen_resets()
        is_moving = False
        """x偵測"""
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            if keys[pygame.K_SPACE]:
                dx = fast_move_speed
            else:
                dx = move_speed
            is_moving = True
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            if keys[pygame.K_SPACE]:
                dx = -fast_move_speed
            else:
                dx = -move_speed
            is_moving = True
        else:
            dx = 0
            is_moving = False

        """y偵測"""

        # 偵測剛跳躍的瞬間 (不變)
        if keys[pygame.K_w] and not has_jumped:
            vel_y = jump_power  # 給予基礎初速
            is_jumping = True
            has_jumped = True
            jump_timer = max_jump_hold

        # 修改：按住 W 時的邏輯
        if is_jumping and keys[pygame.K_w] and jump_timer > 0:
            # 不要直接減去大於重力的值，而是讓重力「變小」
            # 這樣 vel_y 依然會增加(變重)，只是增加得比較慢，才會有減速上升的感覺
            vel_y -= gravity * 0.8
            jump_timer -= 1

        # 核心優化：放開按鍵時的「截斷」
        # 如果玩家在上升途中(vel_y < 0)就放開 W，立刻削減向上動量
        if not keys[pygame.K_w] and vel_y < 0:
            vel_y *= 0.6  # 數值愈小，跳躍高度被切斷得愈明顯
            jump_timer = 0  # 同時清空計時器

        current_player_size = int(player_size * y_scale)

        colliding_rect = -1

        """地圖捲動"""
        target_scroll_x = min(max(player_x - WIDTH // 2, 0), LEVEL_WIDTH - WIDTH)

        scroll_x += (target_scroll_x - scroll_x) * 0.07
        # 1. 計算目標位置
        target_scroll_y = player_y - HEIGHT // 2

        # 2. 平滑移動 (線性插值 LERP 概念)
        # 數值 0.1 代表每幀攝影機只移動到目標距離的 10%
        # 這個數值越小越平滑，越大越靈敏
        scroll_y += (target_scroll_y - scroll_y) * 0.07

        """x碰撞"""
        player_x += dx
        # 虛擬玩家：用玩家的世界座標
        player_rect = pygame.Rect(int(player_x), int(player_y), current_player_size, current_player_size)

        for index, obs in enumerate(all_obstacles + all_invisible_rects):
            # 取得該物件縮放後的世界座標矩形
            orig = obs["rect"]
            w_rect = pygame.Rect(orig.x * y_scale, (orig.y + OFFSET_Y) * y_scale, orig.width * y_scale, orig.height * y_scale)

            if player_rect.colliderect(w_rect):
                # 如果正在往右走撞到牆
                if dx > 0:
                    player_x = w_rect.left - current_player_size
                # 如果正在往左走撞到牆
                elif dx < 0:
                    player_x = w_rect.right
                # 同步更新虛擬矩形，避免 Y 軸判定出錯
                player_rect.x = player_x
                colliding_rect = index

        """裝飾方塊繪製"""
        for dc in all_decorations:
            orig = dc["rect"]
            dc_rect = pygame.Rect(
                (orig.x * y_scale) - scroll_x,
                (orig.y + OFFSET_Y) * y_scale - scroll_y,
                orig.width * y_scale,
                orig.height * y_scale,
            )
            pygame.draw.rect(screen, dc["color"], dc_rect)
        """y碰撞"""

        # 1. 每一幀都先套用重力與位移
        vel_y += gravity
        player_y += vel_y
        player_rect.y = player_y  # 更新虛擬矩形位置

        on_ground = False  # 先預設不在地上

        # 2. 無條件檢查所有方塊 (不要放在 if not is_jumping 裡面)
        for index, obs in enumerate(all_invisible_rects + all_obstacles):
            orig = obs["rect"]
            w_rect = pygame.Rect(orig.x * y_scale, (orig.y + OFFSET_Y) * y_scale, orig.width * y_scale, orig.height * y_scale)

            if player_rect.colliderect(w_rect):
                if vel_y > 0:  # 正在往下掉，踩到地板了
                    player_y = w_rect.top - current_player_size
                    vel_y = 0
                    is_jumping = False
                    on_ground = True
                elif vel_y < 0:  # 正在往上跳，撞到頭了
                    player_y = w_rect.bottom
                    vel_y = 0

                player_rect.y = player_y  # 修正後立刻同步矩形
                colliding_rect = index

        # 3. 檢查最底下的地板
        if player_y + current_player_size >= ground_y - 2:
            player_y = ground_y - current_player_size
            vel_y = 0
            is_jumping = False
            on_ground = True
            colliding_rect = "ground"

        # 4. 最後檢查：如果完全沒踩到東西，才算是在跳躍中
        if on_ground:
            is_jumping = False
            has_jumped = False  # 踩到地了，重設跳躍權限
            vel_y = 0
        else:
            # 這裡就是關鍵：如果只是走出邊緣掉下去，is_jumping 變成 True
            # 但 has_jumped 依然是 False，所以你還能跳一次
            is_jumping = True

        """一般方塊繪製"""
        for obs in all_invisible_rects + all_obstacles:
            orig = obs["rect"]
            draw_rect = pygame.Rect(
                orig.x * y_scale - scroll_x, (orig.y + OFFSET_Y) * y_scale - scroll_y, orig.width * y_scale, orig.height * y_scale
            )
            # 轉換為螢幕座標
            if obs.get("show", True):
                # 正常方塊
                pygame.draw.rect(screen, obs["color"], draw_rect)
            elif inr_debug:  # 除錯模式
                pygame.draw.rect(screen, tool.Colors.PURPLE, draw_rect, 1)

        """岩漿方塊繪製"""
        die_lava_num = -1
        for index, lv in enumerate(lava_rects):
            orig = lv["rect"]
            w_x = orig.x * y_scale
            w_y = (orig.y + OFFSET_Y) * y_scale  # 加上那個 140 偏移
            w_w = orig.width * y_scale  # 測試為y
            w_h = orig.height * y_scale

            # 轉換為螢幕座標
            draw_rect = pygame.draw.rect(screen, lv["color"], (w_x - scroll_x, w_y - scroll_y, w_w, w_h))
            w_rect = pygame.Rect(w_x, w_y, w_w, w_h)

            # 死亡判定
            if player_rect.colliderect(w_rect):
                die_lava_num = index
                game_state = "game_over!"
        """其他死法"""

        # 掉下虛空
        if player_y > ground_y + 500:
            game_state = "game_over!"
            die_text = "Fell into the void"

        """"""

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    game_state = "pause"
                if event.key == pygame.K_r:
                    key_die = True
                    game_state = "game_over!"

        # ---  繪製玩家與地面 ---
        # 畫地面
        for i in range(0, LEVEL_WIDTH, int(100 * y_scale)):
            pygame.draw.rect(
                screen, level_config["floor_color"], (i - scroll_x, ground_y - scroll_y, 80 * y_scale, 20 * y_scale)
            )  # 畫玩家
        # 因為 player_x 是世界座標，所以要減去 scroll_x 轉為螢幕座標
        pygame.draw.rect(
            screen, tool.Colors.BLUE, (player_x - scroll_x, player_y - scroll_y, current_player_size, current_player_size)
        )
        tool.show_text(
            "colliding_rect: None" if colliding_rect == -1 else f"colliding_rect: {colliding_rect}",
            level_config["hint_color"],
            0.2,
            0.9,
            size=20,
        )
        tool.show_text(  # round(player_x, 2):g    round(ground_y - player_y, 2):g
            f"x: {int(player_x)}, y: {int(ground_y - player_y)}",
            level_config["hint_color"],
            0.7,
            0.1,
            size=17,
            screen_center=False,
        )
    elif game_state == "pause":
        """繪製上一個畫面"""
        screen.fill(level_config["screen_color"])
        for i in range(0, LEVEL_WIDTH, int(100 * y_scale)):
            pygame.draw.rect(
                screen, level_config["floor_color"], (i - scroll_x, ground_y - scroll_y, 80 * y_scale, 20 * y_scale)
            )  # 畫玩家
        pygame.draw.rect(screen, tool.Colors.BLUE, (player_x - scroll_x, player_y - scroll_y, player_size, player_size))
        tool.show_text(
            "colliding_rect: None" if colliding_rect == -1 else f"colliding_rect: {colliding_rect}",
            level_config["hint_color"],
            0.2,
            0.9,
            size=20,
        )
        tool.show_text(
            f"x: {round(player_x, 2):g}, y: {round(ground_y - player_y, 2):g}",
            level_config["hint_color"],
            0.7,
            0.1,
            size=17,
            screen_center=False,
        )
        """一般方塊繪製"""
        for obs in all_invisible_rects + all_obstacles:
            orig = obs["rect"]
            draw_rect = pygame.Rect(
                orig.x * y_scale - scroll_x, (orig.y + OFFSET_Y) * y_scale - scroll_y, orig.width * y_scale, orig.height * y_scale
            )
            # 轉換為螢幕座標
            if obs.get("show", True):
                # 正常方塊
                pygame.draw.rect(screen, obs["color"], draw_rect)
            elif inr_debug:  # 除錯模式
                pygame.draw.rect(screen, tool.Colors.PURPLE, draw_rect, 1)

        """岩漿方塊繪製"""
        die_lava_num = -1
        for lv in lava_rects:
            orig = lv["rect"]
            w_x = orig.x * y_scale
            w_y = (orig.y + OFFSET_Y) * y_scale  # 加上那個 140 偏移
            w_w = orig.width * y_scale  # 測試為y
            w_h = orig.height * y_scale

            # 轉換為螢幕座標
            draw_rect = pygame.draw.rect(screen, lv["color"], (w_x - scroll_x, w_y - scroll_y, w_w, w_h))
        tool.screen_vague(12)
        """到這"""

        tool.show_text("Pause", level_config["hint_color"], 0.5, 0.08, size=40)
        resume_btn = tool.text_button("Resume", tool.Colors.BLACK, tool.Colors.GREEN, 0, 0.21, 0.43)
        menu_btn = tool.text_button("Back to Menu", tool.Colors.BLACK, tool.Colors.YELLOW, 0, 0.38, 0.43)
        lv_btn = tool.text_button("Back to Levels Select", tool.Colors.BLACK, tool.Colors.CYAN, 0, 0.55, 0.43)
        restart_btn = tool.text_button("Restart", tool.Colors.BLACK, tool.Colors.PURPLE, 0, 0.72, 0.43)
        close_btn = tool.text_button("Close This Game", tool.Colors.BLACK, tool.Colors.RED, 0, 0.88, 0.43)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    game_state = "start_game"
                if event.key == pygame.K_c:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_btn.collidepoint(mouse_pos):
                    is_pressing[0] = True
                if menu_btn.collidepoint(mouse_pos):
                    is_pressing[1] = True
                if lv_btn.collidepoint(mouse_pos):
                    is_pressing[2] = True
                if restart_btn.collidepoint(mouse_pos):
                    is_pressing[3] = True
                if close_btn.collidepoint(mouse_pos):
                    is_pressing[4] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if resume_btn.collidepoint(mouse_pos) and is_pressing[0]:
                    game_state = "start_game"
                if menu_btn.collidepoint(mouse_pos) and is_pressing[1]:
                    reset_game()
                    game_state = "menu"
                if lv_btn.collidepoint(mouse_pos) and is_pressing[2]:
                    reset_game()
                    game_state = "levels_select"
                if restart_btn.collidepoint(mouse_pos) and is_pressing[3]:
                    reset_game()
                    game_state = "start_game"
                if close_btn.collidepoint(mouse_pos) and is_pressing[4]:
                    running = False
                reset_pressing()

    elif game_state == "game_over!":
        """繪製上一個畫面"""
        screen.fill(level_config["screen_color"])
        for i in range(0, LEVEL_WIDTH, int(100 * y_scale)):
            pygame.draw.rect(
                screen, level_config["floor_color"], (i - scroll_x, ground_y - scroll_y, 80 * y_scale, 20 * y_scale)
            )  # 畫玩家
        pygame.draw.rect(screen, tool.Colors.BLUE, (player_x - scroll_x, player_y - scroll_y, player_size, player_size))
        tool.show_text(
            "colliding_rect: None" if colliding_rect == -1 else f"colliding_rect: {colliding_rect}",
            level_config["hint_color"],
            0.2,
            0.9,
            size=20,
        )
        tool.show_text(f"x: {int(player_x)}, y: {int(player_y)}", level_config["hint_color"], 0.85, 0.1, size=20)
        for obs in all_invisible_rects + all_obstacles:
            orig = obs["rect"]
            w_x = orig.x * y_scale
            w_y = (orig.y + OFFSET_Y) * y_scale  # 加上那個 140 偏移
            w_w = orig.width * y_scale  # 測試為y
            w_h = orig.height * y_scale

            # 轉換為螢幕座標
            draw_rect = pygame.Rect(w_x - scroll_x, w_y - scroll_y, w_w, w_h)
            w_rect = pygame.Rect(w_x, w_y, w_w, w_h)

            if obs.get("show"):
                # 正常方塊
                pygame.draw.rect(screen, obs["color"], draw_rect)
        for dc in all_decorations + lava_rects:
            orig = dc["rect"]
            dc_rect = pygame.Rect(
                (orig.x * y_scale) - scroll_x,
                (orig.y + OFFSET_Y) * y_scale - scroll_y,
                orig.width * y_scale,
                orig.height * y_scale,
            )
            pygame.draw.rect(screen, dc["color"], dc_rect)
        tool.screen_vague(12)
        """到這"""

        tool.show_text("You Died!", tool.Colors.RED, 0.5, 0.08, size=40)
        # 死亡類型判定
        if die_lava_num != -1:
            if levels == "Lv3" and die_lava_num == 0:
                if vel_y:
                    die_text = f"Crashed Hard Into the Electric Wire (No.{die_lava_num + 1})"
            elif vel_y:
                if vel_y < 0:
                    die_text = f"Died By Trying To Jump Over Lava No.{die_lava_num + 1}"
                else:
                    die_text = f"Died By Jumping Into Lava No.{die_lava_num + 1}"
            else:
                die_text = f"Died By Touch Lava No.{die_lava_num + 1}"
        elif key_die:
            die_text = "Died By Your Self's Hand"

        tool.show_text(die_text, tool.Colors.WHITE, 0.5, 0.2)
        restart_btn = tool.text_button("Restart", tool.Colors.WHITE, tool.Colors.GREEN, 0, 0.37, 0.43)
        menu_btn = tool.text_button("Back to Menu", tool.Colors.BLACK, tool.Colors.YELLOW, 0, 0.54, 0.43)
        lv_btn = tool.text_button("Back to Levels Select", tool.Colors.BLACK, tool.Colors.CYAN, 0, 0.71, 0.43)
        close_btn = tool.text_button("Close This Game", tool.Colors.BLACK, tool.Colors.RED, 0, 0.88, 0.43)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_btn.collidepoint(mouse_pos):
                    is_pressing[0] = True
                if menu_btn.collidepoint(mouse_pos):
                    is_pressing[1] = True
                if lv_btn.collidepoint(mouse_pos):
                    is_pressing[2] = True
                if close_btn.collidepoint(mouse_pos):
                    is_pressing[3] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if restart_btn.collidepoint(mouse_pos) and is_pressing[0]:
                    die_resets()
                    game_state = "start_game"
                if menu_btn.collidepoint(mouse_pos) and is_pressing[1]:
                    reset_game()
                    game_state = "menu"
                if lv_btn.collidepoint(mouse_pos) and is_pressing[2]:
                    reset_game()
                    game_state = "levels_select"
                if close_btn.collidepoint(mouse_pos) and is_pressing[3]:
                    running = False
                reset_pressing()

    pygame.display.set_caption(config.TITLE + " - " + game_state.replace("_", " ").title())
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print()
sys.exit("NNNNNOOOOOOOOO! You End This Game!!")
print()
