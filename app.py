from flask import Flask, render_template, request, send_file
import os
from converters.pdf_to_ppt import pdf_to_ppt

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return "No file selected"

        if not file.filename.endswith(".pdf"):
            return "Only PDF files are supported"

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "converted.pptx")

        file.save(input_path)
        pdf_to_ppt(input_path, output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
