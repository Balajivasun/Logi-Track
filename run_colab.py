import nest_asyncio
from pyngrok import ngrok
import uvicorn
import os

print("Starting LOGI-TRACK on Google Colab...")

# 1. Change working directory to the project folder
try:
    os.chdir('/content/logi-track')
except FileNotFoundError:
    print("Warning: /content/logi-track folder not found. Running in current directory.")

# 2. Allow Uvicorn to run inside Colab
nest_asyncio.apply()

# ---------------------------------------------------------
# 3. PASTE YOUR NGROK AUTH TOKEN BELOW
# ---------------------------------------------------------
ngrok.set_auth_token("3HLlgFZZefS8V1nyMDDNq6k6KpT_6VupKW8bsCvVC31CVcwve")

# 4. Open a public tunnel
try:
    public_url = ngrok.connect(8000)
    print("\n" + "="*60)
    print(f"👉 OPEN THIS LINK TO VIEW LOGI-TRACK: {public_url.public_url}")
    print("="*60 + "\n")
except Exception as e:
    print(f"Failed to start ngrok tunnel. Did you replace YOUR_NGROK_AUTH_TOKEN? Error: {e}")

# 5. Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
