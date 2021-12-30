#!/usr/bin/env python
#coding: utf-8

# DaVinci Resolve のコンソールで動かす用
# import sys
# sys.path.append("C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\")

import lib

import time
import os
import sys
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        filePath = event.src_path
        # FIXME: watchdog が追加を検知した瞬間には DaVinci Resolve に追加できないっぽい？
        # voiceroid 側で区切り文字を設定して複数ファイルを同時に書き出した場合、
        # 瞬間的にのみ作られるファイルの可能性がある。なのでちょっと待ってから存在をチェック
        time.sleep(0.1)
        if os.path.exists(filePath) and os.path.splitext(filePath)[1] == ".wav":
            print("add " + filePath)
            addedClips = lib.addToVoiceFolder(filePath)
            addedItems = lib.addToTimeline(addedClips)
            correspondingTxtFilePath = os.path.splitext(filePath)[0] + ".txt"
            if os.path.exists(correspondingTxtFilePath):
                with open(correspondingTxtFilePath, mode="r", encoding="cp932") as txtFile:
                    txt = txtFile.read()
                    for item in addedItems:
                        lib.writeTextToTextPlus(lib.insertTextPlusToTrack(2, item.GetStart()), txt)

    # FIXME: 他のイベントも見たほうがよいだろうか？

if len(sys.argv) != 2:
    print("Usage: python main.py directory-to-watch")
    exit(1)

directoryToWatch = sys.argv[1]
# event_handler = LoggingEventHandler()
event_handler = FileEventHandler()

observer = Observer()
observer.schedule(event_handler, directoryToWatch, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()