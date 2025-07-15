from paddleocr import PaddleOCR

# TODO: Remove this, don't want to store state in server
res = {}

# TODO: Make properties configurable
# TODO: This takes a while to load, causing startup of the backend to take a full minute
ocr_engine = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False)
