import os
import urllib.request
from PIL import Image
from rembg import remove, new_session

BASE = "https://preview.free3d.com/img/2016/12/1750915414256256930/"
NAMES = [
    "9wmszw80", "vwymxx4x", "nfgdxabs", "zl5t41oy",
    "zsqn9fxd", "xeb2npjq", "o8cluscn", "zwlhs116",
]
SRC = os.path.join(os.path.dirname(__file__), "..", "_src_house")
DST = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "house")

os.makedirs(SRC, exist_ok=True)
os.makedirs(DST, exist_ok=True)

session = new_session("u2net")

for i, name in enumerate(NAMES, start=1):
    src_path = os.path.join(SRC, name + ".jpg")
    if not os.path.exists(src_path):
        print(f"[{i}/8] descargando {name}...")
        try:
            urllib.request.urlretrieve(BASE + name + ".jpg", src_path)
        except Exception as e:
            print(f"  error descarga {name}: {e}")
            continue

    print(f"[{i}/8] quitando fondo a {name}...")
    with open(src_path, "rb") as f:
        input_data = f.read()
    try:
        output = remove(input_data, session=session)
        out_path = os.path.join(DST, f"casa{i}.png")
        with open(out_path, "wb") as f:
            f.write(output)
        print(f"  -> guardado {os.path.relpath(out_path)}")
    except Exception as e:
        print(f"  error rembg {name}: {e}")

print("Listo.")
