from fastapi import APIRouter
import base64
from io import BytesIO
from schemareq import ImageData
from apps.calculator.utils import analyze_image
from PIL import Image

router=APIRouter()

@router.post('')
async def run(imageData:ImageData):
    image_data=base64.b64decode(imageData.image.split(",")[1])
    image_bytes=BytesIO(image_data)
    image=Image.open(image_bytes)
    responses=analyze_image(img=image,dict_of_vars=imageData.dict_of_vars)
    
    data=[]
    for response in responses:
        data.append(response)
    print('response in route: ', response)
    return {"message": "Image processed", "data": data, "status": "success"}
    
    