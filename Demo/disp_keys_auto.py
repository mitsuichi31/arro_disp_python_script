import pygame
import os
from PIL import Image

def get_image_files(directory):
    """指定されたディレクトリからGIFファイルを探してリストを返します。"""
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".gif"):
            image_files.append(os.path.join(directory, filename))
    return image_files

# PillowによるGIFの読み込みとフレームの取得 (使用されていないが残しておく)
def load_gif_frames(filename):
    """GIFファイルを読み込み、PygameのSurfaceのフレームリストを返します。"""
    frames = []
    gif = Image.open(filename)
    try:
        while True:
            # PillowのイメージをPygameのSurfaceに変換
            frame = gif.convert('RGBA')
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# --- 画像ファイルの定義 ---
# image_files: 手動/特殊キーでの操作時に使用されるメインの画像群
image_files = ["./images/1.png", "./images/start.png", "./images/2.png", "./images/3.png", "./images/4.png",
               "./images/5.png", "./images/6.png",     "./images/7.png", "./images/8.png",
               "./images/9.png", "./images/10.png",    "./images/stop.png"]  # 例

# special_files: Aキーなどの特殊キー操作で表示される画像群 (自動切り替えには使用しない)
special_files = ["./all/1.png", "./all/2.png", "./all/3.png", "./all/4.png", "./all/5.png",
               "./all/6.png", "./all/7.png"]  # 例

# auto_files: **新しく定義された、自動切り替えモードでのみ使用される画像群**
auto_files = ["./images/1.png", "./images/2.png", "./images/3.png", "./images/4.png",
              "./images/5.png", "./images/6.png", "./images/7.png", "./images/8.png",
              "./images/9.png", "./images/10.png"]  # 例

# --- 自動切り替えモード用の定数と変数 ---
IMAGE_SWITCH_EVENT = pygame.USEREVENT + 1 # カスタムイベントIDを定義
SWITCH_INTERVAL_MS = 3000                 # 切り替え間隔（ミリ秒）。ここでは3秒に設定。
auto_mode_active = False                  # 状態管理フラグ。初期値は手動モード

pygame.init()

# ディスプレイの数を取得
num_displays = pygame.display.get_num_displays()
desktop_sizes = pygame.display.get_desktop_sizes()

# 2つのディスプレイが存在するか確認
if num_displays < 2:
    print("2つのディスプレイが必要です。")
    pygame.quit()
    exit()

# 2つのディスプレイをフルスクリーンで初期化（サブサーフェスを使用）
width = 2160
height = 3840

screen0 = pygame.display.set_mode((width*3, height)) # 3画面分の横幅を持つメイン画面
screen1 = screen0.subsurface(pygame.Rect(width, 0, width, height))
screen2 = screen0.subsurface(pygame.Rect(width*2, 0, width, height))

screen_width, screen_height = screen1.get_size()

# --- メインループ変数の初期化 ---
current_image_index = 0   # image_files用のインデックス
current_auto_index = 0    # auto_files用のインデックス
special_image_file = ""
current_special_index = 0
welcome_flag = 0

# --- **修正点: 起動時タイマー開始ロジックの追加** ---
if auto_mode_active:
    print("スクリプト起動時、自動切り替えモードで開始しました。")
    pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)
# ----------------------------------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- 自動切り替えイベントの処理 ---
        if event.type == IMAGE_SWITCH_EVENT and auto_mode_active:
            # 自動モードがアクティブな場合、auto_filesのインデックスを切り替え
            current_auto_index = (current_auto_index + 1) % len(auto_files)
            # 自動モード中は特殊画像ファイルをクリア
            special_image_file = "" 
        # -----------------------------------

        if event.type == pygame.KEYDOWN:
            # キーを押した際、特殊表示をリセット
            if event.key != pygame.K_t:
                special_image_file = ""

            # --- 自動切り替えモードのトグル (Tキー) ---
            if event.key == pygame.K_t: # 't'キーで自動切り替えモードをトグル
                auto_mode_active = not auto_mode_active
                if auto_mode_active:
                    # モードON: タイマーを開始し、自動インデックスをリセット
                    print("自動切り替えモードをONにしました。auto_filesが表示されます。")
                    pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)
                    current_auto_index = 0 # 開始時に最初の画像を表示
                    special_image_file = "" # 自動モード中は特殊画像を強制的にオフ
                else:
                    # モードOFF: タイマーを停止し、手動インデックスを維持
                    print("自動切り替えモードをOFFにしました。image_filesが表示されます。")
                    pygame.time.set_timer(IMAGE_SWITCH_EVENT, 0) # タイマーを停止
                continue # 他のキー入力処理はスキップ
            # ------------------------------------------

            # 自動モードがOFFの時のみ、手動切り替えと特殊キーの処理を行う
            if not auto_mode_active:
                if event.key == pygame.K_SPACE:  # スペースキーで画像を切り替え
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_RIGHT:  # ->で画像を切り替え
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_LEFT:  # <-で画像を切り替え
                    current_image_index = (current_image_index - 1) % len(image_files)
                elif event.key == pygame.K_ESCAPE: # ESCキーで終了
                    running = False
                # --- 特殊キーの処理 ---
                elif event.key == pygame.K_s:
                    special_image_file = "./zhaodi/start-3.png"
                elif event.key == pygame.K_e:
                    special_image_file = "./zhaodi/stop-3.png"
                elif event.key == pygame.K_l:
                    special_image_file = "./zhaodi/left-3.png"
                elif event.key == pygame.K_r:
                    special_image_file = "./zhaodi/right-3.png"
                elif event.key == pygame.K_a:
                    # special_files は Aキーなどの特殊キー操作で使用されます。
                    special_image_file = special_files[current_special_index]
                    current_special_index = (current_special_index + 1) % len(special_files)
                elif event.key == pygame.K_w:
                    if welcome_flag != 0:
                        special_image_file = ""
                        welcome_flag = 0
                    else:
                        special_image_file = "./welcome/welcome.png"
                        welcome_flag = 1
            # -----------------------------------


    # --- 画像の選択と読み込み ---
    if special_image_file != "":
        # 1. 特殊キーが押されている場合（最優先）
        image = pygame.image.load(special_image_file)
    elif auto_mode_active:
        # 2. 自動モードがONの場合 (auto_filesを表示)
        # 画像インデックスが有効範囲内であることを保証
        current_auto_index = current_auto_index % len(auto_files)
        image = pygame.image.load(auto_files[current_auto_index])
    else:
        # 3. 手動モードがONの場合 (image_filesを表示)
        # 画像インデックスが有効範囲内であることを保証
        current_image_index = current_image_index % len(image_files)
        image = pygame.image.load(image_files[current_image_index])

    # 画像を画面サイズにリサイズ
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # 画像をそれぞれのディスプレイに描画
    image_to_draw = image
    screen1.blit(image_to_draw, (0, 0))
    screen2.blit(image_to_draw, (0, 0))

    # 画面を更新
    pygame.display.flip()

pygame.quit()