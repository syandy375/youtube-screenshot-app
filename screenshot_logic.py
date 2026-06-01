import cv2
import yt_dlp
import os
import math

def get_video_screenshots(youtube_url, num_screenshots=10):
    """
    YouTube動画から指定された枚数のスクリーンショットを均等な間隔で抽出する関数。
    Streamlit Cloud（Linux環境）でのOpenCVのURL読み込みバグを回避するため、
    一時的に動画ファイルを軽量保存してから処理を行います。
    """
    temp_video_path = "temp_downloaded_video.mp4"
    screenshots = []

    # 1. yt-dlpのダウンロード設定（サーバーに負荷をかけないよう最軽量画質を狙う）
    ydl_opts_download = {
        # 480p以下のmp4形式、それがなければ一番軽い動画をダウンロード
        'format': 'mp4[height<=480]/best[height<=480]/worstvideo', 
        'outtmpl': temp_video_path,
        'overwrites': True,
        'quiet': True,
        'no_warnings': True
    }

    try:
        # YouTubeから動画を一時的にダウンロード
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([youtube_url])
        
        # 2. ダウンロードした「ローカルファイル」をOpenCVで開く（これで100%エラーを回避！）
        cap = cv2.VideoCapture(temp_video_path)
        
        if not cap.isOpened():
            print("エラー: 動画ファイルを開けませんでした。")
            return []

        # 動画の総フレーム数とFPSを取得
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if total_frames <= 0 or fps <= 0:
            print("エラー: 動画のフレーム情報が正しく取得できませんでした。")
            cap.release()
            return []

        # 均等にスクショを撮るための間隔（フレーム数）を計算
        interval = math.floor(total_frames / (num_screenshots + 1))

        # 指定された枚数分、フレームを抜き出す
        for i in range(1, num_screenshots + 1):
            target_frame = interval * i
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            
            ret, frame = cap.read()
            if ret:
                # OpenCVのBGR形式から、画像処理で一般的なRGB形式に変換
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                screenshots.append(frame_rgb)
            else:
                break
                
        cap.release()

    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")
        return []

    finally:
        # 3. 使い終わった一時ファイルをサーバーから確実に削除（お掃除）
        if os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
            except Exception as e:
                print(f"一時ファイルの削除に失敗しました: {e}")

    return screenshots