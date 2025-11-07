import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def launch_script():
    """選択されたスクリプトを指定されたPythonバージョンで実行します。"""
    python_version = version_entry.get()
    script_path = filedialog.askopenfilename(title="実行するスクリプトを選択してください", filetypes=[("Python Files", "*.py")])

    if script_path:
        try:
            # Python実行可能ファイルのパスを生成
            python_executable = f"python{python_version}.exe"

            # スクリプトを実行
            subprocess.run([python_executable, script_path], check=True)
            # messagebox.showinfo("成功", "スクリプトが成功裏に実行されました。")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("エラー", f"スクリプトの実行中にエラーが発生しました: {e}")
        except FileNotFoundError:
            messagebox.showerror("エラー", f"指定されたPythonバージョン '{python_version}' が見つかりません。")
    else:
        messagebox.showwarning("警告", "スクリプトが選択されませんでした。")

# GUIのセットアップ
root = tk.Tk()
root.title("Python スクリプトランチャー")

tk.Label(root, text="Pythonのバージョン:").grid(row=0, column=0, padx=10, pady=5)
version_entry = tk.Entry(root)
version_entry.grid(row=0, column=1, padx=10, pady=5)
version_entry.insert(0, "3.10")  # デフォルトのPythonバージョンを設定

launch_button = tk.Button(root, text="スクリプトを実行", command=launch_script)
launch_button.grid(row=1, columnspan=2, pady=10)

root.mainloop()