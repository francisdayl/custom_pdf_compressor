from flask import Flask, render_template, request, send_file

from pypdf import PdfReader, PdfWriter
from io import BytesIO

MINIMUM_FILE_SIZE = 1_900_000


def _compress_pdf(file_stream, quality_decrease: int) -> BytesIO:
    reader = PdfReader(file_stream)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)

    for page in writer.pages:
        for img in page.images:
            img.replace(img.image, quality=quality_decrease)
        page.compress_content_streams()
    buffer = BytesIO()
    writer.write(buffer)
    return buffer


def send_to_compress(file_stream, compression_type: str, expected_size: float):
    buffer = BytesIO()
    quality_decrease_by_type = {"Light": 80, "Medium": 60, "Extreme": 40}
    if compression_type == "Custom":
        current_decrease = 80
        buffer = _compress_pdf(
            file_stream=file_stream, quality_decrease=current_decrease
        )
        buffer_size = buffer.tell()
        while (
            current_decrease > 20
            and buffer_size > expected_size
            and buffer_size > MINIMUM_FILE_SIZE
        ):
            current_decrease -= 20
            buffer = _compress_pdf(
                file_stream=file_stream, quality_decrease=current_decrease
            )
            buffer_size = buffer.tell()
    else:
        buffer = _compress_pdf(
            file_stream=file_stream,
            quality_decrease=quality_decrease_by_type[compression_type],
        )
    return buffer


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def upload_file():
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
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5100)
