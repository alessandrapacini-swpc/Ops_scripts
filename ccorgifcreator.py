import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# 1. Configuration
URL = "https://services.swpc.noaa.gov/images/animations/ccor1/"
OUTPUT_PATH = "noaa_ccor1_animation.gif" 

def main():
    print("Scanning NOAA directory...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_names = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.jpg') and 'latest' not in a['href']]
    img_names.sort()
    img_names = img_names[::5] # Frame skip

    if not img_names:
        print("No images found.")
        return

    frames = []
    for name in img_names:
        try:
            response = requests.get(URL + name)
            img = Image.open(BytesIO(response.content)).resize((512, 480), Image.Resampling.LANCZOS).convert('P', palette=Image.ADAPTIVE, colors=128)
            frames.append(img)
        except Exception as e:
            print(f"Skipping {name}: {e}")

    if frames:
        frames[0].save(OUTPUT_PATH, format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0, optimize=True)
        print("✅ GIF compiled and saved successfully.")
    else:
        print("No frames processed.")

if __name__ == "__main__":
    main()
