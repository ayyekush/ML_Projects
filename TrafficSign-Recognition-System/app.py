import numpy as np
import pandas as pd
from PIL import Image
import os
import keras
from random import randint

from fastapi import FastAPI,Form, Request,UploadFile,File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#image will be sent accross in base64
import base64

#for url given image
import io
import requests


app = FastAPI()

#linking static and template dir
templates =Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
    
#laoding our model(L3 for test data and L4 for new) L stands for grayscale
model1=keras.models.load_model("./MODELS/RNN_Traffic_L3.keras")
model2=keras.models.load_model("./MODELS/RNN_Traffic_L4.keras")

#meta data
meta_csv=pd.read_csv("./Reduced_DATASET/Meta.csv")
META_IMG_DIR={CLASS_ID:f"./Reduced_DATASET/{META_IMG_PATH}" for CLASS_ID,META_IMG_PATH in zip(meta_csv["ClassId"],meta_csv["Path"])}

#home route
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
        )

@app.post("/predict-uploaded-img")
async def predict_uploaded_img(uploaded_Img:UploadFile=File(...)):
    #its a fast api uploaded file, we can directly read it in binary
    contents =await uploaded_Img.read()
    img =Image.open(io.BytesIO(contents)).convert("L")
        
    from PIL import ImageEnhance
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    # Resize using better quality interpolation
    img = img.resize((30, 30), Image.LANCZOS)
    
    # img=img.resize((30,30))
    img=np.array(img, dtype=np.float32) / 255.0
    # img=np.array(img, dtype=np.float32) / 255.0 
    #predict the bin image now
    pred_Class,meta_Img_Address,confidence=await predict_image(img,model2)
    with open(meta_Img_Address,"rb") as img_file:
        img_bin=img_file.read()
        base64_Meta_Img=base64.b64encode(img_bin).decode("utf-8")

    return {
        "base64_Meta_Img": base64_Meta_Img,
        "confidence": float(confidence),
    }

@app.post("/predict-from-url")
async def predict_from_url(url: str = Form(...)):
    #gets the url data in binary format
    get_img_from_url=requests.get(url).content
    img=Image.open(io.BytesIO(get_img_from_url)).convert("L")

    img=img.resize((30,30))
    
    img=np.array(img, dtype=np.float32) / 255.0
    
    pred_Class,meta_Img_Address,confidence=await predict_image(img,model2)
    
    #converting meta img into sendable base 64
    with open(meta_Img_Address,"rb") as img_file:
        img_binaary=img_file.read()
        base64_Meta_Img=base64.b64encode(img_binaary).decode("utf-8")
    
    return {
        "base64_Meta_Img": base64_Meta_Img,
        "confidence": float(confidence),
    }

@app.get("/n-random-predictions")
async def n_random_predictions(n:int=5):
    #randomly selects five img from 200 test images
    starting_Img_No=randint(0,199-n)
    test_img_paths=[f"./Reduced_DATASET/Test/{i}" for i in os.listdir("./Reduced_DATASET/Test/")[starting_Img_No:starting_Img_No+n]]

    #predicting and then convert each into sendable base64 format
    test_img_base64_list=[]
    meta_img_base64_list=[]
    for i in range(n):
        img=Image.open(test_img_paths[i]).convert("L")
        img=img.resize((30,30))

        img=np.array(img, dtype=np.float32) / 255.0
        pred_Class,meta_Img_Add,confidence=await predict_image(np.array(img),model=model1)
        with open(META_IMG_DIR[pred_Class],"rb") as meta_img_file:
            meta_img_bin=meta_img_file.read()
            meta_img_b64=base64.b64encode(meta_img_bin).decode("utf-8")
            meta_img_base64_list.append(meta_img_b64)

        with open(test_img_paths[i],"rb") as img_file:
            img_bin=img_file.read()
            img_base64=base64.b64encode(img_bin).decode("utf-8")
            test_img_base64_list.append(img_base64)

    return {
        "test_Img_List":test_img_base64_list,
        "pred_Meta_Img_List":meta_img_base64_list
    }

async def predict_image(img:np.ndarray ,model):
    #preporocess image

    img=np.expand_dims(img, axis=-1)#for since grayscalae
    img=np.expand_dims(img, axis=0)#to make it in list form
    
    #predict
    pred=model.predict(img, verbose=0)[0]
    pred_class=np.argmax(pred)
    
    #return predicted class, metaimgfilepath, and confidence
    return int(pred_class),META_IMG_DIR[pred_class],pred[pred_class]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",host="0.0.0.0", port=5050)