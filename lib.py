import DaVinciResolveScript as dvr_script
import time
import os

resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()

# ボイス保存用ビン。もしサブフォルダなどを指定したければ "a/b/c" のように "/" で区切る。
VOICE_FOLDER = "voice"

# パスを受け取ったフォルダを返す。見つからなかったら None
# 主な用途は "voice" を渡して声用フォルダを取得。
def relativeFolder(path):
    mediaPool = project.GetMediaPool()
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
def createFolder(path):
    mediaPool = project.GetMediaPool()
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

def voiceFolder():
    return relativeFolder(VOICE_FOLDER)

def createVoiceFolder():
    return createFolder(VOICE_FOLDER)

def addToVoiceFolder(files):
    mediaPool = project.GetMediaPool()

    # 後で戻す用
    prev = mediaPool.GetCurrentFolder()
    # ボイス用フォルダを開く、なかったら作る。
    voice = voiceFolder()
    if voice == None:
        voice = createVoiceFolder()
    mediaPool.SetCurrentFolder(voice)

    # FIXME: re-link とかしたほうがよい？
    ret = mediaPool.ImportMedia(files)

    # 元のフォルダに戻す。
    mediaPool.SetCurrentFolder(prev)

    return ret

def frameToTimecode(frame):
    # TODO: 01:00:00 以外からもスタートできるようにする。
    frameRate = project.GetSetting("timelineFrameRate")
    # 秒の計算で余りが出ると面倒なので先にフレームの部分だけ計算しておく。
    remainder = frame % frameRate
    frame -= remainder
    second = frame / frameRate
    hour = second // (60 * 60)
    second -= hour * (60 * 60)
    minute = second // 60
    second -= minute * 60

    return f"%02d:%02d:%02d:%02d"%(hour, minute, second, remainder)

def appendVoiceToTrack(clip, track):
    pass

def backupLockState():
    timeline = project.GetCurrentTimeline()
    lockState = {
        "video": [],
        "audio": [],
        "subtitle": []
    }
    # Track の index は 1-based
    for trackType in lockState:
        for i in range(timeline.GetTrackCount(trackType)):
            lockState[trackType].append(timeline.GetIsTrackLocked(trackType, i+1))

    return lockState

def restoreLockState(backupLockState):
    timeline = project.GetCurrentTimeline()
    for trackType in ["video", "audio", "subtitle"]:
        for i in range(timeline.GetTrackCount(trackType)):
            # Track の index は 1-based
            timeline.SetTrackLock(trackType, i+1, backupLockState[trackType][i])

def lockAllTracks():
    timeline = project.GetCurrentTimeline()
    for trackType in ["video", "audio", "subtitle"]:
        for i in range(timeline.GetTrackCount(trackType)):
            # Track の index は 1-based
            timeline.SetTrackLock(trackType, i+1, True)

def insertTextPlusToTrack(track, frame):
    timeline = project.GetCurrentTimeline()
    # 後で戻す用
    prevTimecode = timeline.GetCurrentTimecode()
    prevLockState = backupLockState()

    timeline.SetCurrentTimecode(frameToTimecode(frame))

    # 一度すべての他の video track を lock する。
    # これは insert が lock されていない最初の track に insert するため
    # (この仕様もどうかと思うけど……)
    # ちなみに lock するための API は unofficial なのでそのうち動かなくなるかもしれない
    # https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040
    lockAllTracks()
    timeline.SetTrackLock("video", track, False)
    ret = timeline.InsertFusionTitleIntoTimeline("Text+")

    # 処理が終わったら timecode と lock 状態を戻しておく
    timeline.SetCurrentTimecode(prevTimecode)
    restoreLockState(prevLockState)
    return ret

def writeTextToTextPlus(item, text):
    fusion = item.GetFusionCompByIndex(1) #FIXME: これでいいんだろうか？
    fusion.Template.StyledText = text

def addToTimeline(clips):
    timeline = project.GetCurrentTimeline()
    mediaPool = project.GetMediaPool()

    items = mediaPool.AppendToTimeline(clips)
    return items