from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage,
)

import random

app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    bot_reply = "你好啊，我對某些留言會有特殊回應喔！向我「哈囉」看看！"
    # single or multiple line, line allow multi-line reply in list form
    multi_line = 0
    # sticker package id and sticekr id
    s_pid = 1
    s_id = 1

    if msg in ["哈囉", "你好"]:
        bot_reply = "你好，我是測試用聊天機器人！"
    elif msg in ["機器人", "聊天機器人"]:
        bot_reply = "聊天機器人會根據您輸入的句子做出回應喔！"
    elif msg == "巴哈姆特":
        bot_reply = "巴哈姆特網址為：https://www.gamer.com.tw/index2.php"
    elif "笑話" in msg:
        multi_line = 1 # multiple lines reply
        joke = random.randint(1,3)
        if joke == 1:
            bot_reply = "想聽笑話嗎？我就來講一個吧：\n第一個知道牛奶可以喝的傢伙，你到底對牛做了什麼。"
            s_pid = 1
            s_id = 10
        elif joke == 2:
            bot_reply = "想聽笑話嗎？這個我覺得超好笑：\n如果白癡會飛，那我的公司簡直是個機場。"
            s_pid = 1
            s_id = 16
        elif joke == 3:
            bot_reply = "想聽笑話嗎？不要笑得太大力喔：\n我想，只要我再稍微具有一些謙虛的品質，我就是個完美的人了。"
            s_pid = 1
            s_id = 110

    if multi_line == 1:
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=bot_reply),StickerSendMessage(package_id=str(s_pid),sticker_id=str(s_id))])
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=bot_reply))

if __name__ == "__main__":
    app.run()
    