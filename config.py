import os
import json

# ----------------------------
# Configuration
# ----------------------------
MEMORY_FOLDER = "./AutoGen_Memory"
os.makedirs(MEMORY_FOLDER, exist_ok=True)

PRODUCT_FILE = "products.json"

if os.path.exists(PRODUCT_FILE):
    with open(PRODUCT_FILE, "r") as f:
        PRODUCT_DB = json.load(f)
else:
    raise FileNotFoundError(f"{PRODUCT_FILE} not found. Please add product data.")
