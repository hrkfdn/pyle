# Configuration
STATIC_PATH = "/home/henrik/webdump"

from mimetypes import MimeTypes
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def main():
    return "nope."

@app.route("/data/<file>")
def readfile(file):
    return send_from_directory(STATIC_PATH, file)

@app.route("/<file>/")
def showfile(file):
    mime = MimeTypes()
    mime_type = mime.guess_type(file)
    if mime_type[0] is not None and mime_type[0].startswith("image"):
        return render_template("image.html",
                title="pyle :: preview",
                filename=file,
                filepath="/data/" + file)
    else:
        return readfile(file)

if __name__ == "__main__":
    app.run(debug=True)
