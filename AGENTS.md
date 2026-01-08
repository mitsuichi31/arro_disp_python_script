# Repository Guidelines

## プロジェクト構成とモジュール
このリポジトリはWindows向けのPythonデモです。主要なファイルはすべて`Demo/`配下にあります。
- `Demo/*.py`: 実行用スクリプト（pygame表示、Tkinterランチャー）。
- `Demo/*.ps1`: PowerShellの起動用スクリプト。
- `Demo/images`、`Demo/all`、`Demo/welcome`、`Demo/zhaodi`: 画像アセット。
- `Demo/FCT`: デモ用アセット（`video.mp4`など）。

相対パス参照が多いため、実行は基本的に`Demo/`から行ってください。

## ビルド・テスト・開発コマンド
ビルド工程はありません。Pythonを直接実行します。
- `cd Demo`
- `python .\disp_keys_auto_video.py`（自動スライド＋動画）
- `python .\disp_keys_auto_video2screen.py`（2画面想定の自動スライド＋動画）
- `python .\disp_keys_auto.py`（自動スライド）
- `python .\disp_keys.py`（手動キー操作）
- `powershell -ExecutionPolicy Bypass -File .\start.ps1`（ランチャー起動）
- `powershell -ExecutionPolicy Bypass -File .\auto_start.ps1`（自動動画デモ）

## コーディングスタイルと命名
- Pythonは4スペースインデント、PEP 8を目安にします。
- 画像ファイル名は既存のリストと整合させてください（例: `images/1.png`）。
- 関数名は意味が伝わる英語名を優先し、略語は既存と整合する場合のみ使用します。

## テスト方針
現在は自動テストがありません。追加する場合は`tests/`を新設し、`test_*.py`形式で命名し、実行手順を本ファイルに追記してください。

## コミット・PRガイドライン
直近の履歴はConventional Commits風（例: `feat:`）です。新規コミットも`feat:`/`fix:`/`chore:`を使ってください。PRには以下を含めます。
- 変更内容の要約
- 対象スクリプトと確認方法
- 画面表示に影響がある場合はスクリーンショットまたは短い動画

## 設定と実行時の注意
- 依存関係: `pygame`、`Pillow`（`tkinter`は標準）。
- 動画再生はVLCを前提にしており、`Demo/disp_keys_auto_video.py`内の`vlc_path`を必要に応じて更新してください。
- 複数ディスプレイ前提の表示設定があります。

## スクリプト差分
- `Demo/disp_keys_auto_video2screen.py`は現状`Demo/disp_keys_auto_video.py`と内容が同一です（挙動差はありません）。
- 将来差分を作る場合は、2画面向け固有の表示ロジックをこちらに集約する想定です。
