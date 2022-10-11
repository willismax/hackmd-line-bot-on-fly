from PyHackMD import API
import pyimgur
import datetime
from config import (
    HACKMD_API_TOKEN, TODO_NOTE_ID, TEMP_NOTE_ID, IMGUR_CLIENT_ID
) 


def creat_fletting_note(message):
    api = API(HACKMD_API_TOKEN)
    data = api.create_note(
        content = f"# fleeting note: {message.split()[0]}\n\n  ###### tags:`fleeting`\n\n {message}")
    link = f"https://hackmd.io/{data['id']}"
    return link

def update_todo_note(content):
    api = API(HACKMD_API_TOKEN)
    note = api.get_note(note_id = TODO_NOTE_ID)
    ori_content = note['content']
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime("%a, %b %d, %Y %I:%M %p")
    update_content = f"{ori_content}\n- [ ] {content} [time={now}]"
    api.update_note(
        note_id = TODO_NOTE_ID,
        content = update_content
        )
    return f"Added to TODO Notes: \n{content}\n {note['publishLink']}"

def get_user_image(image_content):
    path = './static/temp.png'
    with open(path, 'wb') as fd:
        for chunk in image_content.iter_content():
            fd.write(chunk)
    return path

def upload_img_link(imgpath):
	im = pyimgur.Imgur(IMGUR_CLIENT_ID)
	upload_image = im.upload_image(imgpath, title="Uploaded with PyImgur")
	return upload_image.link

def add_temp_note(content):
    api = API(HACKMD_API_TOKEN)
    note_id = TEMP_NOTE_ID
    note = api.get_note(note_id = note_id)
    ori_content = note['content']
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8))).strftime("%a, %b %d, %Y %I:%M %p")
    update_content = f"{ori_content}\n---\n- {content} [time={now}]"
    api.update_note(
        note_id = TEMP_NOTE_ID,
        content = update_content
        )
    return f"Added to Temporary Notes: \n{content}\n {note['publishLink']}"