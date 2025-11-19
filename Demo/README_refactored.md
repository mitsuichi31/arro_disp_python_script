# 画像・動画表示アプリケーション - リファクタリング版

## 概要

このアプリケーションは、複数のディスプレイに画像を表示し、自動切り替えや動画再生をサポートするPygameベースのプログラムです。リファクタリング版では、オブジェクト指向設計により、保守性と拡張性が大幅に向上しています。

## 主な機能

- **マルチディスプレイ対応**: 2つ以上のディスプレイに同じ画像を表示
- **自動切り替えモード**: 設定した間隔で画像を自動的に切り替え
- **手動切り替えモード**: キーボード操作で画像を手動で切り替え
- **動画再生**: VLCメディアプレイヤーを使用した全画面動画再生
- **特殊画像表示**: 特定のキーで特別な画像を表示

## システム要件

### 必須環境
- Python 3.7以上
- 2台以上のディスプレイ
- VLC Media Player

### 必要なパッケージ
```bash
pip install pygame pillow
```

## ディレクトリ構成

```
Demo/
├── disp_keys_auto_video2screen_refactored.py  # リファクタリング版メインスクリプト
├── images/                                     # 標準画像フォルダ
│   ├── 1.png
│   ├── 2.png
│   ├── start.png
│   ├── stop.png
│   └── ...
├── all/                                        # 特殊画像フォルダ
│   ├── 1.png
│   └── ...
├── FCT/                                        # 自動モード用画像・動画フォルダ
│   ├── welcome.png
│   └── video.mp4
├── zhaodi/                                     # 方向指示画像フォルダ
│   ├── start-3.png
│   ├── stop-3.png
│   ├── left-3.png
│   └── right-3.png
└── welcome/                                    # ウェルカム画像フォルダ
    └── welcome.png
```

## 使用方法

### 起動方法

```bash
python disp_keys_auto_video2screen_refactored.py
```

アプリケーションは自動切り替えモードで起動します。

### キー操作

#### 基本操作
| キー | 機能 | モード |
|------|------|--------|
| `T` | 自動/手動モード切り替え | すべて |
| `ESC` | アプリケーション終了 | 手動 |

#### 手動モード専用操作
| キー | 機能 |
|------|------|
| `Space` | 次の画像へ |
| `→` (右矢印) | 次の画像へ |
| `←` (左矢印) | 前の画像へ |
| `V` | 動画再生 |

#### 特殊画像表示（手動モードのみ）
| キー | 表示内容 |
|------|----------|
| `S` | スタート画像 (`./zhaodi/start-3.png`) |
| `E` | ストップ画像 (`./zhaodi/stop-3.png`) |
| `L` | 左方向画像 (`./zhaodi/left-3.png`) |
| `R` | 右方向画像 (`./zhaodi/right-3.png`) |
| `A` | 特殊画像を順次切り替え (`./all/` 内の画像) |
| `W` | ウェルカム画面の表示/非表示切り替え |

## アーキテクチャ

### クラス構成

#### 1. `DisplayConfig`
**役割**: アプリケーションの設定を管理

```python
@dataclass
class DisplayConfig:
    width: int = 2160              # ディスプレイ幅
    height: int = 3840             # ディスプレイ高さ
    switch_interval_ms: int = 5000 # 自動切り替え間隔（ミリ秒）
    required_displays: int = 2     # 必要なディスプレイ数
    vlc_path: str                  # VLCのパス
```

#### 2. `ImagePaths`
**役割**: 画像ファイルパスの管理

- `image_files`: 手動モードで使用する画像リスト
- `special_files`: 特殊表示用画像リスト
- `auto_files`: 自動モードで使用する画像リスト
- `video_file`: 動画ファイルのパス

#### 3. `VideoPlayer`
**役割**: 動画再生の管理

**主要メソッド**:
- `play(video_path)`: 動画再生開始
- `update()`: 再生状態の確認
- `stop()`: 再生停止

**特徴**:
- VLCを外部プロセスとして起動
- 再生終了の自動検出
- 再生中はキー入力を無効化

#### 4. `ImageManager`
**役割**: 画像の選択と状態管理

**主要メソッド**:
- `get_current_image_path(mode)`: 現在表示すべき画像のパスを取得
- `advance_image(forward)`: 画像を前後に切り替え
- `advance_auto()`: 自動モードで次の画像へ
- `set_special_image(path)`: 特殊画像を設定
- `cycle_special_all()`: 特殊画像を順次切り替え
- `toggle_welcome()`: ウェルカム画面の表示切り替え

**管理する状態**:
- 現在の画像インデックス
- 自動モード用インデックス
- 特殊画像インデックス
- 特殊画像ファイルパス
- ウェルカムフラグ

#### 5. `DisplayApplication`
**役割**: アプリケーション全体の制御

