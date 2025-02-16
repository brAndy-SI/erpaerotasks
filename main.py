"Module providing interactive way to interact with tasks"

import json
import os
import glob
from datetime import datetime

from tasks.task_1 import PDFExtractor
from tasks.task_2 import validate_structure

def extract_pdf_data():
    file_name = input("Enter the PDF filename (from the 'data/' folder): ").strip()
    path = os.path.join("data", file_name)

    try:
        extractor = PDFExtractor(path)
        pdf_info = extractor.extract_all()

        json_output = json.dumps(pdf_info, indent=4, ensure_ascii=False)
        print(json_output)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"{file_name}_structure_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            f.write(json_output)

        print(
            f"\n✅ Pdf structure has been extracted and saved 💾 to file {json_filename}\n"
        )

    except Exception as e:
        print(f"❌ Error extracting PDF data: {e}")

def compare_pdfs():
    while True:
        reference_file = input(
            "Enter the reference file name (from the 'data/' folder): "
        ).strip()
        reference_path = os.path.join("data", reference_file)

        if os.path.exists(reference_path):
            break
        else:
            print(f"❌ File '{reference_path}' not found. Please try again.")

    test_files = []
    while not test_files:
        test_files_input = input(
            "Enter test file names (comma-separated, from 'data/' folder): "
        ).strip()
        test_files = [file.strip() for file in test_files_input.split(",")]

        # Check each test file
        invalid_files = [
            file
            for file in test_files
            if not os.path.exists(os.path.join("data", file))
        ]

        if invalid_files:
            print(f"❌ The following files were not found: {invalid_files}")
            test_files = []

    try:
        ref_extractor = PDFExtractor(reference_path)
        reference_structure = ref_extractor.extract_all()


        for test_file in test_files:
            test_path = os.path.join("data", test_file)
            print(f"\n🧐 Comparing: {test_file}")
            try:
                test_extractor = PDFExtractor(test_path)
                test_structure = test_extractor.extract_all()

                errors = validate_structure(reference_structure, test_structure)

                if errors:
                    print("❌ Discrepancies found:")
                    for err in errors:
                        print(f"  - {err}")
                else:
                    print("✅ File is fully match to the refference")

            except Exception as e:
                print(f"❌ Error during checking the file '{test_file}': {e}")

    except Exception as e:
        print(f"❌ Error during refference file processing: {e}")

def clear_data():
    screenshots = glob.glob("./temp_page_*.png")
    for screenshot in screenshots:
        try:
            os.remove(screenshot)
            print(f"🗑️ The photo deleted: {screenshot}")
        except Exception as e:
            print(f"⚠️  Deleting error {screenshot}: {e}")

    json_files = glob.glob("*.json")
    for json_file in json_files:
        try:
            os.remove(json_file)
            print(f"🗑️ The json file deleted: {json_file}")
        except Exception as e:
            print(f"⚠️  Deleting error {json_file}: {e}")

    print("✅ Cleaning has been completed")

def main():
    """Интерактивное меню управления"""
    while True:
        print("\n📘 Interactive Menu:")
        print("1️⃣  Extract pdf structure and data as a JSON dictionary")
        print("2️⃣  Compare a reference pdf with one or more test pdf's")
        print("3️⃣  Clear data (delete screenshots and JSON files)")
        print("4️⃣  Exit the program")
        choice = input("👉 Choose an action (1-4): ").strip()

        if choice == "1":
            extract_pdf_data()
        elif choice == "2":
            compare_pdfs()
        elif choice == "3":
            clear_data()
        elif choice == "4":
            print("👋 Exit")
            break
        else:
            print("⚠️  Incorrect enter try again")


if __name__ == "__main__":
    main()
