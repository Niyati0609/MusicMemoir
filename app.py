from dotenv import load_dotenv
import os
load_dotenv()

import google.generativeai as genai
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, render_template,request ,redirect,url_for

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

gemini_api_key=os.getenv("gemini_api_key")
genai.configure(api_key="gemini_api_key")
model= genai.GenerativeModel("gemini-2.5-flash")
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    journal = request.form["journal"]
    title = request.form["title"]
    response = model.generate_content(

        f"""
        Read this journal: {journal}
        return your answer in exactly this format:

        REFLECTION:<short warm reflection>
        EMOTION: emotion1, emotion2, emotion3, emotion4, emotion5
        SONGS <3 hindi 3 english>:
        Song Name | Artist | Year the song was released
        Song Name | Artist | Year the song was released
        Song Name | Artist | Year the song was released
        Song Name | Artist | Year the song was released
        Song Name | Artist | Year the song was released
        Song Name | Artist | Year the song was released

    Put each song on a new line.
    """
    )

    result = response.text
    reflection = result.split("EMOTION:")[0]
    reflection = reflection.replace("REFLECTION:", "").strip()
    songs_text = result.split("SONGS <3 hindi 3 english>:")[1]
    song_lines = songs_text.strip().split("\n")
    song1 = song_lines[0]
    song1_parts = song1.split("|")
    
    song1_name = song1_parts[0].strip()
    song1_artist = song1_parts[1].strip()
    song1_year = song1_parts[2].strip()
    cover1, link1 = song(song1_name, song1_artist, token)
    
    song2 = song_lines[1]
    song2_parts = song2.split("|")
    song2_name = song2_parts[0].strip()
    song2_artist = song2_parts[1].strip()
    song2_year = song2_parts[2].strip()
    cover2 , link2 = song(song2_name, song2_artist, token)
    song3 = song_lines[2]
    song3_parts = song3.split("|")
    song3_name = song3_parts[0].strip()
    song3_artist = song3_parts[1].strip()
    song3_year = song3_parts[2].strip()
    cover3,link3 = song(song3_name, song3_artist, token)
    song4 = song_lines[3]
    song4_parts = song4.split("|")
    song4_name = song4_parts[0].strip()
    song4_artist = song4_parts[1].strip()
    song4_year = song4_parts[2].strip()
    cover4,link4 = song(song4_name, song4_artist, token)
    song5 = song_lines[4]
    song5_parts = song5.split("|")
    song5_name = song5_parts[0].strip()
    song5_artist = song5_parts[1].strip()
    song5_year = song5_parts[2].strip()
    cover5,link5 = song(song5_name, song5_artist, token)
    song6 = song_lines[5]
    song6_parts = song6.split("|")
    song6_name = song6_parts[0].strip()
    song6_artist = song6_parts[1].strip()
    song6_year = song6_parts[2].strip()
    cover6,link6  = song(song6_name, song6_artist, token)

    emotion = result.split("SONGS <3 hindi 3 english>:")[0]
    emotion = emotion.replace("EMOTION:", "").strip()

    color = "blue"
    if "Happy" or "Satisfied"in emotion:
        color = "yellow"

    elif "Accomplished" in emotion:
        color = "blue"

    elif "Peaceful" in emotion:
        color = "green"

    elif "Sadness" in emotion:
        color = "purple"

    elif "Nostalgia" in emotion:
        color = "pink"

    elif "Mixed" in emotion:
        color = "orange"
    elif "Angry" in emotion:
        color = "red"
    else:
        color = "red"

    now = datetime.datetime.now()
    date = now.strftime("%d,%B,%Y")
    with open("memories.json","r") as file:

        memories=json.load(file)
        
        memory = {
            "date":date,
            "title":title,
            "journal":journal,
            "reflection":reflection,
            "songs":songs_text,
            "emotion":emotion,
            "color":color
        }
        memories.append(memory)
    with open("memories.json","w") as file:
        json.dump(memories,file,indent=4)

    print(emotion)
    return render_template(
        "results.html",
        color = color,
        emotion = emotion,
        result=result,
        title=title,
        reflection=reflection,
        song1=song1,
        song2=song2,
        song3=song3,
        song4=song4,
        song5=song5,
        song6=song6,
        
        song1_name=song1_name,
        song1_artist=song1_artist,
        song1_year=song1_year,
        cover1=cover1,
        link1=link1,
        
        song2_name=song2_name,
        song2_artist=song2_artist,
        song2_year=song2_year,
        cover2=cover2,
        link2=link2,

        song3_name=song3_name,
        song3_artist=song3_artist,
        song3_year=song3_year,
        cover3=cover3,
        link3=link3,

        song4_name=song4_name,
        song4_artist=song4_artist,
        song4_year=song4_year,
        cover4= cover4,
        link4=link4,

        song5_name=song5_name,
        song5_artist=song5_artist,
        song5_year=song5_year,
        cover5=cover5,
        link5=link5,

        song6_name=song6_name,
        song6_artist=song6_artist,
        song6_year=song6_year,
        cover6=cover6,
        link6=link6
    )

@app.route("/archive")
def archive():
    with open("memories.json","r") as file:
        memories= json.load(file)

    return render_template(
        "archive.html",
        memories = memories
        )

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/memory/<int:index>")
def memory(index):
    with open("memories.json","r") as file:
        memories = json.load(file)
        mem = memories[index]

    tracks = mem["songs"].split("\n")[1:]
    
    return render_template(
        "memory.html",
        mem=mem,
        tracks=tracks
    )


def get_access_token():
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "client_credentials"
        },
        auth=HTTPBasicAuth(
        CLIENT_ID,
        CLIENT_SECRET
        )
) 

    print(response.status_code)
    data = response.json()
    token = data["access_token"]
    
    return token

def song(song,artist,token):
    response=requests.get(
        "https://api.spotify.com/v1/search",
        headers={
    "Authorization": f"Bearer {token}"
    },
    params={
    "q": f"{song} {artist}",
    "type": "track",
    "limit": 1
    }
)
    data = response.json()
    cover = data["tracks"]["items"][0]["album"]["images"][0]["url"]
    link = data["tracks"]["items"][0]["external_urls"]["spotify"]
    return cover,link

@app.route("/delete/<int:index>")
def delete(index):
    with open("memories.json") as file:
        memories = json.load(file)
        memories.pop(index)

    with open("memories.json","w") as file:
        json.dump(memories,file,indent=4)

    return redirect("/archive")


if __name__ == "__main__":
    token = get_access_token()
    cover=song("fix you","coldplay", token)
    print(cover)
    app.run(debug=True)