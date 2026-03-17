import os
import random
import tweepy
from openai import OpenAI

# =====================
# 環境変数から取得
# =====================

consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_SECRET")

openai_key = os.getenv("OPENAI_KEY")

# =====================
# 認証
# =====================

auth = tweepy.OAuth1UserHandler(
    consumer_key,
    consumer_secret,
    access_token,
    access_secret
)

api = tweepy.API(auth)
client = OpenAI(api_key=openai_key)

# =====================
# 写真取得
# =====================

def get_photo():
    folders = ["photos/sea", "photos/town", "photos/guesthouse"]
    folder = random.choice(folders)
    photos = os.listdir(folder)
    photo = random.choice(photos)
    return os.path.join(folder, photo)

# =====================
# AI文章
# =====================

def generate_caption():
    prompt = "瀬戸内のゲストハウスの魅力的な投稿文を80文字以内＋ハッシュタグ付きで作成"
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content

# =====================
# 投稿
# =====================

def post():
    photo = get_photo()
    caption = generate_caption()

    media = api.media_upload(photo)

    api.update_status(
        status=caption,
        media_ids=[media.media_id]
    )

# =====================
# フォロワー増殖
# =====================

def grow():
    tweets = api.search_tweets(q="#香川旅行", count=5)

    for t in tweets:
        try:
            api.create_favorite(t.id)
            api.create_friendship(t.user.id)
        except:
            pass

# =====================
# 実行
# =====================

if __name__ == "__main__":
    post()
    grow()
