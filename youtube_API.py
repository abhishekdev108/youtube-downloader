from flask import Flask, request, jsonify, send_file
from flask_restful import Resource,Api
from pytube import YouTube
from youtube_search import YoutubeSearch
from io import BytesIO
app = Flask(__name__)
api = Api(app)

class YoutubeSeach(Resource):
    def get(self):
        welcomeNote = {
            "name":"Welcome note",
            "message": "Hello welcome to my appliction. please type what is in your mind in search box."
        }
        return jsonify(welcomeNote)
    def post(self):
        search_term = request.get_json()
        if search_term is None:
            return {"message":"please paas a valid term"}
        else:
            youtubeApp = YoutubeSearch(search_term["term"],max_results=2).to_dict()
            return jsonify({"videos":youtubeApp})


class YoutubeDownload(Resource):
    def get(self):
        buffer = BytesIO()
        video = YouTube("https://www.youtube.com/watch?v=ixCnsZswdpU")
        streams = video.streams.filter(only_audio=True).get_by_itag(140)
        streams.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer , as_attachment=True,download_name="aayehomerijindgime.mp3",mimetype="audio/mp4")

    def post(self):
        data = request.get_json()
        title = data['title']
        buffer = BytesIO()
        try:
            chunk =1024
            video = YouTube(data['url'])
            streams = video.streams.filter(only_audio=True).get_by_itag(140)
            streams.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=title, mimetype="audio/mp4")
        except :
            return "you enter a wrong url or value.." ,401







api.add_resource(YoutubeSeach,'/')
api.add_resource(YoutubeDownload,"/download")
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

