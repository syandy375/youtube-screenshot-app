import streamlit as st
# screenshot_logic.py から関数を読み込む
from screenshot_logic import capture_youtube_screenshots

# WEBページのタイトル設定
st.title("📺 YouTubeスクショ生成")
st.write("URLを入力すると、動画から等間隔で10枚のスクリーンショットを自動生成します。")

# 1. URLを入力するテキストボックス
youtube_url = st.text_input("YouTubeのURLを入力してください", placeholder="https://www.youtube.com/watch?v=...")

# 「スクショ生成」ボタンが押されたら処理をスタート
if st.button("スクショを生成する"):
    if youtube_url:
        # 🔒 【セキュリティ対策】YouTubeのURLかどうかを簡易チェック
        if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
            st.error("エラー: YouTubeの動画URLを入力してください。安全のため、その他のURLは処理できません。")
        else:
            # 安全が確認できたら処理を開始
            with st.spinner("高画質で解析中... 少々お待ちください"):
                try:
                    # 別のファイル(screenshot_logic)の関数を実行
                    title, images = capture_youtube_screenshots(youtube_url)
                    
                    st.success("完了しました！")
                    st.subheader(f"動画タイトル: {title}")
                    
                    # 画面を縦2列（グリッド状）にして、綺麗に画像を表示する
                    cols = st.columns(2) 
                    for idx, img in enumerate(images):
                        with cols[idx % 2]:
                            st.image(img, caption=f"{idx + 1}枚目のスクショ", width="stretch")
                            
                except Exception as e:
                    # 万が一yt-dlp側でエラーが出ても、Webページがクラッシュしないように守る
                    st.error(f"動画の解析中にエラーが発生しました。URLが正しいか確認してください。")
    else:
        st.warning("URLを入力してください。")