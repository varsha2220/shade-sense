import cv2
import numpy as np
import os

# 📁 folder where your images are stored
folder = "dataset_images"

data = []

for filename in os.listdir(folder):

    path = os.path.join(folder, filename)

    # read image
    image = cv2.imread(path)

    if image is None:
        continue

    # convert BGR → RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert RGB → HSV
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

    h, w, _ = image_rgb.shape

    # 🟢 take center region (approx face area)
    face = image_rgb[
        int(h * 0.3):int(h * 0.7),
        int(w * 0.3):int(w * 0.7)
    ]

    # 🟢 calculate average RGB
   # skin detection ma
    lower = np.array([0, 30, 60])
    upper = np.array([20, 150, 255])

    mask = cv2.inRange(hsv, lower, upper)
    skin = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

    avg_color = np.mean(skin[mask > 0], axis=0)
    r, g, b = avg_color

    # 🟢 brightness formula
    brightness = 0.299 * r + 0.587 * g + 0.114 * b

    # 🟢 V value from HSV
    v = np.mean(hsv[:, :, 2])

    # 🟢 final row (without label)
    row = [int(r), int(g), int(b), int(brightness), int(v)]

    print(filename, "→", row)

    data.append(row)

# 🔥 print all data
print("\nFINAL DATASET:")
for d in data:
    print(d +",")