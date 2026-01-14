import argparse
import os
import subprocess  # 外部プログラムを起動するために使用

import pygame
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description="pygame デモの起動オプション")
    parser.add_argument(
        "--test",
        action="store_true",
        help="単一画面で動作（画面サイズは自動取得）",
    )
    parser.add_argument(
        "--mute",
        action="store_true",
        default=True,
        help="動画再生を無音にする（デフォルト: 有効）",
    )
    parser.add_argument(
        "--with-audio",
        action="store_false",
        dest="mute",
        help="動画再生を有音にする",
    )
    return parser.parse_args()


def get_image_files(directory):
    """指定したディレクトリからGIFファイルを探してリストで返す。"""
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".gif"):
            image_files.append(os.path.join(directory, filename))
    return image_files


# PillowによるGIF読み込みとフレーム取得（現状未使用だが残しておく）
def load_gif_frames(filename):
    """GIFを読み込み、PygameのSurfaceフレーム一覧を返す。"""
    frames = []
    gif = Image.open(filename)
    try:
        while True:
            # PillowのイメージをPygameのSurfaceに変換
            frame = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

# --- 画像ファイルの定義 ---
image_files = [
    "./images/1.png",
    "./images/start.png",
    "./images/2.png",
    "./images/3.png",
    "./images/4.png",
    "./images/5.png",
    "./images/6.png",
    "./images/7.png",
    "./images/8.png",
    "./images/9.png",
    "./images/10.png",
    "./images/stop.png",
]  # 画像リスト
special_files = [
    "./all/1.png",
    "./all/2.png",
    "./all/3.png",
    "./all/4.png",
    "./all/5.png",
    "./all/6.png",
    "./all/7.png",
]  # 特殊表示リスト

def get_auto_files(directory):
    """autoフォルダ内の画像/動画ファイルを自動検出して返す。"""
    if not os.path.isdir(directory):
        return []
    auto_list = []
    # ファイル名の昇順（辞書順）で並べる
    for filename in sorted(os.listdir(directory)):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(filename)[1].lower()
        if ext in IMAGE_EXTENSIONS or ext in VIDEO_EXTENSIONS:
            auto_list.append(path)
    return auto_list


auto_files = get_auto_files("./auto")  # 自動切り替えリスト（動画も可）

video_file_path = "./FCT/video.mp4"  # ここを動画のパスに修正

# --- 自動切り替えモード用の定数と変数 ---
IMAGE_SWITCH_EVENT = pygame.USEREVENT + 1  # カスタムイベントを定義
SWITCH_INTERVAL_MS = 5000  # 切り替え間隔（ミリ秒）。ここでは5秒に設定
auto_mode_active = True  # 状態管理フラグ。起動時は自動モード

args = parse_args()

pygame.init()

# ディスプレイ数とサイズを取得
num_displays = pygame.display.get_num_displays()
desktop_sizes = pygame.display.get_desktop_sizes()

if args.test:
    if not desktop_sizes:
        print("画面サイズを取得できません。")
        pygame.quit()
        raise SystemExit(1)
    width, height = desktop_sizes[0]
    screen0 = pygame.display.set_mode((width, height))
    screen1 = screen0
    screen2 = None
else:
    if num_displays < 2:
        print("2つのディスプレイが必要です。--test で単一画面モードを有効にできます。")
        pygame.quit()
        raise SystemExit(1)

    # ディスプレイ設定（既存と同じ想定）
    width = 2160
    height = 3840
    screen0 = pygame.display.set_mode((width * 3, height))
    screen1 = screen0.subsurface(pygame.Rect(width, 0, width, height))
    screen2 = screen0.subsurface(pygame.Rect(width * 2, 0, width, height))

screen_width, screen_height = screen1.get_size()

# --- メインループ用の初期値 ---
current_image_index = 0
current_auto_index = 0
current_auto_path = ""
current_image_path = ""
special_image_file = ""
current_special_index = 0
welcome_flag = 0

# --- 動画再生関連の変数 ---
is_video_playing = False
video_process = None
# -----------------------------------


def is_video_file(path):
    return os.path.splitext(path)[1].lower() in VIDEO_EXTENSIONS


def is_image_file(path):
    return os.path.splitext(path)[1].lower() in IMAGE_EXTENSIONS


