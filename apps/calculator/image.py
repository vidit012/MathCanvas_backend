from fastapi import APIRouter
import base64
from io import BytesIO
from schemareq import ImageData
from apps.calculator.utils2 import understand_image
from apps.calculator.utils3 import generate_image
from PIL import Image

router=APIRouter()


@router.post('')
async def run(imageData:ImageData):
    image_data=base64.b64decode(imageData.image.split(",")[1])
    image_bytes=BytesIO(image_data)
    image=Image.open(image_bytes)
    responses=understand_image(img=image,dict_of_vars=imageData.dict_of_vars)
    
    data=[]
    for response in responses:
        data.append(response)
        
    ##image_details=str(response)

    print('response in route: ', response.get("Attributes"))
    attributes=response.get("Attributes")
    primary_object=response.get("Primary Object")
    context=response.get("Context")
    style_notes=response.get("Style Notes")
    
    generated_image=generate_image(attributes,primary_object,context,style_notes);
    
    buffer = BytesIO()
    generated_image.save(buffer, format="PNG")
    buffer.seek(0)
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    return {"message": "Image processed", "data": data, "status": "success","image": f"data:image/png;base64,{base64_image}",}