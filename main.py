import streamlit as st
import io
import requests
from PIL import Image, ImageDraw, ImageFont

# Azureの顔認識APIを読込む
# APIのキー１
subscription_key = 'b2c098dbbb6f456d904c2846136aefd0'
assert subscription_key
# APIのエンドポイント
face_api_url = 'https://20211111facecogni.cognitiveservices.azure.com/face/v1.0/detect'

st.title('Azure Face API 顔認識アプリ')

# アップロード画像を読込み
uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    # 画像読込
    img = Image.open(uploaded_file)
    # 画像をバイナリデータへ変換しAPIへ投げる必要がある
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() # バイナリ取得

    # 顔認識API問合せ
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
        }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes' : 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()
    # フォント準備
    def_font = ImageFont.load_default()
    # 顔認識情報テキスト背景色
    bg_color = (255,255, 255)

    # 複数人検出
    for result in results:
        # 顔認識情報で必要なものを取得
        rect = result['faceRectangle']
        age = result['faceAttributes']['age']
        gender = result['faceAttributes']['gender']
        emo = result['faceAttributes']['emotion']
        text = " " +gender + str(age) + " "

        # 性別による色分け
        color = 'green'
        if gender == 'female':
            color = 'red'
        else:
            color = 'blue'

        # 顔認識の結果表示
        draw = ImageDraw.Draw(img)
        # 矩形描画　左上、右下を指定
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline=color, width=2)
        # 文字サイズ
        txw, txh = draw.textsize(text, font=def_font)
        # 顔認識情報テキスト位置
        txpos = (rect['left'], rect['top'] - txh)
        # 顔認識情報テキストの背景
        draw.rectangle([(rect['left'], rect['top'] - txh), (rect['left'] + txw, rect['top'])], fill=bg_color, outline=color, width=2)
        # テキストを表示
        draw.text(txpos, text, font=def_font, fill=color)





    st.image(img, caption='Uploaded Image.', use_column_width=True)

st.write('presented by O.Naohiro')


