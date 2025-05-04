import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from keras.models import load_model




def randomTestsrediction(lower,upper,model_choice:str):
    if (model_choice=="L"):
        model=load_model("./MODELS/RNN_Traffic_L4.keras")
    elif (model_choice=="RGB"):
        model=load_model("./MODELS/RNN_Traffic.keras")
    else:
        return False
    test_img_paths=pd.read_csv("./DATASET/Test.csv")["Path"].iloc[lower:upper]
    test_img_labels=pd.read_csv("./DATASET/Test.csv")["ClassId"].iloc[lower:upper]
    
    accuracyList=[]
    predList=[]
    for i in range(len(test_img_paths)):
        if (model_choice=="L"):
            img=Image.open("./DATASET/"+test_img_paths.iloc[i]).convert("L")
        elif (model_choice=="RGB"):
            img=Image.open("./DATASET/"+test_img_paths.iloc[i])
        else:
            raise False
        








        # img=img.resize((30,30))
        img=np.array(img,dtype=np.float32)/255.0
        if (model_choice=="L"):
            img=np.expand_dims(img,axis=-1)
        img=np.expand_dims(img,axis=0)
        prediction_ohe=model.predict(img,verbose=0)[0]
        pred=np.argmax(prediction_ohe)
        predList.append(pred)
        accuracyList.append(int(pred==test_img_labels.iloc[i]))
    return (accuracyList, predList)

def VisualisePrediction(lower,upper,model_choice:str):
    if (model_choice=="L"):
        model=load_model("./MODELS/RNN_Traffic_L4.keras")
    elif (model_choice=="RGB"):
        model=load_model("./MODELS/RNN_Traffic.keras")
    else:
        return False
    test_img_paths=pd.read_csv("./DATASET/Test.csv")["Path"].iloc[lower:upper]
    test_img_labels=pd.read_csv("./DATASET/Test.csv")["ClassId"].iloc[lower:upper]
    meta=pd.read_csv("./DATASET/Meta.csv").sort_values(["ClassId"])["Path"]
    fig,axes=plt.subplots(upper-lower,2,figsize=(10,6.5))
    predCorrectList=[]
    for i in range(upper-lower):
        if (model_choice=="L"):
            img=Image.open("./DATASET/"+test_img_paths.iloc[i]).convert("L")
        elif (model_choice=="RGB"):
            img=Image.open("./DATASET/"+test_img_paths.iloc[i])
        img=img.resize((30,30))
        img=np.array(img,dtype=np.float32)/255.0
        axes[i][0].imshow(img)
        axes[i][0].set_title(f"Test_Image {i+1}")
        if (model_choice=="L"):
            img=np.expand_dims(img,axis=-1)
        img=np.expand_dims(img,axis=0)#for batch_size
        predOHEd=model.predict(img,verbose=0)
        pred=np.argmax(predOHEd)
        predCorrectList.append(True if (test_img_labels.iloc[i]==pred) else False)
        matching_meta_img=Image.open("./DATASET/"+meta.iloc[pred])
        axes[i][1].imshow(matching_meta_img)
        axes[i][1].set_title(f"Result: {predCorrectList[i]} Prediciton")
    plt.tight_layout()#reduces gutter margins
    plt.show()
    return predCorrectList

def customPrediction(path,model_choice:str,throughFrontend=False):
    meta=pd.read_csv("./DATASET/Meta.csv").sort_values(["ClassId"])["Path"]
    if (model_choice=="RGB"):
        model=load_model("./MODELS/RNN_Traffic.keras")
        img=Image.open(path)
    else: #(model_choice=="L")
        model=load_model("./MODELS/RNN_Traffic_L4.keras")
        img=Image.open(path).convert("L")
    if (throughFrontend):
        if (model_choice=="L"):
            img=np.expand_dims(img,axis=-1)#since L read doesnt have layers
        img=np.expand_dims(img,axis=0)#making list
        predOHEd=model.predict(img,verbose=0)
        predClass=np.argmax(predOHEd)
        matching_meta_img_path:str=f"/static/Meta/{meta.iloc[predClass]}.png"
        return matching_meta_img_path
    else:
        
        from PIL import ImageEnhance
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        # Resize using better quality interpolation
        img = img.resize((30, 30), Image.LANCZOS)



        # img=img.resize((30,30))
        img=np.array(img,dtype=np.float32)/255.0
        fig,axes=plt.subplots(1,2,figsize=(15,6.5))
        axes[0].imshow(img)
        axes[0].set_title("Test_Image")
        if (model_choice=="L"):
            img=np.expand_dims(img,axis=-1)#since L read doesnt have layers
        img=np.expand_dims(img,axis=0)#to make it a list of imgs
        predOHEd=model.predict(img,verbose=0)
        predClass=np.argmax(predOHEd)
        matching_meta_img=Image.open("./DATASET/"+meta.iloc[predClass])
        axes[1].imshow(matching_meta_img)
        axes[1].set_title(f"This is our closest match :)")
        plt.tight_layout()#reduces gutter margins
        plt.show()
        return predClass


if __name__=="__main__":
    Nof_TEST_IMAGES=12_629
    model_choice="L" or "RGB"
    # # BuildModel(*PreparingData(train_df,test_df,model_choice),model_choice)
    # from random import randint
    # Nof_Preds_WE_WANT=30
    # ran=randint(0,Nof_TEST_IMAGES-Nof_Preds_WE_WANT)
    # accuracy_list,pred=Prediction(ran,ran+Nof_Preds_WE_WANT,model_choice)
    # print("Prediction Accuracy: ",sum(accuracy_list)/Nof_Preds_WE_WANT*100,"%\n")

    # Nof_Visuals_WE_WANT=5
    # ran=randint(0,Nof_TEST_IMAGES-Nof_Visuals_WE_WANT)
    # predCorrectList=VisualisePrediction(ran,ran+Nof_Visuals_WE_WANT,model_choice)
    # print("\nVisual Prediction Accuracy: ",sum(predCorrectList)/Nof_Visuals_WE_WANT*100,"%")

    predClass=customPrediction("./ts8.png",model_choice)