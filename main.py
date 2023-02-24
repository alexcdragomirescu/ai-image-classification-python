import nltk
from nltk.stem import PorterStemmer
from PIL import Image
import requests
import random
import os
from pathlib import PurePath, Path
import re
from urllib.parse import urlparse, parse_qs
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from sklearn.cluster import KMeans


def mkdir(dir):
    dir.mkdir() if not dir.exists() else None

def remove_files(path, parent=''):
    if os.path.isdir(path):
        for root, dirs, files in os.walk(os.path.abspath(path), topdown=False):
            for f in files:
                os.remove(os.path.join(root, f))
            for d in dirs:
                os.rmdir(os.path.join(root, d))
        if parent:
            os.rmdir(path)

def download_image(url, folder):
    response = requests.get(url)
    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)
    p = re.compile(r"(^.*)?\?")
    basename = p.findall(os.path.basename(response.url))[0] \
        if p.findall(os.path.basename(response.url)) \
        else os.path.basename(response.url)

    format_ = query_params.get('fm') if query_params.get('fm') else None
    format_ = '.' + format_[0] if format_ else ''
    basename = basename + format_

    filename = os.path.join(folder, basename)
    print(filename)
    with open(filename, 'wb') as f:
        f.write(response.content)


currentDir = PurePath(Path.cwd())
imagesDir = currentDir.joinpath("images")

mkdir(Path(imagesDir))
remove_files(imagesDir)

urls = ['https://source.unsplash.com/random', 'https://picsum.photos/200',
        'https://loremflickr.com/320/240']

numImages = 12
for i in range(numImages):
    url = random.choice(urls)
    download_image(url, imagesDir)

images = []
for f in os.listdir(imagesDir):
    img = cv2.imread(os.path.join(imagesDir, f))
    if img is not None:
        images.append(img)
images = np.array(images)

resImages = []
for img in images:
    resImg = cv2.resize(img, (100, 100)) # specify size to resize to
    resImages.append(resImg)
resized_images = np.array(resImages)

flattened_images = resized_images.reshape(len(resized_images), -1)

kmeans = KMeans(n_clusters=2, random_state=0).fit(flattened_images)
labels = kmeans.labels_

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(images[0])
axs[0].set_title('Original Image')
axs[1].imshow(images[labels==0][0])
axs[1].set_title('Cluster 1')
plt.show()

