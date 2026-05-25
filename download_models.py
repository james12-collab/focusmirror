import requests, os

os.makedirs('static', exist_ok=True)

print("Downloading BlazeFace model...")
url = "https://tfhub.dev/tensorflow/tfjs-model/blazeface/1/default/1/model.json"
# We'll use CDN instead - no download needed
print("BlazeFace uses CDN - no download needed!")
print("Done!")