import replicate
import requests
import os
import config
import requests
from halo import Halo

spinner = Halo(text='Loading', spinner='dots')
os.environ['REPLICATE_API_TOKEN']= config.REPLICATE_API_TOKEN

API_URL = "https://api-inference.huggingface.co/models/succinctly/text2image-prompt-generator"
headers = {"Authorization": "Bearer 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"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def imageMaker (customPrompt, nameOfFile):
    
    print(customPrompt)
    try:
        prompt = (query(customPrompt))[0]['generated_text']
    except:
        print("error")
        prompt = customPrompt
    print(prompt)
    model = model = replicate.models.get("tstramer/midjourney-diffusion")
    version = model.versions.get("436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b")
  
    # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#input
    inputs = {
        # Input prompt
        'prompt': prompt,

        # Specify things to not see in the output
        # 'negative_prompt': ...,

        # Width of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'width': 512,

        # Height of output image. Maximum size is 1024x768 or 768x1024 because
        # of memory limits
        'height': 512,

        # Prompt strength when using init image. 1.0 corresponds to full
        # destruction of information in init image
        'prompt_strength': 0.8,

        # Number of images to output.
        # Range: 1 to 4
        'num_outputs': 1,

        # Number of denoising steps
        # Range: 1 to 500
        'num_inference_steps': 50,

        # Scale for classifier-free guidance
        # Range: 1 to 20
        'guidance_scale': 7.5,

        # Choose a scheduler.
        'scheduler': "KLMS",

    }

    # https://replicate.com/tstramer/midjourney-diffusion/versions/436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b#output-schema
    output = version.predict(**inputs)
    print(output)

    response = requests.get(output[0])
    content = response.content
    

    with open("files/output.png", "wb") as f:
        f.write(content)
        


