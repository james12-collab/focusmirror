from pyngrok import conf, ngrok
import time

conf.get_default().auth_token = '3DrLlNIrwJNNaPSdnhvj9S5PWxw_6HHaNYBhV69yP7mHWRWmV'

tunnel = ngrok.connect(5000)
print("=" * 50)
print("Your public URL:")
print(tunnel.public_url)
print("=" * 50)
print("Keep this window open! Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.kill()