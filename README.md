# 🛠️ Interactive Guide to Launching the Program

## 📋 Prerequisites

Before running the program, make sure you have:

- Python 3.10+
- pip (Python package manager)
- Git (for working with the repository)

### Installing Dependencies

pip install -r requirements.txt

## 🚀 Running the Program

1. Navigate to the project root:

cd erpaerotasks

2. Run the program:

python main.py

## 🖥️ Interactive Menu

After starting the program, the following interactive menu will appear:

📘 Interactive Menu: 

1️⃣  Extract pdf structure and data as a JSON dictionary

2️⃣  Compare a reference pdf with one or more test pdf's 

3️⃣  Clear data (delete screenshots and JSON files)

4️⃣  Exit the program

👉 Choose an action (1-4):

### 🧩 Menu Options

1️⃣ Extract pdf structure and data as a JSON dictionary    
- Enter the name of the PDF file from the `data/` folder.  
- The program will create a JSON file with the document structure and display it in the console.  

2️⃣ Compare a reference pdf with one or more test pdf's  
- Enter the name of the reference file (from the `data/` folder).  
- Enter the names of the test files separated by commas.  
- The program will verify the structure of the test files against the reference.  

3️⃣ Clear data (delete screenshots and JSON files)
- Deletes temporary files, including page screenshots and the JSON structure file.  

4️⃣ Exit the program  
- Terminates the program.  

## 🛠️ Useful Info

### Running with a Virtual Environment

python -m venv venv  
source venv/Scripts/activate  (Windows)  
source venv/bin/activate      (Linux/MacOS)  

## 📄 Project Structure

├── data  
│   └── example.pdf  
├── tasks  
│   ├── task_1.py  
│   └── task_2.py
│   └── additional_task.py
├── main.py  
├── requirements.txt  
└── README.md  

## ❓ Troubleshooting

1. `ModuleNotFoundError`: Make sure the virtual environment is activated.  
2. `PDF file not found`: Check the file name and ensure it is in the `data/` folder.  
3. Error during barcode scanning: Ensure the `opencv-python` and `pyzbar` libraries are installed.  