from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import hackmd_bot.hackmd_bot as hb

from config import (
    CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, LINE_USER_ID
) 

import os

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text='你可以開始了'))




# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word =  str(event.message.text)
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'
    if word[:6] == "@fleet":
        content = hb.creat_fletting_note(word[6:])
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if word[:5] == "@todo":
        content = hb.update_todo_note(word[5:])
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    else: 
        content = hb.add_temp_note(word)
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)