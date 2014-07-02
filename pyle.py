# Configuration
STATIC_PATH = "/home/henrik/webdump"

import os
from mimetypes import MimeTypes
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

def listdirectory(requested_path):
    path = os.path.normpath(STATIC_PATH) + requested_path
    dirlist = os.listdir(path)

    dirs = [d for d in dirlist if not os.path.isfile(os.path.join(path, d))]
    files = [f for f in dirlist if f not in dirs]

    return dirs, files

@app.route("/")
def main():
    return "nope."

@app.route("/list/", defaults={"path" : None})
@app.route("/list/<path:path>/")
def listdir(path):
    if path is None:
        path = "/"
    else:
        path = os.path.join("/", path, "")

    dirs, files = listdirectory(path)

    if path != "/":
        dirs.insert(0, "..")

    return render_template("dirlist.html",
            title="pyle :: " + path,
            path=path,
            directories=dirs,
            files=files)


@app.route("/data/<path:file>")
def readfile(file):
    return send_from_directory(STATIC_PATH, file)

@app.route("/<path:file>")
def showfile(file):
    mime = MimeTypes()
    mime_type = mime.guess_type(file)
    if mime_type[0] is not None and mime_type[0].startswith("image"):
        return render_template("image.html",
                title="pyle :: preview",
                filepath="/data/" + file)
    else:
        return readfile(file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
