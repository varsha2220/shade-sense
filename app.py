from flask import Flask, render_template, request
import os
import cv2
import numpy as np
import base64
import json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load products
with open("data/products.json") as f:
    products = json.load(f)

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ---------------- HEX DISTANCE ----------------
def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))

# ---------------- CATEGORY MATCH ----------------
def match_category(product_name, selected_category):
    name = product_name.lower()

    keywords = {
        "foundation": ["foundation", "fou"],
        "concealer": ["concealer", "con"],
        "blush": ["blush", "blu"],
        "compact": ["compact", "pow", "com"],
        "lipstick": ["lipstick", "lip"]
    }

    if selected_category == "all":
        return True

    for word in keywords.get(selected_category, []):
        if word in name:
            return True

    return False

# ---------------- RECOMMENDATION ENGINE ----------------
def recommend_products(user_hex, tone, undertone, category="all"):

    def hex_to_rgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def color_distance(c1, c2):
        return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5

    user_rgb = hex_to_rgb(user_hex)

    # ✅ CATEGORY KEYWORDS (IMPORTANT)
    categories = {
        "foundation": ["foundation"],
        "concealer": ["concealer"],
        "blush": ["blush"],
        "compact": ["compact", "powder"],
        "lipstick": ["lipstick"]
    }

    final_output = {}

    for cat, keywords in categories.items():

        # ✅ FILTER ONLY SELECTED CATEGORY
        if category.lower() != "all" and cat != category.lower():
            continue

        scored = []

        for item in products:

            # ✅ CATEGORY MATCH USING PRODUCT NAME (NO JSON CATEGORY NEEDED)
            name = (item.get("product", "") + " " + item.get("shade", "")).lower()

            if not any(k in name for k in keywords):
                continue

            try:
                product_rgb = hex_to_rgb(item["hex"])
            except:
                continue

            dist = color_distance(user_rgb, product_rgb)

            # penalties
            tone_penalty = 0 if tone.lower() in item.get("shade", "").lower() else 10
            undertone_penalty = 0 if undertone.lower() in item.get("shade", "").lower() else 5

            total_score = (dist * 0.7) + (tone_penalty * 2) + (undertone_penalty * 1.5)

            confidence = max(0, 100 - (total_score / 441) * 100)
            item["score"] = round(confidence, 1)

            scored.append((total_score, item))

        # ✅ SORT BEST MATCHES
        scored.sort(key=lambda x: x[0])

        # ✅ TAKE TOP 5 PRODUCTS
        # decide number of products
        limit = 5 if category.lower() != "all" else 2

        final_output[cat] = [item for _, item in scored[:limit]]
        

    return final_output






    


# ---------------- IMAGE PROCESS ----------------

    if r > g and r > b:
        undertone = "Warm"
    elif b > r:
        undertone = "Cool"
    else:
        undertone = "Neutral"
        return hex_value, tone, undertone
    





def process_image(filepath):

    image = cv2.imread(filepath)

    # ---------------- FACE DETECTION ----------------
    
   # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]

        face = image[y:y+h, x:x+w]

        # ---------------- CENTER CHEEK CROP ----------------
        h, w, _ = face.shape
        face = face[int(h*0.3):int(h*0.7),
                    int(w*0.3):int(w*0.7)]
    else:
        face = image  # fallback

    # ---------------- SMOOTHING ----------------
    face = cv2.GaussianBlur(face, (5,5), 0)

    # ---------------- SKIN DETECTION (YCrCb) ----------------
    ycrcb = cv2.cvtColor(face, cv2.COLOR_BGR2YCrCb)

    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)

    mask = cv2.inRange(ycrcb, lower, upper)

    skin = cv2.bitwise_and(face, face, mask=mask)

    # ---------------- EXTRACT VALID PIXELS ----------------
    pixels = skin.reshape(-1, 3)

    # remove black pixels
    pixels = [p for p in pixels if not (p == [0,0,0]).all()]

    # remove extreme brightness/darkness
    pixels = [p for p in pixels if sum(p)/3 > 40 and sum(p)/3 < 220]

    # fallback if no pixels
    if len(pixels) == 0:
        pixels = face.reshape(-1, 3)

    pixels = np.array(pixels)

    # ---------------- AVERAGE COLOR ----------------
    avg_color = np.mean(pixels, axis=0)

    b, g, r = avg_color

    # ---------------- FORCE SKIN TONE ----------------
    # boost red, reduce blue
    r = min(255, r * 1.1)
    g = min(255, g * 1.0)
    b = min(255, b * 0.9)

    # avoid blue/gray tone
    if b > r:
        b = r * 0.8

    # ---------------- HEX ----------------
    hex_value = "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

    # ---------------- TONE ----------------
    brightness = (r + g + b) / 3

    if brightness > 180:
        tone = "Very Light"
    elif brightness > 140:
        tone = "Light"
    elif brightness > 100:
        tone = "Medium"
    else:
        tone = "Dark"

    # ---------------- UNDERTONE ----------------
    if r > g and r > b:
        undertone = "Warm"
    elif b > r:
        undertone = "Cool"
    else:
        undertone = "Neutral"

    return hex_value, tone, undertone

















   

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["image"]
    category = request.form.get("category","all")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    hex_value, tone, undertone = process_image(filepath)

    recommendations = recommend_products(
        hex_value, tone, undertone,category
    )

    return render_template(
        "result.html",
        data=recommendations,
        hex_value=hex_value,
        tone=tone,
        undertone=undertone
    )

@app.route("/upload_camera", methods=["POST"])
def upload_camera():

    image_data = request.form.get("image_data")
    if not image_data:
      return "No image data received", 400
    category = request.form.get("category","all")

    image_data = image_data.split(",")[1]
    img_bytes = base64.b64decode(image_data)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], "captured.png")

    with open(filepath, "wb") as f:
        f.write(img_bytes)

    hex_value, tone, undertone = process_image(filepath)

    recommendations = recommend_products(
        hex_value, tone, undertone,category
    )

    return render_template(
        "result.html",
        data=recommendations,
        hex_value=hex_value,
        tone=tone,
        undertone=undertone
    )


@app.route("/get_brands/<category>")
def get_brands(category):

    brands = set()

    for item in products:
        name = item.get("product", "").lower()
        brand = item.get("brand", "")

        if category in name:
            brands.add(brand)

    return {"brands": list(brands)}

if __name__ == "__main__":
    app.run(debug=True)