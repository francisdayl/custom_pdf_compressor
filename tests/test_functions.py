import responses

test_filename = "pdf_test.pdf"
file_test = open(test_filename, "rb")


def test_home(client):
    response = client.get("/")
    assert b"COMPRESS PDF" in response.data
    assert b"MERGE PDF" in response.data
    assert b"EXTRACT PDF" in response.data


def test_compress_pdf_file(client):
    response = client.get("/compress-pdf")
    assert response.status_code == 200
    assert b"uploadForm" in response.data
    assert b"compression_type" in response.data
    context = {"file": file_test, "content_type": "multipart/form-data"}
    response = client.post("/compress-pdf", data=context)
    assert response.status_code == 200


def test_compress_not_working_without_file(client):
    response = client.post("/compress-pdf")
    assert response.status_code == 400


def test_extract(client):
    response = client.get("/extract-pdf")
    assert response.status_code == 200
    assert b"fileInputWraper" in response.data
    assert b"Generate PDF" in response.data
    test_filename = "pdf_test.pdf"
    file_test = open(test_filename, "rb")
    context = {"file": file_test, "valid_pages": "1"}
    response = client.post("/extract-pdf", data=context)
    assert response.status_code == 200


def test_extract_fails_without_file(client):
    response = client.post("/extract-pdf")
    assert response.status_code == 400


def test_convert_to_images(client):
    response = client.get("/convert-pdf-jpg")
    assert response.status_code == 200
    assert b"uploadForm" in response.data
    assert b"Convert to JPG" in response.data
    test_filename = "pdf_test.pdf"
    file_test = open(test_filename, "rb")
    context = {"file": file_test}
    response = client.post("/convert-pdf-jpg", data=context)
    assert response.status_code == 200


def test_convert_to_images_fails_without_file(client):
    response = client.post("/convert-pdf-jpg")
    assert response.status_code == 400


def test_unexistent_route(client):
    response = client.get("/whatamidoing")
    assert (
        b"Sorry but we couldn't handle your request. Please try again :("
        in response.data
    )