**主要メソッド**:
- `run()`: メインループの実行
- `_setup_displays()`: ディスプレイの初期化
- `_handle_events()`: イベント処理
- `_handle_keydown(key)`: キーボード入力処理
- `_render()`: 画像のレンダリング
- `cleanup()`: リソースの解放

### 動作モード

#### 自動モード (`DisplayMode.AUTO`)
- 起動時のデフォルトモード
- 5秒間隔で自動的に画像を切り替え
- `auto_files` リストの画像を順次表示
- Tキーで手動モードに切り替え可能

#### 手動モード (`DisplayMode.MANUAL`)
- ユーザーのキー操作で画像を切り替え
- `image_files` リストの画像を使用
- すべてのキー操作が有効
- Tキーで自動モードに戻る

### 動画再生機能

1. **再生開始**: Vキー押下でVLCが起動
2. **入力無効化**: 再生中はすべてのキー入力を無視
3. **自動終了検出**: VLCプロセスの終了を監視
4. **復帰**: 動画終了後、自動的にキー入力が有効化

## カスタマイズ

### 画像パスの変更

`ImagePaths.default()` メソッド内で画像パスを編集：

```python
@classmethod
def default(cls):
    return cls(
        image_files=["./images/1.png", ...],  # 手動モード用
        special_files=["./all/1.png", ...],    # 特殊画像用
        auto_files=["./FCT/welcome.png", ...], # 自動モード用
        video_file="./FCT/video.mp4"           # 動画ファイル
    )
```

### 設定の変更

`DisplayConfig` クラスで設定を調整：

```python
config = DisplayConfig(
    width=2160,                    # ディスプレイ幅
    height=3840,                   # ディスプレイ高さ
    switch_interval_ms=5000,       # 自動切り替え間隔（5秒）
    required_displays=2,           # 必要なディスプレイ数
    vlc_path=r'C:\Program Files\VideoLAN\VLC\vlc.exe'
)
```

### VLCのパス変更

Windowsの場合:
```python
vlc_path = r'C:\Program Files\VideoLAN\VLC\vlc.exe'
```

### 自動切り替え間隔の変更

```python
switch_interval_ms = 5000  # 5秒
switch_interval_ms = 3000  # 3秒に変更
```

## リファクタリングの改善点

### 元のスクリプトからの主な変更

1. **オブジェクト指向設計**
   - 機能ごとにクラスを分離
   - 責任範囲の明確化
   - 再利用性の向上

2. **型ヒント対応**
   - すべての関数に型注釈を追加
   - IDE補完のサポート向上
   - バグの早期発見

3. **エラーハンドリング強化**
   - 画像読み込みエラーの捕捉
   - わかりやすいエラーメッセージ
   - 安全な終了処理

4. **コードの可読性向上**
   - 説明的なメソッド名
   - 適切なコメントとドキュメント
   - ロジックの単純化

5. **保守性の向上**
   - 設定の一元管理
   - マジックナンバーの排除
   - 定数の明確化

6. **状態管理の改善**
   - Enumによるモード管理
   - ブール値の適切な使用
   - 状態の一貫性保証

## トラブルシューティング

### ディスプレイが検出されない
- 2台以上のディスプレイが接続されているか確認
- ディスプレイの設定で拡張モードになっているか確認

### 画像が表示されない
- 画像ファイルパスが正しいか確認
- 画像ファイルが存在するか確認
- エラーメッセージをコンソールで確認

### 動画が再生されない
- VLC Media Playerがインストールされているか確認
- `vlc_path` が正しいか確認
- 動画ファイルが存在するか確認

### 自動切り替えが動作しない
- Tキーで自動モードがONになっているか確認
- コンソールで「Auto mode enabled」が表示されているか確認

## 開発者向け情報

### 新機能の追加方法

#### 新しいキーバインドの追加
`_handle_manual_mode_keys()` メソッドに追加：

```python
elif key == pygame.K_n:  # 新しいキー
    self.image_manager.set_special_image("./new/image.png")
```

#### 新しい画像セットの追加
`ImagePaths` クラスに新しいリストを追加：

```python
@dataclass
class ImagePaths:
    new_files: List[str]  # 新しい画像セット
```

### テスト実行

```python
# 設定のテスト
config = DisplayConfig()
assert config.width == 2160

# 画像パスのテスト
paths = ImagePaths.default()
assert len(paths.image_files) > 0
```

## ライセンス

このスクリプトは内部使用を目的としています。

## バージョン履歴

- **v2.0 (リファクタリング版)**
  - オブジェクト指向設計に全面刷新
  - 型ヒント対応
  - エラーハンドリング強化
  - ドキュメント整備

- **v1.0 (オリジナル版)**
  - 基本機能実装
  - マルチディスプレイ対応
  - 自動/手動モード切り替え
  - 動画再生機能

## お問い合わせ

問題が発生した場合は、エラーメッセージとともに開発チームにご連絡ください。
