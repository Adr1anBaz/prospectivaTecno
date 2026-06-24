import os
import urllib.request
import zipfile

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
MODEL_DIR = "models/vosk"
MODEL_NAME = "vosk-model-small-es-0.42"


def download():
    """Download and extract the Vosk Spanish model."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    zip_path = os.path.join(MODEL_DIR, f"{MODEL_NAME}.zip")
    extract_path = os.path.join(MODEL_DIR, MODEL_NAME)

    if os.path.exists(extract_path):
        print(f"Model already exists at: {extract_path}")
        return extract_path

    if not os.path.exists(zip_path):
        print(f"Downloading {MODEL_URL}...")
        print("This may take a few minutes (42MB)...")
        urllib.request.urlretrieve(MODEL_URL, zip_path)
        print("Download complete!")
    else:
        print(f"Zip file already downloaded: {zip_path}")

    print("Extracting...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(MODEL_DIR)
    print("Extraction complete!")

    # Remove zip to save space
    os.remove(zip_path)
    print(f"Cleaned up zip file.")

    print(f"\nModel available at: {extract_path}")
    print(f"Add this to your .env: VOSK_MODEL_PATH={extract_path}")
    return extract_path


if __name__ == "__main__":
    download()
