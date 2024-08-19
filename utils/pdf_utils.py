import io
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

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


def extract_pdf_file(file_stream, valid_pages: list[str]) -> BytesIO:
    reader = PdfReader(file_stream)
    writer = PdfWriter()
    for valid_page in valid_pages:
        writer.add_page(reader.get_page(int(valid_page) - 1))

    buffer = BytesIO()
    writer.write(buffer)
    return buffer


def convert_pdf_file_to_jpgs(file_stream, valid_pages: list[str]) -> BytesIO:
    reader = PdfReader(file_stream)
    writer = PdfWriter()
    for valid_page in valid_pages:
        writer.add_page(reader.get_page(int(valid_page) - 1))

    buffer = BytesIO()
    writer.write(buffer)
    return buffer


def convert_jpgs_to_pdf(image_files, valid_pages: list[str]) -> BytesIO:
    images = []
    for file in image_files:
        img = Image.open(file)
        img = img.convert("RGB")
        images.append(img)

    pdf_bytes = io.BytesIO()
    if images:
        images[0].save(pdf_bytes, save_all=True, append_images=images[1:], format="PDF")
    return pdf_bytes
