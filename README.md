
# 動かし方

## 環境

とりあえず以下の環境で動くように作っています。

- Windows 10
- [python 3.6.15](https://www.python.org/downloads/release/python-3615/)
- DaVinci Resolve Studio 17.4.3

Powershell での動かし方です。

```powershell
.\setenv.ps1
# 初回起動時のみ
python -m venv venv; pip install -r requirements.txt
python main.py 
```

# Trouble shooting

- Python 3.6 を使うこと。

# メモ

- https://twitter.com/nu_ro_ku/status/1475874975924236289?s=20
- https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040