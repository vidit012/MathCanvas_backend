import google.generativeai as genai
import os
from dotenv import load_dotenv
import ast
from PIL import Image

load_dotenv()

gemini_api_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

def understand_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = (
    f"You are an AI model designed to analyze and interpret drawings provided by users. "
    
    f"Primary Object Identification:\\n"
    f"Identify the main object or theme depicted in the drawing. Be creative but stay grounded in the details of the image.\\n\\n"
    
    f"Attributes Description:\\n"
    f"Describe key characteristics of the drawing such as shape, size, texture, or patterns. Consider any distinct visual features that stand out.\\n\\n"
    
    f"Contextual Details:\\n"
    f"Add possible context based on the drawing. This can include the environment, setting, or mood of the image. If there are interactions or relationships between objects, mention them.\\n\\n"
    
    f"Style Notes:\\n"
    f"Describe the style of the drawing, if any. Is it sketchy, detailed, minimalist, or abstract? Also, note the perspective (e.g., top-down view, side view, etc.) and any specific artistic techniques used.\\n\\n"
    
    f"Return Format: [{{'Primary Object': 'description', 'Attributes': 'description', 'Context': 'description', 'Style Notes': 'description'}}]\\n"
    f"Example: [{{'Primary Object': 'tree', 'Attributes': 'a simple tree with a trunk and leafy branches', 'Context': 'the tree is drawn against a plain background', 'Style Notes': 'sketched with basic lines and no shading'}}]\\n\\n"
    
    f"DO NOT USE BACKTICKS OR MARKDOWN FORMATTING. "
    f"PROPERLY QUOTE THE KEYS AND VALUES IN THE DICTIONARY FOR EASIER PARSING WITH Python's ast.literal_eval."
    )
    
    response = model.generate_content([prompt, img])
    
    answers = []
    try:
        answers = ast.literal_eval(response.text)
    except Exception as e:
        print(f"Error in parsing response from Gemini API: {e}")
   
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
       
    return answers;
    

    
