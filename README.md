# Menu Analyzer (OCR + LLM with OpenRouter)

This Streamlit-based application allows users to upload images of multilingual restaurant menus, extract dish names using Tesseract OCR, and generate detailed information about each dish using large language models via the OpenRouter API.

---

## Features

- Upload menu images in JPG, PNG, or JPEG format
- Extract text from image using Tesseract OCR
- Multilingual OCR support (English, Hindi, Marathi)
- Identify dish names from raw OCR text using OpenRouter LLM
- Display structured details for a selected dish:
  - Description
  - Ingredients
  - Nutrition facts (Calories, Protein, Fat, Carbs)
  - Dish image (fetched from the internet or fallback)

---

## Tech Stack

- Python 3.9+
- Streamlit
- Tesseract OCR
- OpenRouter API (LLM)
- Pillow (PIL)
- `python-dotenv` for environment variables
- Regex, JSON

---

## Project Structure

```bash
menu-analyzer/
├── app.py # Main application code
├── .env # Contains API key (ignored by Git)
├── requirements.txt # Python dependencies
├── .gitignore # Excludes .env and other untracked files
└── README.md # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/menu-analyzer.git
cd menu-analyzer
```

### 2. Set Up Virtual Environment

```
bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate          # On Windows
```

### 3. Install Dependencies

```
bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
**Ubuntu/Debian**

```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-hin tesseract-ocr-mar
```


**macOS (with Homebrew)**

```bash
brew install tesseract
```

**Windows**

Download and install from:
https://github.com/tesseract-ocr/tesseract

Ensure the installation path is correct in your script:

```python
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
```

Update the path if it differs on your system.

### 5. Set Your API Key
Create a .env file in the root directory with the following content:

```
ini
OPENROUTER_API_KEY=your_openrouter_key_here
```

Your `.env` file is automatically excluded from Git via `.gitignore`.


### 6. Run the App

```
bash
streamlit run app.py
```

### Example Output

**Input:**
Image of a multilingual menu containing dishes in English, Hindi, or Marathi.

**Extracted Dishes**

```
json

["Paneer Butter Masala", "Chicken Biryani", "Tandoori Roti"]
```


**Dish Details**


```
json
{
  "description": "A popular North Indian curry made with soft paneer cubes in a creamy tomato-based sauce.",
  "image_url": "https://example.com/paneer.jpg",
  "ingredients": ["paneer", "tomatoes", "butter", "cream", "spices"],
  "nutrition": {
    "calories": "380 kcal",
    "protein": "18 g",
    "fat": "28 g",
    "carbs": "15 g"
  }
}
```

### Future Scope

- Export dish reports or menu to PDF

- Manual correction/editing of OCR output before LLM parsing

- Integration with nutrition databases (e.g., USDA, FatSecret)

- LLM fine-tuning or migration to open-weight local models

- Support for handwritten or low-quality menu images with preprocessing

- Option to display dish details in additional Indian languages

- Admin dashboard for monitoring and managing extracted dish insights

- Smart menu scanning using QR codes

- Mobile-friendly version or companion app


### License

This project is open-source and intended for personal, academic, and research use only.
For commercial use, please contact the project maintainer for permission.