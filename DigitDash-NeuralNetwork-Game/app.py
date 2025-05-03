from fastapi import FastAPI,Request,Form,UploadFile
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
from keras.models import load_model
import io,json
import numpy as np
app=FastAPI()

# mounting static and templates folders
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

#creating a class for the leaderboard entries
from pydantic import BaseModel
class LeaderboardEntry(BaseModel):
    userId:str
    score:int

#to read from leaderboard.json and keep ;leaderboard updated
@app.get("/api/leaderboard", response_class=JSONResponse)
async def get_leaderboard():
    with open("leaderboard.json","r") as file:
        leaderboard_data=json.load(file)
    unique_users={}
    for val in leaderboard_data:
        if ((val["userId"] not in unique_users) or (val["score"]>unique_users[val["userId"]])):
            unique_users[val["userId"]] =val["score"]
    
    #listing and sorting unique users
    new_leaderboard = [
        {"userId": user_id, "score": score} 
        for user_id, score in unique_users.items()
    ]
    new_leaderboard.sort(key=lambda x: x["score"], reverse=True)
    #returning only top 10
    return JSONResponse(content=new_leaderboard[:10])

#adding a new entry
@app.post("/api/score", response_class=JSONResponse)
async def update_score(entry: LeaderboardEntry):
    with open("leaderboard.json", "r") as file:
        leaderboard_data = json.load(file)
    #add the new entry
    leaderboard_data.append({"userId": entry.userId, "score": entry.score})
    #save updatyed leaderboard
    with open("leaderboard.json","w") as file:
        json.dump(leaderboard_data,file)
    
    #returningin the new leaderboard
    unique_users={}
    for val in leaderboard_data:
        if ((val["userId"] not in unique_users) or (val["score"]>unique_users[val["userId"]])):
            unique_users[val["userId"]] = val["score"]
    
    processed_leaderboard=[
        {"userId":user_id,"score":score} 
        for user_id, score in unique_users.items()
    ]
    processed_leaderboard.sort(key=lambda x: x["score"], reverse=True)
    #again returning top 10 players
    return JSONResponse(content=processed_leaderboard[:10])
    

    
@app.get("/", response_class=HTMLResponse)
async def homePage(req:Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request":req
        }
    )

model=load_model("MODELS/mnistANNModel.keras")
@app.post("/mnist", response_class=JSONResponse)
async def predDigit(img_param:UploadFile=Form(...)):
    img=await img_param.read()
    img=Image.open(io.BytesIO(img))
    img=img.convert("L")
    img=img.resize((28,28))
    img_array=np.array(img, dtype=np.float32)
    img_array=img_array/255.0
    # img_array=1-img_array
    img=img_array.reshape(1, 784).astype("float32")
    pred_array=model.predict(img,verbose=False)
    pred_Digit=np.argmax(pred_array)
    print(pred_Digit,pred_array)
    return JSONResponse(content={
        "pred_Digit":str(pred_Digit), 
    })


if __name__=="__main__":
    import uvicorn
    uvicorn.run("app:app",host="0.0.0.0", port=8080, reload=True)