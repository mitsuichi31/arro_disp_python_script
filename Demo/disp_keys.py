import pygame
import os
from PIL import Image

def get_image_files(directory):
    image_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".gif"):
            image_files.append(os.path.join(directory, filename))
    return image_files

# PillowによるGIFの読み込みとフレームの取得
def load_gif_frames(filename):
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

# image_files = get_image_files("./gifs") # カレントディレクトリからPNGファイルを検索
image_files = ["./images/1.png", "./images/start.png", "./images/2.png", "./images/3.png", "./images/4.png",
               "./images/5.png", "./images/6.png",     "./images/7.png", "./images/8.png",
               "./images/9.png", "./images/10.png",    "./images/stop.png"]  # 例
special_files = ["./all/1.png", "./all/2.png", "./all/3.png", "./all/4.png", "./all/5.png",
               "./all/6.png", "./all/7.png"]  # 例

pygame.init()

# ディスプレイの数を取得
num_displays = pygame.display.get_num_displays()
desktop_sizes = pygame.display.get_desktop_sizes()

# 2つのディスプレイが存在するか確認
if num_displays < 2:
    print("2つのディスプレイが必要です。")
    pygame.quit()
    exit()

# 2つのディスプレイをフルスクリーンで初期化
# screen1 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)
# screen2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=1)
# screen1 = pygame.display.set_mode(desktop_sizes[0], pygame.FULLSCREEN, display=0)
# screen2 = pygame.display.set_mode(desktop_sizes[1], pygame.FULLSCREEN, display=1)
width = 2160
height = 3840

screen0 = pygame.display.set_mode((width*3, height)) # ((3240+3240, 3840))
screen1 = screen0.subsurface(pygame.Rect(width, 0, width, height))
screen2 = screen0.subsurface(pygame.Rect(width*2, 0, width, height))


screen_width, screen_height = screen1.get_size()

# images = []
# for file in image_files:
#     image = pygame.image.load(file)
#     # 画像を画面サイズにリサイズ
#     image = pygame.transform.scale(image, (screen_width, screen_height))
#     images.append(image)

current_image_index = 0
special_image_file = ""
current_special_index = 0
welcome_flag = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            special_image_file = ""
            if event.key == pygame.K_SPACE:  # スペースキーで画像を切り替え
                current_image_index = (current_image_index + 1) % len(image_files)
            elif event.key == pygame.K_RIGHT:  # ->で画像を切り替え
                current_image_index = (current_image_index + 1) % len(image_files)
            elif event.key == pygame.K_LEFT:  # ->で画像を切り替え
                current_image_index = (current_image_index - 1) % len(image_files)
            elif event.key == pygame.K_ESCAPE: # ESCキーで終了
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

    if special_image_file != "":
        image = pygame.image.load(special_image_file)
    else:
        image = pygame.image.load(image_files[current_image_index])

    # 画像を画面サイズにリサイズ
    image = pygame.transform.scale(image, (screen_width, screen_height))

    # 画像をそれぞれのディスプレイに描画
    image_to_draw = image # images[current_image_index]
    screen1.blit(image_to_draw, (0, 0))
    screen2.blit(image_to_draw, (0, 0))

    # 画面を更新
    pygame.display.flip()

pygame.quit()