from utils.pdf_utils import *


test_file = "pdf_test.pdf"

# send_to_compress(test_file, "Light", 10_000_000)#Time: 2.254s, Max Memory: 69M
# send_to_compress(test_file, "Extreme", 10_000_000)  # Time: 2.311s, Max Memory: 77M


extract_pdf_file(test_file, ["3", "1"])  # Time 443ms; Max Memory: 13
