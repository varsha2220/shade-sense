
# 💄 Shade Sense

Shade Sense is an AI-powered web application that analyzes a user's skin tone from an uploaded image or live camera capture and recommends suitable makeup products. It uses computer vision techniques to detect facial skin color, identify the user's skin tone and undertone, and suggest matching products from a curated makeup database.

## ✨ Features

- 📸 Upload an image or capture one using the webcam
- 💡 Real-time lighting quality detection before image capture
- 😊 Automatic face detection using OpenCV Haar Cascade
- 🎨 Detects skin tone, undertone, and HEX color
- 💄 Personalized makeup recommendations
- 🏷️ Filter recommendations by category
  - Foundation
  - Concealer
  - Blush
  - Compact
  - Lipstick
- 🏢 View available brands for each product category
- 📱 Clean, responsive, and user-friendly interface

## 🛠️ Tech Stack

- Python
- Flask
- OpenCV
- NumPy
- HTML
- CSS
- JavaScript
- JSON

## 📂 Project Structure

```
shade-sense/
│── app.py
│── requirements.txt
│── README.md
│── data/
│   └── products.json
│── templates/
│   ├── upload.html
│   └── result.html
│── static/
│   └── images/
│── uploads/
│── haarcascade_frontalface_default.xml
│── generate_dataset.py
│── extract_dataset.py
│── train_model.py
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/varsha2220/shade-sense.git
```

Go to the project folder:

```bash
cd shade-sense
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## 📊 Workflow

1. Upload an image or capture one using the webcam.
2. The system checks lighting conditions.
3. OpenCV detects the face region.
4. Skin color is extracted from the detected face.
5. Skin tone, undertone, and HEX color are calculated.
6. Matching makeup products are recommended.
7. Results are displayed with brand, product name, shade, and match percentage.

## 📌 Future Improvements

- Deep Learning based skin tone detection
- Better lighting normalization
- Expanded makeup product database
- User authentication
- Save favorite recommendations
- Mobile application support
- Cloud deployment

## 👩‍💻 Author

**Shree Varsha Chary**

GitHub: https://github.com/varsha2220

---

⭐ If you found this project useful, consider giving it a star on GitHub!