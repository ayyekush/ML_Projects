from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()
#linking static and templating dir
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from SCRAPERS.WebScraper import prepareChromeDriver,scrapeNReviewsHumanoid,scrapeNReviewsFast,openingReviewSite
def scrapeReviewFn(method,userLink,n_reviews):
    driver=prepareChromeDriver()
    openingReviewSite(userLink,driver)
    if method=="FAST":
        #returns a list of all reviews scraped instantaeosiuly
        return scrapeNReviewsFast(n_reviews,driver)
    else:
        #returns a generator fn to scrape one by one on command
        return scrapeNReviewsHumanoid(n_reviews,driver)

from Prediction import finalPrediction
from EDAFns import wordRankingDF,wordCloud

@app.post("/fast-reviews-scrape")
async def fastReviewsScrape(request: Request):
    data=await request.json()
    userLink =data.get("url")
    n_reviews =int(data.get("reviewsToScrape"))

    scraped_reviews_list=scrapeReviewFn("FAST",userLink,n_reviews)

    prediction=finalPrediction(scraped_reviews_list)
    wordCloud(wordRankingDF(scraped_reviews_list))


    return JSONResponse(content={
        "ScrapedReviewsList": scraped_reviews_list,
        "prediction": prediction,
        "WordCloudAddress": "/static/alpha.png",
    })

latest_review={"rNo":-1,"reviewText":"NULL"}
@app.get("/latest-review",response_class=JSONResponse)
async def latestReview():
    return JSONResponse(content={"rNo":latest_review["rNo"],"reviewText":latest_review["reviewText"]})

@app.post("/slower-reviews-scrape",response_class=JSONResponse)
async def slowReviewsScrape(request: Request):
    print("reached here")
    data=await request.json()
    userLink=data.get("url")
    n_reviews=int(data.get("reviewsToScrape"))
    speed=data.get("speed")

    driver = prepareChromeDriver()
    openingReviewSite(userLink, driver)
    async def slow_scrape():
        global latest_review
        scraped_reviews_generator=scrapeNReviewsHumanoid(n_reviews, driver, speed)
        reviews_list=[]

        for i, val in enumerate(scraped_reviews_generator):
            latest_review["rNo"] = i
            latest_review["reviewText"] = val
            reviews_list.append(val)
            await asyncio.sleep(0.1)  # small sleep to simulate delay (backend pace)
        return reviews_list

    scraped_reviews =await slow_scrape()

    # ML +WordCloud
    prediction =finalPrediction(scraped_reviews)
    wordCloud(wordRankingDF(scraped_reviews))

    return JSONResponse(content={
        "ScrapedReviewsList": scraped_reviews,
        "prediction": prediction,
        "WordCloudAddress": "/static/alpha.png",
    })
if __name__=="__main__":
    print("run through uvicorn")