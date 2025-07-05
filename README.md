# Menu Analyzer (OCR + LLM with OpenRouter)

This Streamlit-based application allows users to upload images of multilingual restaurant menus, extract dish names using Tesseract OCR, and generate detailed information about each dish using large language models through OpenRouter API.

## Features

- Upload menu images in JPG, PNG, or JPEG format
- Extract text from image using Tesseract OCR
- Multilingual OCR support (English, Hindi, Marathi)
- Identify dish names from raw OCR text using OpenRouter LLM
- Display structured details for a selected dish:
  - Description
  - Ingredients
  - Nutrition facts (Calories, Protein, Fat, Carbs)
  - Dish image (fetched from the internet or a fallback image)

## Tech Stack

- Python 3.9+
- Streamlit
- Tesseract OCR
- OpenRouter API (LLM)
- Pillow (PIL)
- python-dotenv (for environment variables)
- Regex, JSON

## Project Structure

menu-analyzer/
├── app.py # Main application code
├── .env # Contains API key (not pushed to Git)
├── requirements.txt # Python dependencies
├── .gitignore # Excludes .env and other untracked files
└── README.md # Project documentation



## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/menu-analyzer.git
cd menu-analyzer
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate          # On Windows
```

### 3. Install Dependencies

```bash
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

Ensure the executable path is added to the script:


```python

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
```


Update path if different on your system.

### 5. Set Your API Key
Create a .env file in the project root with the following:

```ini

OPENROUTER_API_KEY=your_openrouter_key_here
```

Make sure `.env` is not committed to Git. It's ignored via `.gitignore`.

### 6. Run the App
```bash
streamlit run app.py
```

### Example Output

**Input**
    Image of a multilingual menu containing dishes in English, Hindi, or Marathi.

**Extracted Output**

```json

["Paneer Butter Masala", "Chicken Biryani", "Tandoori Roti"]
```

**Dish Details**

```json

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
    
    - PDF export for menu or dish reports

    - Option to manually correct OCR output before LLM parsing

    - Integration with nutrition databases (e.g., USDA)

    - LLM fine-tuning or switching to local open-weight models

    - Support for handwritten menus or blurred images using image preprocessing

    - Option to view dish data in other Indian languages

    - Admin dashboard for reviewing extracted dish insights

    - QR code scanning for smart menus

    - Mobile app version

### License

This project is intended for personal, academic, and research purposes. Commercial usage is not allowed without permission.

