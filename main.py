#!/usr/bin/env python
#coding: utf-8

# DaVinci Resolve のコンソールで動かす用
# import sys
# sys.path.append("C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\")

# 一般 => 外部スクリプトに使用

import DaVinciResolveScript as dvr_script
import os

resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()

# ボイス保存用ビン。もしサブフォルダなどを指定したければ "a/b/c" のように "/" で区切る。
VOICE_FOLDER = "voice"

# パスを受け取ったフォルダを返す。見つからなかったら None
# 主な用途は "voice" を渡して声用フォルダを取得。
def relativeFolder(mediaPool, path):
    root = mediaPool.GetRootFolder()
    cur = root
    path = path.split("/")
    while len(path) != 0:
        for sub in cur.GetSubFolderList():
            if sub.GetName() == path[0]:
                path = path[1:]
                cur = sub
                break
        else:
            return None
    return cur

# パスがなかったら作る用
def createFolder(mediaPool, path):
    root = mediaPool.GetRootFolder()
    cur = root
    path = path.split("/")
    while len(path) != 0:
        for sub in cur.GetSubFolderList():
            if sub.GetName() == path[0]:
                path = path[1:]
                cur = sub
                break
        else:
            cur = mediaPool.AddSubFolder(cur, path[0])
            path = path[1:]
    return cur

def voiceFolder(mediaPool):
    return relativeFolder(mediaPool, VOICE_FOLDER)

def createVoiceFolder(mediaPool):
    return createFolder(mediaPool, VOICE_FOLDER)

def addToVoiceFolder(mediaPool, files):
    # 後で戻す用
    prev = mediaPool.GetCurrentFolder()
    # ボイス用フォルダを開く、なかったら作る。
    voice = voiceFolder(mediaPool)
    if voice == None:
        voice = createVoiceFolder(mediaPool)
    mediaPool.SetCurrentFolder(voice)

    # FIXME: いい感じに re-link とかしたほうがよい？
    mediaPool.ImportMedia(files)

    # 元のフォルダに戻す。
    mediaPool.SetCurrentFolder(prev)

# addToVoiceFolder(project.GetMediaPool(), "C:\\Users\\tomoki\\Videos\\gopro\\nagoya\\voice\\1-0.wav")