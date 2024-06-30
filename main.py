from pypdf import PdfReader, PdfWriter
from io import BytesIO

MINIMUM_FILE_SIZE = 1_900_000


def _compress_pdf(file_name: str, quality_decrease: int) -> BytesIO:

    reader = PdfReader(file_name)
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


def send_to_compress(file_name: str, compression_type: str, expected_size: int):
    buffer = BytesIO()
    quality_decrease_by_type = {"Light": 80, "Medium": 60, "Extreme": 40}
    if compression_type == "Custom":
        current_decrease = 80
        buffer = _compress_pdf(file_name=file_name, quality_decrease=current_decrease)
        buffer_size = buffer.tell()
        print(buffer_size, current_decrease)
        while (current_decrease > 20 and buffer_size > expected_size and buffer_size > MINIMUM_FILE_SIZE):
            current_decrease -= 20
            buffer = _compress_pdf(file_name=file_name, quality_decrease=current_decrease)
            buffer_size = buffer.tell()
            print(buffer_size, current_decrease)

    else:
        buffer = _compress_pdf(
            file_name=file_name,
            quality_decrease=quality_decrease_by_type[compression_type],
        )

    with open(f"{file_name[:-4]}_compressed.pdf", "wb") as file:
        file.write(buffer.getvalue())
        file.close()
    buffer.close()


send_to_compress(
    file_name="prueba.pdf", compression_type="Custom", expected_size=2_000_000
)
