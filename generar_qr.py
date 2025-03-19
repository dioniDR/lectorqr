import segno
from PIL import Image
import os

# 📌 Ruta de la plantilla del diseño
TEMPLATE_PATH = "qrimages/template/image.png"

# 🔹 Verificar si la plantilla existe antes de ejecutar
if not os.path.exists(TEMPLATE_PATH):
    abs_path = os.path.abspath(TEMPLATE_PATH)
    raise FileNotFoundError(f"❌ Error: No se encontró la plantilla en {TEMPLATE_PATH}\nRuta absoluta: {abs_path}")

# 1️⃣ Definir productos y sus categorías
productos = {
    "001": "electronicos",
    "002": "electronicos",
    "003": "ropa",
    "004": "ropa",
    "005": "hogar",
    "006": "hogar",
    "007": "deportes",
    "008": "deportes",
    "009": "accesorios",
    "010": "accesorios",
}

# 2️⃣ Crear la carpeta base para guardar los QR
base_dir = "qrimages"
os.makedirs(base_dir, exist_ok=True)

# 3️⃣ Generar QR y fusionarlos con la imagen de fondo
for product_id, categoria in productos.items():
    folder_path = os.path.join(base_dir, categoria)
    os.makedirs(folder_path, exist_ok=True)

    qr_final_path = os.path.join(folder_path, f"qr_{product_id}.png")
    temp_qr_path = f"temp_qr_{product_id}.png"  # Archivo temporal

    # 🔹 Generar QR y guardarlo como imagen temporal
    qr = segno.make_qr(product_id, error="H")
    qr.save(temp_qr_path, scale=10)  # ✅ Usa save() en lugar de to_pil()

    # 🔹 Cargar el QR como imagen con PIL
    qr_img = Image.open(temp_qr_path).convert("RGBA")
    qr_size = qr_img.size[0]

    # 🔹 Cargar la plantilla de diseño
    fondo = Image.open(TEMPLATE_PATH).convert("RGBA")

    # 🔹 Definir la posición del QR en la plantilla (centrado)
    pos_x = (fondo.size[0] - qr_size) // 2
    pos_y = (fondo.size[1] - qr_size) // 2

    # 🔹 Pegar el QR en la plantilla
    fondo.paste(qr_img, (pos_x, pos_y), qr_img)

    # 🔹 Guardar la imagen final con el QR sobre la plantilla
    fondo.save(qr_final_path)

    # 🔹 Eliminar el archivo temporal
    os.remove(temp_qr_path)

    print(f"✅ QR con diseño generado: {qr_final_path}")

print("\n📂 Todos los códigos QR con diseño han sido creados y organizados por categoría.")
