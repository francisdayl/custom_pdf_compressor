from flask import Flask, render_template, request, send_file

from pypdf import PdfReader, PdfWriter
from io import BytesIO

from utils.pdf_utils import send_to_compress

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/compress-pdf", methods=["GET", "POST"])
def compress_pdf():
    if request.method == "POST":
        print("POST")
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        print(file.__dir__())
        print(file)
        if file:
            compression_type = request.form.get("compression_type", "Light")
            expected_size = (
                float(request.form.get("customSize")) * 10**6
                if request.form.get("customSize")
                else 2_000_000
            )
            file_name = file.filename
            buffer: BytesIO = send_to_compress(
                file_stream=file.stream,
                compression_type=compression_type,
                expected_size=expected_size,
            )
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{file_name[:-4]}_compressed.pdf",
            )
    return render_template("compress.html")


@app.route("/merge-pdf", methods=["GET", "POST"])
def merge_pdf():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        if file:
            compression_type = request.form.get("compression_type", "Light")
            expected_size = (
                float(request.form.get("customSize")) * 10**6
                if request.form.get("customSize")
                else 2_000_000
            )
            file_name = file.filename
            buffer: BytesIO = send_to_compress(
                file_stream=file.stream,
                compression_type=compression_type,
                expected_size=expected_size,
            )
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{file_name[:-4]}_compressed.pdf",
            )
    return render_template("merge.html")


@app.route("/extract-pdf", methods=["GET", "POST"])
def extract_pdf():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        if file:
            compression_type = request.form.get("compression_type", "Light")
            expected_size = (
                float(request.form.get("customSize")) * 10**6
                if request.form.get("customSize")
                else 2_000_000
            )
            file_name = file.filename
            buffer: BytesIO = send_to_compress(
                file_stream=file.stream,
                compression_type=compression_type,
                expected_size=expected_size,
            )
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{file_name[:-4]}_compressed.pdf",
            )
    return render_template("extract.html")


@app.route("/convert-pdf-jpg", methods=["GET", "POST"])
def convert_pdf_to_jpg():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        if file:
            compression_type = request.form.get("compression_type", "Light")
            expected_size = (
                float(request.form.get("customSize")) * 10**6
                if request.form.get("customSize")
                else 2_000_000
            )
            file_name = file.filename
            buffer: BytesIO = send_to_compress(
                file_stream=file.stream,
                compression_type=compression_type,
                expected_size=expected_size,
            )
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{file_name[:-4]}_compressed.pdf",
            )
    return render_template("pdf_to_jpg.html")


@app.route("/convert-jpg-pdf", methods=["GET", "POST"])
def convert_jpg_to_pdf():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400
        if file:
            compression_type = request.form.get("compression_type", "Light")
            expected_size = (
                float(request.form.get("customSize")) * 10**6
                if request.form.get("customSize")
                else 2_000_000
            )
            file_name = file.filename
            buffer: BytesIO = send_to_compress(
                file_stream=file.stream,
                compression_type=compression_type,
                expected_size=expected_size,
            )
            buffer.seek(0)
            return send_file(
                buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{file_name[:-4]}_compressed.pdf",
            )
    return render_template("jpg_to_pdf.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
