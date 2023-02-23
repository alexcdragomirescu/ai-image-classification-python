import nltk
from nltk.stem import PorterStemmer
from PIL import Image
import requests
import random
import os
from pathlib import PurePath, Path
import re
import urllib


currentDir = PurePath(Path.cwd())
downloadDir = currentDir.joinpath("downloads")

def mkdir(dir):
    dir.mkdir() if not dir.exists() else None

def download_image(url, folder):
    response = requests.get(url)
    p = re.compile(r"(^.*)?\?")
    basename = p.findall(os.path.basename(response.url))[0] \
        if p.findall(os.path.basename(response.url)) \
            else os.path.basename(url)

    print(response.url)
    print(basename)
    filename = os.path.join(folder, basename)
    with open(filename, 'wb') as f:
        f.write(response.content)

sentence = "The quick brown fox jumps over the lazy dog."
tokens = nltk.word_tokenize(sentence)

stemmer = PorterStemmer()

words = ["playing", "played", "plays"]
stemmed_words = list(set([stemmer.stem(word) for word in words]))

print(tokens)
print(stemmed_words)

mkdir(Path(downloadDir))
urls = ['https://source.unsplash.com/random', 'https://picsum.photos/200', 'https://loremflickr.com/320/240']

num_images = 5
for i in range(num_images):
    url = random.choice(urls)
    download_image(url, downloadDir)