def start_video(video_path):
    global is_video_playing, video_process
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    try:
        # "C:\Program Files\VideoLAN\VLC\vlc.exe" --video-splitter=wall --wall-cols=2 --wall-rows=1 --no-embedded-video --fullscreen --qt-fullscreen-screennumber=0
        # video_process = subprocess.Popen(
        #     [vlc_path, video_path, "--video-splitter=wall", "--wall-cols=2", "--wall-rows=1", "--no-embedded-video", "--fullscreen", "--qt-fullscreen-screennumber=0"]
        # )
        vlc_args = [vlc_path, video_path, "--fullscreen", "--play-and-exit"]
        if args.mute:
            vlc_args.append("--no-audio")
        else:
            vlc_args.append("--audio")
        video_process = subprocess.Popen(vlc_args)
        is_video_playing = True
        print(
            f"動画ファイル {video_path} をVLCで再生開始しました。"
            "Pygameのキー入力を無効にします。"
        )
        return True
    except FileNotFoundError:
        print("エラー: VLC media playerが見つかりません。パスを確認してください。")
    except Exception as e:
        print(f"動画再生中にエラーが発生しました: {e}")
    return False


def set_auto_item(index):
    global current_auto_path, current_image_path
    current_auto_path = auto_files[index]
    if is_video_file(current_auto_path):
        current_image_path = ""
        start_video(current_auto_path)
    elif is_image_file(current_auto_path):
        current_image_path = current_auto_path
    else:
        current_image_path = ""
        print(f"未対応のファイル形式です: {current_auto_path}")


# 起動時タイマー開始ロジック
if auto_mode_active:
    if auto_files:
        print("スクリプト起動時、自動切り替えモードで開始しました")
        pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)
        set_auto_item(current_auto_index)
    else:
        print("autoフォルダに対象ファイルがありません。自動切り替えモードを無効化します。")
        auto_mode_active = False

last_image = pygame.Surface((screen_width, screen_height))
last_image.fill((0, 0, 0))

running = True
while running:
    # --- 動画プロセス終了のチェック ---
    if is_video_playing and video_process:
        # poll() は終了なら終了コード、未終了なら None を返す
        if video_process.poll() is not None:
            is_video_playing = False
            video_process = None
            print("動画再生が終了しました。キー入力を再開します。")
    # ---------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- 自動切り替えイベント処理 ---
        # 動画再生中は自動切り替えも停止
        if (
            event.type == IMAGE_SWITCH_EVENT
            and auto_mode_active
            and not is_video_playing
            and auto_files
        ):
            current_auto_index = (current_auto_index + 1) % len(auto_files)
            special_image_file = ""
            set_auto_item(current_auto_index)
        # -----------------------------------

        # --- 動画再生中はキー入力を無視 ---
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
                    if auto_files:
                        print("自動切り替えモードをONにしました。auto_filesが表示されます")
                        pygame.time.set_timer(IMAGE_SWITCH_EVENT, SWITCH_INTERVAL_MS)
                        current_auto_index = 0
                        special_image_file = ""
                        set_auto_item(current_auto_index)
                    else:
                        print(
                            "autoフォルダに対象ファイルがありません。自動切り替えモードを無効化します。"
                        )
                        auto_mode_active = False
                else:
                    print("自動切り替えモードをOFFにしました。image_filesが表示されます")
                    pygame.time.set_timer(IMAGE_SWITCH_EVENT, 0)
                continue

            # 自動モードOFF時のみ、手動切り替え・動画・特殊キーを処理
            if not auto_mode_active:
                if event.key == pygame.K_SPACE:
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_RIGHT:
                    current_image_index = (current_image_index + 1) % len(image_files)
                elif event.key == pygame.K_LEFT:
                    current_image_index = (current_image_index - 1) % len(image_files)

                # --- 動画再生キー (Vキー) の処理 ---
                elif event.key == pygame.K_v:
                    start_video(video_file_path)
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

    # --- 画像の選択と読み込み（動画再生中も背景は更新） ---
    if special_image_file != "":
        image = pygame.image.load(special_image_file)
        image = pygame.transform.scale(image, (screen_width, screen_height))
        last_image = image
    elif auto_mode_active:
        if current_image_path and is_image_file(current_image_path):
            image = pygame.image.load(current_image_path)
            image = pygame.transform.scale(image, (screen_width, screen_height))
            last_image = image
    else:
        current_image_index = current_image_index % len(image_files)
        image = pygame.image.load(image_files[current_image_index])
        image = pygame.transform.scale(image, (screen_width, screen_height))
        last_image = image

    # 画像を各ディスプレイに描画
    image_to_draw = last_image
    screen1.blit(image_to_draw, (0, 0))
    if screen2 is not None:
        screen2.blit(image_to_draw, (0, 0))

    # 画面を更新
    pygame.display.flip()

pygame.quit()
