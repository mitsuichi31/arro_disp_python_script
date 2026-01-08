import pygame
import os
from PIL import Image
import subprocess # 外部プログラムを起動するために必要

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
image_files = ["./images/1.png", "./images/start.png", "./images/2.png", "./images/3.png", "./images/4.png",
               "./images/5.png", "./images/6.png",     "./images/7.png", "./images/8.png",
               "./images/9.png", "./images/10.png",    "./images/stop.png"]  # 例
special_files = ["./all/1.png", "./all/2.png", "./all/3.png", "./all/4.png", "./all/5.png",
               "./all/6.png", "./all/7.png"]  # 例
auto_files = ["./FCT/welcome.png", 
              "./images/1.png", "./images/2.png",  "./images/3.png", "./images/4.png",
              "./images/5.png", "./images/6.png",  "./images/7.png", "./images/8.png",
              "./images/9.png", "./images/10.png"]  # 例

video_file_path = "./FCT/video.mp4" # ★★★ ここを動画のパスに修正 ★★★

# --- 自動切り替えモード用の定数と変数 ---
IMAGE_SWITCH_EVENT = pygame.USEREVENT + 1 # カスタムイベントIDを定義
SWITCH_INTERVAL_MS = 5000                 # 切り替え間隔（ミリ秒）。ここでは5秒に設定。
auto_mode_active = True                   # 状態管理フラグ。起動時自動モードに設定

pygame.init()

# ディスプレイの数を取得
num_displays = pygame.display.get_num_displays()
desktop_sizes = pygame.display.get_desktop_sizes()

if num_displays < 2:
    print("2つのディスプレイが必要です。")
    pygame.quit()
    exit()

# ディスプレイ設定
width = 2160
height = 3840

screen0 = pygame.display.set_mode((width*3, height))
screen1 = screen0.subsurface(pygame.Rect(width, 0, width, height))
screen2 = screen0.subsurface(pygame.Rect(width*2, 0, width, height))

screen_width, screen_height = screen1.get_size()

# --- メインループ変数の初期化 ---
current_image_index = 0
current_auto_index = 0
special_image_file = ""
current_special_index = 0
welcome_flag = 0

# --- **動画再生関連の新しい変数** ---
is_video_playing = False
video_process = None
# -----------------------------------

# 起動時タイマー開始ロジック
if auto_mode_active:
    print("スクリプト起動時、自動切り替えモードで開始しました。")
    pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)

running = True
while running:
    # --- 動画プロセスが終了したかのチェック ---
    if is_video_playing and video_process:
        # poll()はプロセスが終了していれば終了コードを返し、そうでなければNoneを返す
        if video_process.poll() is not None: 
            is_video_playing = False
            video_process = None
            print("動画再生が終了しました。キー入力が再開されます。")
    # ---------------------------------------------
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- 自動切り替えイベントの処理 ---
        # 動画再生中は自動切り替えも停止
        if event.type == IMAGE_SWITCH_EVENT and auto_mode_active and not is_video_playing:
            current_auto_index = (current_auto_index + 1) % len(auto_files)
            special_image_file = "" 
        # -----------------------------------

        # --- **動画再生中はキー入力を無視する** ---
        if is_video_playing:
            continue 
        # ------------------------------------------

        if event.type == pygame.KEYDOWN:
            # Tキー以外は特殊表示をリセット
            if event.key != pygame.K_t:
                special_image_file = ""

            # --- 自動切り替えモードのトグル (Tキー) ---
            if event.key == pygame.K_t:
                auto_mode_active = not auto_mode_active
                if auto_mode_active:
                    print("自動切り替えモードをONにしました。auto_filesが表示されます。")
                    pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)
                    current_auto_index = 0
                    special_image_file = ""
                else:
                    print("自動切り替えモードをOFFにしました。image_filesが表示されます。")
                    pygame.time.set_timer(IMAGE_SWITCH_EVENT, 0)
                continue

            # 自動モードがOFFの時のみ、手動切り替え、動画、特殊キーの処理を行う
            if not auto_mode_active:
                if event.key == pygame.K_SPACE:
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_RIGHT:
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_LEFT:
                    current_image_index = (current_image_index - 1) % len(image_files)
                
                # --- 動画再生キー (Vキー) の処理 ---
                elif event.key == pygame.K_v:
                    vlc_path = r'C:\Program Files\VideoLAN\VLC\vlc.exe'
                    try:
                        # 動画再生を開始し、プロセスを保持
                        # "C:\Program Files\VideoLAN\VLC\vlc.exe" --video-splitter=wall --wall-cols=2 --wall-rows=1 --no-embedded-video --fullscreen --qt-fullscreen-screennumber=0
                        video_process = subprocess.Popen([vlc_path, video_file_path, '--fullscreen', '--play-and-exit'])
                        is_video_playing = True
                        print(f"動画ファイル {video_file_path} をVLCで再生開始しました。Pygameのキー入力を無効にしました。")
                    except FileNotFoundError:
                        print("エラー: VLC media playerが見つかりません。パスを確認してください。")
                    except Exception as e:
                        print(f"動画再生中にエラーが発生しました: {e}")
                # ------------------------------------------
                
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_s:
                    special_image_file = "./zhaodi/start-3.png"
                elif event.key == pygame.K_e:
                    special_image_file = "./zhaodi/stop-3.png"
                elif event.key == pygame.K_l:
                    special_image_file = "./zhaodi/left-3.png"
                elif event.key == pygame.K_r:
                    special_image_file = "./zhaodi/right-3.png"
                elif event.key == pygame.K_a:
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


    # --- 画像の選択と読み込み (動画再生中は背景の更新は継続する) ---
    if special_image_file != "":
        image = pygame.image.load(special_image_file)
    elif auto_mode_active:
        current_auto_index = current_auto_index % len(auto_files)
        image = pygame.image.load(auto_files[current_auto_index])
    else:
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