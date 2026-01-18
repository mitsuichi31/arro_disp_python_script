# arro_disp_python_script

Windows向けのPygame/Tkinterデモです。相対パス参照が多いので、実行は `Demo/` から行ってください。

## 前提・依存

- Python 3.x
- pygame
- Pillow
- VLC media player（動画再生用、`disp_keys_auto_video*.py`）

## ディレクトリ構成（主要）

- `Demo/*.py`: 実行用スクリプト
- `Demo/*.ps1`: PowerShellの起動用スクリプト
- `Demo/images`: 画像アセット（メインスライド）
- `Demo/all`: 特殊表示の画像アセット（Aキーで巡回）
- `Demo/welcome`: ウェルカム画像
- `Demo/zhaodi`: 方向/開始/停止の画像
- `Demo/auto`: 自動切り替え用アセット（画像/動画、`disp_keys_auto_video2screen.py`）
- `Demo/FCT`: デモ用アセット（`video.mp4`, `welcome.png` など）

## 実行方法

```powershell
cd Demo
python .\disp_keys.py
```

起動用スクリプトも利用できます。

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
powershell -ExecutionPolicy Bypass -File .\auto_start.ps1
```

## スクリプト一覧と使い方

### `Demo/disp_keys.py`

- **機能**: 手動キー操作のスライド表示。2画面前提で同一画像を左右に表示。
- **使用フォルダ**:
  - `./images`（`image_files` 固定リスト）
  - `./all`（Aキーで巡回表示）
  - `./welcome`、`./zhaodi`
- **主なキー**:
  - `Space` / `→` / `←`: 画像切り替え
  - `S` / `E` / `L` / `R`: `zhaodi` の開始/停止/左/右画像
  - `A`: `./all` を順番に表示
  - `W`: `./welcome/welcome.png` のトグル
  - `Esc`: 終了
- **注意**: ディスプレイ2枚以上が必要です（内部でチェックあり）。

### `Demo/disp_keys_auto.py`

- **機能**: 手動 + 自動切り替え（Tキーで切り替え）。
- **自動切り替え**: 3秒間隔で `auto_files` を巡回。
- **使用フォルダ**:
  - `./images`（手動用 `image_files`）
  - `./images`（自動用 `auto_files`、画像のみ固定リスト）
  - `./all`、`./welcome`、`./zhaodi`
- **主なキー**:
  - `T`: 自動切り替え ON/OFF
  - 手動操作時は `disp_keys.py` と同じキーが有効
- **注意**: 2画面前提。

### `Demo/disp_keys_auto_video.py`

- **機能**: 自動切り替え + 動画再生（VLC起動）。起動時は自動モード ON。
- **自動切り替え**: 5秒間隔で `auto_files` を巡回。
- **使用フォルダ**:
  - `./images`（手動 `image_files`）
  - `./FCT`（`welcome.png`, `video.mp4` など）
  - `./all`、`./welcome`、`./zhaodi`
- **動画**:
  - `video_file_path = "./FCT/video.mp4"`
  - `V` キーで VLC を起動して再生
  - 再生中はキー入力が無効（終了すると復帰）
  - VLCパスは `vlc_path` で指定
- **主なキー**:
  - `T`: 自動切り替え ON/OFF
  - `V`: 動画再生
  - 手動モード時は `disp_keys.py` と同じキーが有効
- **注意**: 2画面前提。

### `Demo/disp_keys_auto_video2screen.py`

- **機能**: 自動切り替え（画像/動画）+ 動画再生。オプションで単一画面テスト可。
- **自動切り替え**:
  - `./auto` 内の画像/動画をファイル名順に自動検出（`auto_files`）
  - 5秒間隔で巡回、動画ファイルの場合は自動で VLC 再生
- **使用フォルダ**:
  - `./auto`（自動切り替え用の画像/動画）
  - `./images`（手動 `image_files`）
  - `./FCT/video.mp4`（手動動画再生用）
  - `./all`、`./welcome`、`./zhaodi`
- **引数**:
  - `--test`: 単一画面モード（画面サイズは自動取得）
  - `--mute`: 動画を無音（デフォルト）
  - `--with-audio`: 動画を有音
- **環境変数**:
  - `VLC_AUDIO_DEVICE`: VLCの出力デバイス指定（必要時のみ）
    - `disp_keys_auto_video2screen.py` は `VLC_AUDIO_DEVICE` を読み取り、`--directx-audio-device` として VLC に渡します。
    - DirectSound/DirectX のデバイス名をそのまま指定してください（例: Windows のサウンド設定に表示される名称）。
    - 設定しない場合は VLC の既定デバイスが使われます。
    - 例（PowerShell）:
      ```powershell
      $env:VLC_AUDIO_DEVICE = "スピーカー (Realtek(R) Audio)"
      python .\disp_keys_auto_video2screen.py --with-audio
      ```
    - 例（一時的に 1 コマンドだけ適用）:
      ```powershell
      $env:VLC_AUDIO_DEVICE = "USB Audio Device"; python .\disp_keys_auto_video2screen.py --with-audio
      ```
- **主なキー**:
  - `T`: 自動切り替え ON/OFF
  - `V`: `video_file_path` を手動再生
  - `B`: 動画再生中の停止
  - `Esc`: 終了
  - 手動モード時は `disp_keys.py` と同じ特殊キーが有効
- **注意**:
  - 通常は2画面前提。`--test` で単一画面テスト可能。
  - VLCのパスは `start_video()` 内の `vlc_path` を参照。

### `Demo/launcher.py`

- **機能**: Tkinterベースのスクリプト起動ランチャー。
- **使い方**: Pythonバージョンを入力し、実行する `.py` を選択して起動。
- **注意**: `pythonX.exe`（例: `python3.11.exe`）がPATH上にある前提。

### `Demo/start.ps1`

- **機能**: `launcher.py` を起動。
- **実行**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\start.ps1
  ```

### `Demo/auto_start.ps1`

- **機能**: `disp_keys_auto_video.py` を起動。
- **実行**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .\auto_start.ps1
  ```

## 補足

- ほとんどのスクリプトは2ディスプレイ前提です。単一画面での動作確認は `disp_keys_auto_video2screen.py --test` を使用してください。
- 相対パス前提のため、`Demo/` から起動してください。
