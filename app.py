from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError

from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage
)
import hackmd_bot.hackmd_bot as hb

from config import (
    CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, LINE_USER_ID
) 

import os

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Messages on start and restart
line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text='Chat BOT Startup'))

# Listen for all Post Requests from /callback
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


@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    """LINE MessageAPI message processing"""
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'

    if event.message.type=='image':
        image = line_bot_api.get_message_content(event.message.id)
        path = hb.get_user_image(image)
        link = hb.upload_img_link(path)
        content = hb.add_temp_note(content = f"![]({link})")
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.type=='text':
        word =  str(event.message.text)
        if word[:3] == "@靈感":
            content = hb.creat_fletting_note(word[3:])
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        elif word[:5] == "@todo":
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
