from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from keras.models import load_model
import pickle

app =FastAPI()
templates=Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/",response_class=HTMLResponse)
async def home(req:Request):
    return templates.TemplateResponse(
        "index.html",
        {"request":req}
    )

with open("./ARTIFACTS/Bow.pkl","rb") as file:
    BOW_Vectorizer=pickle.load(file)
with open("./ARTIFACTS/Tfidf.pkl","rb") as file:
    TFIDF_Vectorizer=pickle.load(file)

with open("./ClassicalML_MODELS/LogR_Bow.pkl","rb") as file:
    LogR_BOW_Model=pickle.load(file)
with open("./ClassicalML_MODELS/LogR_Tfidf.pkl","rb") as file:
    LogR_TFIDF_Model=pickle.load(file)

with open("./NaiveBayes_MODELS/BNB_Model_With_Bow.pkl","rb") as file:
    BNB_Model_With_Bow=pickle.load(file)
with open("./NaiveBayes_MODELS/BNB_Model_With_Tfidf.pkl","rb") as file:
    BNB_Model_With_Tfidf=pickle.load(file)

with open("./NaiveBayes_MODELS/MNB_Model_With_Bow.pkl","rb") as file:
    MNB_Model_With_Bow=pickle.load(file)
with open("./NaiveBayes_MODELS/MNB_Model_With_Tfidf.pkl","rb") as file:
    MNB_Model_With_Tfidf=pickle.load(file)

with open("./NaiveBayes_MODELS/GNB_Model_With_Bow.pkl","rb") as file:
    GNB_Model_With_Bow=pickle.load(file)
with open("./NaiveBayes_MODELS/GNB_Model_With_Tfidf.pkl","rb") as file:
    GNB_Model_With_Tfidf=pickle.load(file)

with open("./ARTIFACTS/PCAforSVC.pkl","rb") as file:
    PCAforSVC=pickle.load(file)
with open("./SVM_MODELS/SVC_Bow.pkl","rb") as file:
    SVC_BOW_Model=pickle.load(file)
with open("./SVM_MODELS/SVC_Tfidf.pkl","rb") as file:
    SVC_TFIDF_Model=pickle.load(file)

ANN_BOW_Model=load_model("./NeuralNetwork_MODELS/ANN_Bow.keras")
ANN_TFIDF_Model=load_model("./NeuralNetwork_MODELS/ANN_Tfidf.keras")

@app.post("/predict-single-review",response_class=JSONResponse)
async def predictSingleReview(req:Request):
    data=await req.json()
    print(data)
    if data["vectorizer"]=="bow":
        to_test=BOW_Vectorizer.transform([data["text"]])
        # to_test=[[to_test]]
        if data["model"]=="ann":
            to_test=BOW_Vectorizer.transform([data["text"]]).toarray()
            pred=ANN_BOW_Model.predict(to_test).toarray()
            pred=pred[0][0]
        elif data["model"]=="svm":
            to_test=PCAforSVC.transform(to_test)
            pred=SVC_BOW_Model.predict(to_test)
            pred=pred[0]
        elif data["model"]=="lr":
            pred=LogR_BOW_Model.predict(to_test)
            pred=pred[0]
        elif data["model"]=="nb_bern":
            pred=BNB_Model_With_Bow.predict(to_test)
            pred=pred[0]
        elif data["model"]=="nb_gauss":
            pred=GNB_Model_With_Bow.predict(to_test.toarray())
            pred=pred[0]
        else: #multi and others
            pred=MNB_Model_With_Bow.predict(to_test)
            pred=pred[0]

    elif data["vectorizer"]=="tfidf":
        to_test=TFIDF_Vectorizer.transform([data["text"]])
        # to_test=[[to_test]]
        if data["model"]=="ann":
            to_test=TFIDF_Vectorizer.transform([data["text"]]).toarray()
            pred=ANN_TFIDF_Model.predict(to_test)
            pred=pred[0][0]
        elif data["model"]=="svm":
            to_test=PCAforSVC.transform(to_test)
            pred=SVC_TFIDF_Model.predict(to_test)
            pred=pred[0]
        elif data["model"]=="lr":
            pred=LogR_TFIDF_Model.predict(to_test)
            pred=pred[0]
        elif data["model"]=="nb_bern":
            pred=BNB_Model_With_Tfidf.predict(to_test)
            pred=pred[0]
        elif data["model"]=="nb_gauss":
            pred=GNB_Model_With_Tfidf.predict(to_test.toarray())
            pred=pred[0]
        else: #multi and others
            pred=MNB_Model_With_Tfidf.predict(to_test)
            pred=pred[0]
    # pred=pred[0][0]
    print(pred)
    return JSONResponse(content={
        "confidence":str(pred),
        "sentiment":"1" if pred>0.5 else "0",
    })
if __name__=="__main__":
    import uvicorn
    import os
    port=int(os.environ.get("PORT",8080))
    uvicorn.run("app:app",host="0.0.0.0", port=port)



