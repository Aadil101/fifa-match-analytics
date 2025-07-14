from app.core.ocr import res, ocr_engine

def perform_ocr(image_path: str, image_type: str) -> None:
    # Run OCR inference on an image 
    results = ocr_engine.predict(input=image_path)

    # Visualize the results and save the JSON results
    for result in results:
        result.save_to_img("output")
        result.save_to_json("output")
        res[image_type] = result