import cv2
import yt_dlp

def capture_youtube_screenshots(youtube_url, num_samples=10):
    """
    YouTubeのURLから指定された枚数のスクリーンショットを取得する関数
    """
    # ✨ 短縮URLや様々な形式に対応できるよう、設定を強化
    ydl_opts = {
        'format': 'bestvideo/best', 
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False, # 動画のディープな情報までしっかり抽出する設定
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        video_url = info['url']
        video_title = info.get('title', '無題の動画')

    # OpenCVで解析
    cap = cv2.VideoCapture(video_url)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 万が一、動画全体のフレーム数がうまく取得できなかった場合の安全策
    if total_frames <= 0:
        total_frames = 1000 

    interval = total_frames // num_samples
    images = []

    for i in range(num_samples):
        frame_id = i * interval
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        
        # ✨ ちゃんと画像が読み込めた（中身が空っぽじゃない）場合だけリストに追加する
        if ret and frame is not None and frame.size > 0:
            # OpenCVの画像(BGR)をStreamlit用(RGB)に変換
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            images.append(frame_rgb)

    cap.release()
    
    # 万が一、1枚も読み込めなかった場合はエラーを出す
    if len(images) == 0:
        raise ValueError("動画の映像データを読み込めませんでした。通常のURL（youtube.com/watch?v=...）でお試しいただくか、別の動画で再度実行してください。")

    return video_title, images