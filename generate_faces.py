import os
import requests
import hashlib
import glob
from time import sleep
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

class ThisPersonDoesNotExist:
    def __init__(self, save_dir="ai_faces", num_faces=10000, delay=0.5, num_threads=10):
        self.url = "https://thispersondoesnotexist.com"
        self.save_dir = save_dir
        self.num_faces = num_faces
        self.delay = delay
        self.num_threads = num_threads
        self.hashes = set()
        self.existing_images = set()

        os.makedirs(self.save_dir, exist_ok=True)
        self._load_existing_images()

    def _load_existing_images(self):
        existing_files = glob.glob(os.path.join(self.save_dir, "*.jpg"))
        for file in existing_files:
            with open(file, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
                self.hashes.add(file_hash)
                self.existing_images.add(file)

    def download_image(self):
        try:
            response = requests.get(self.url, timeout=10)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            print(f"Erreur: {e}")
        return None

    def save_image(self, image, filename):
        filepath = os.path.join(self.save_dir, filename)
        image.save(filepath, format="JPEG")

    def is_duplicate(self, image):
        hash_md5 = hashlib.md5(image.tobytes()).hexdigest()
        if hash_md5 in self.hashes:
            return True
        self.hashes.add(hash_md5)
        return False

    def generate_faces(self):
        count = len(self.existing_images)
        needed_faces = self.num_faces - count
        print(f"Images existantes : {count}, Objectif : {self.num_faces}")

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = []
            for _ in range(needed_faces):
                futures.append(executor.submit(self.process_single_image))

            for future in tqdm(futures, desc="Téléchargement des images"):
                future.result()

        print(f"✅ Génération terminée : {len(glob.glob(os.path.join(self.save_dir, '*.jpg')))} images enregistrées.")

    def process_single_image(self):
        sleep(self.delay)
        image = self.download_image()
        if image:
            if not self.is_duplicate(image):
                count = len(glob.glob(os.path.join(self.save_dir, "*.jpg"))) + 1
                filename = f"face_{count}.jpg"
                self.save_image(image, filename)

if __name__ == "__main__":
    for batch_number in range(1, 8):
        print(f" Démarrage du batch {batch_number}...")
        generator = ThisPersonDoesNotExist(save_dir=f"ai_faces_batch_{batch_number}", num_faces=10000, delay=0.3, num_threads=10)
        generator.generate_faces()

    print(" Toutes les images ont été générées avec succès !")