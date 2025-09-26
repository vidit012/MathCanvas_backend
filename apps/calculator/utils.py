import google.generativeai as genai
import os
from dotenv import load_dotenv
import ast
import json
from PIL import Image

load_dotenv()

gemini_api_key=os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

def analyze_image(img: Image, dict_of_vars: dict):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    dict_of_vars_str = json.dumps(dict_of_vars, ensure_ascii=False)
    prompt = (
    f"You are an advanced mathematical problem solver tasked with analyzing and solving mathematical expressions from images. "

    f"Mathematical Expression Rules:\\n"
    f"Follow the PEMDAS rule for solving all mathematical expressions:\\n"
    f"- P: Parentheses (highest priority)\\n"
    f"- E: Exponents\\n"
    f"- M/D: Multiplication and Division (left to right)\\n"
    f"- A/S: Addition and Subtraction (left to right)\\n\\n"

    f"Examples with Detailed Solutions:\\n"
    f"1. Expression: 2 + 3 * 4\\n"
    f"   Step-by-step solution:\\n"
    f"   - First multiply: 3 * 4 = 12 (multiplication before addition)\\n"
    f"   - Then add: 2 + 12 = 14\\n"
    f"   Final answer: 14\\n\\n"
    
    f"2. Expression: 2 + 3 + 5 * 4 - 8 / 2\\n"
    f"   Step-by-step solution:\\n"
    f"   - First handle multiplication: 5 * 4 = 20\\n"
    f"   - Then division: 8 / 2 = 4\\n"
    f"   - Finally, perform addition and subtraction left to right: 2 + 3 + 20 - 4 = 21\\n"
    f"   Final answer: 21\\n\\n"
    
    
    f"Problem Types and Return Formats:\\n\\n"
    
    f"1. Simple Mathematical Expressions\\n"
    f"   Input example: 2 + 2, 3 * 4, etc.\\n"
    f"   Return format: [{{'expr': 'given_expression', 'result': calculated_answer}}]\\n"
    f"   Example: [{{'expr': '2 + 2', 'result': 4}}]\\n\\n"
    
    f"2. Systems of Equations\\n"
    f"   Input example: x^2 + 2x + 1 = 0, 3y + 4x = 0\\n"
    f"   Return format: [{{'expr': 'x', 'result': value1, 'assign': True}}, "
    f"                   {{'expr': 'y', 'result': value2, 'assign': True}}]\\n\\n"
    
    f"3. Variable Assignments\\n"
    f"   Input example: x = 4, y = 5\\n"
    f"   Return format: [{{'expr': 'x', 'result': 4, 'assign': True}}]\\n\\n"
    
    f"4. Graphical Math Problems\\n"
    f"   Description: Problems represented through drawings (collisions, triangles, etc.)\\n"
    f"   Special instruction: Consider color variations in drawings\\n"
    f"   Return format: [{{'expr': 'problem_description', 'result': calculated_answer}}]\\n\\n"
    
    f"5. Abstract Concept Detection\\n"
    f"   Description: Identifying abstract concepts from drawings\\n"
    f"   Return format: [{{'expr': 'drawing_explanation', 'result': 'abstract_concept'}}]\\n\\n"
    
    f"Variable Resolution Rules:\\n"
    f"- Use this dictionary for pre-assigned variables: {dict_of_vars_str}\\n"
    f"- Replace all variables with their corresponding values before computation\\n"
    f"- If a variable is not found in the dictionary, treat it as an unknown to be solved\\n\\n"
    
    f"DO NOT USE BACKTICKS OR MARKDOWN FORMATTING. "
    f"PROPERLY QUOTE THE KEYS AND VALUES IN THE DICTIONARY FOR EASIER PARSING WITH Python's ast.literal_eval."
    )
    
    response = model.generate_content([prompt, img])
    print(response.text)
    answers = []
    try:
        answers = ast.literal_eval(response.text)
    except Exception as e:
        print(f"Error in parsing response from Gemini API: {e}")
    print('returned answer ', answers)
    for answer in answers:
        if 'assign' in answer:
            answer['assign'] = True
        else:
            answer['assign'] = False
    return answers

