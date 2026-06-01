import cv2
import yt_dlp

def capture_youtube_screenshots(youtube_url, num_samples=10):
    """
    YouTubeのURLから指定された枚数のスクリーンショットを取得する関数（超安定版）
    """
    # 1段階目：まずは動画のタイトルなどの基本情報だけを、一番軽い設定で取得
    ydl_opts_basic = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts_basic) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        video_title = info.get('title', '無題の動画')

    # 2段階目：OpenCVが100%読み込める「mp4形式」の配信URLだけを安全に抽出
    ydl_opts_url = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts_url) as ydl:
        # 短縮URLなどあらゆるURLを一度解析し直す
        info_url = ydl.extract_info(youtube_url, download=False)
        # もし複数のフォーマットがある場合は最適なURLを選択
        if 'requested_formats' in info_url:
            video_url = info_url['requested_formats'][0]['url']
        else:
            video_url = info_url['url']

    # OpenCVで解析
    cap = cv2.VideoCapture(video_url)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 安全策
    if total_frames <= 0:
        total_frames = 1000 

    interval = total_frames // num_samples
    images = []

    for i in range(num_samples):
        frame_id = i * interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        
        # 正常にフレームが読み込めた場合だけ処理
        if ret and frame is not None and frame.size > 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            images.append(frame_rgb)

    cap.release()
    
    # 1枚も読み込めなかった場合の最終エラーハンドリング
    if len(images) == 0:
        raise ValueError("動画の映像データを展開できませんでした。")

    return video_title, images