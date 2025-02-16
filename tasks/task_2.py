"""Module providing a function for file validating"""

import json
from tasks.task_1 import PDFExtractor

def validate_structure(reference_structure, test_structure):
    errors = []

    ref_text = {
        (item["text"], item["page"]) for item in reference_structure["text_structure"]
    }
    test_text = {
        (item["text"], item["page"]) for item in test_structure["text_structure"]
    }

    missing_text = ref_text - test_text
    if missing_text:
        errors.append(f"The text element is missing: {missing_text}")

    for key, ref_value in reference_structure["metadata"].items():
        test_value = test_structure["metadata"].get(key)
        if test_value != ref_value:
            errors.append(
                f"Metadata discrepancies: {key} (expected '{ref_value}', got '{test_value}')"
            )

    ref_barcodes = {(b["data"], b["page"]) for b in reference_structure["barcodes"]}
    test_barcodes = {(b["data"], b["page"]) for b in test_structure["barcodes"]}

    missing_barcodes = ref_barcodes - test_barcodes
    if missing_barcodes:
        errors.append(f"Missing barcodes: {missing_barcodes}")

    # допустимая разница ±5 px
    for ref_word in reference_structure["text_structure"]:
        matched = False
        for test_word in test_structure["text_structure"]:
            if (
                ref_word["text"] == test_word["text"]
                and ref_word["page"] == test_word["page"]
            ):
                x_diff = abs(ref_word["x0"] - test_word["x0"])
                y_diff = abs(ref_word["y0"] - test_word["y0"])
                if x_diff <= 5 and y_diff <= 5:
                    matched = True
                    break
        if not matched:
            errors.append(
                f"The text layout is violated: '{ref_word['text']}' (page {ref_word['page']})"
            )

    return errors

# --------------------------------------------------------------------------------
def main():
    reference_pdf = PDFExtractor(
        "data/test_task.pdf"
    )  # Для ручного запуска указать путь к файлу
    reference_structure = reference_pdf.extract_all()

    with open("reference_structure.json", "w", encoding="utf-8") as f:
        json.dump(reference_structure, f, indent=4)

    test_files = [
        "data/test_pdf_1.pdf",
        "data/test_pdf_2.pdf",
    ]  # Для ручного запуска указать путь к файлам

    for file in test_files:
        print(f"\nFile checking {file}")
        test_pdf = PDFExtractor(file)
        test_structure = test_pdf.extract_all()

        errors = validate_structure(reference_structure, test_structure)

        if errors:
            print("Discrepancies found:")
            for err in errors:
                print(f"  - {err}")
        else:
            print("File is fully match to the refference")
        print("-" * 60)


if __name__ == "__main__":
    main()
