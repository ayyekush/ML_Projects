import time,random
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

### Preparaing Chrome
def prepareChromeDriver():
    option=Options()
    option.add_argument("--headless=new")
    option.add_argument("user-data-dir=/Users/apple/Library/Application Support/Google/Chrome/LilyViolet")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("start-maximized")
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36")
    driver=webdriver.Chrome(options=option)
    return driver

def openingReviewSite(userLink,driver):
    driver.get(userLink)

    #remove webdriver-flag
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    #clicking on see all reviews
    WebDriverWait(driver,3).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="reviews-medley-footer"]/div[2]/a'))
    )
    driver.find_element(By.XPATH,'//*[@id="reviews-medley-footer"]/div[2]/a').click()


def scrapeNReviewsHumanoid(n_times,driver,speed):
    while(n_times):
        currentPageReviewsList=driver.find_elements(By.CSS_SELECTOR,".review-text-content span")
        currentPageHeight=driver.execute_script("return document.body.scrollHeight")
        if (not currentPageReviewsList):
            return
        for review in currentPageReviewsList:
            if (not review): 
                continue
            if (not n_times):
                return
            driver.execute_script(f"window.scrollBy(0,{currentPageHeight/20});")
            if (speed=="SLOW"):
                time.sleep(random.uniform(2.5,3.0))
            else:
                time.sleep(random.uniform(1.0,1.5))
            yield review.text.strip()
            n_times-=1
        #load next page
        print("\nPage Changed\n")
        # driver.execute_script('document.querySelector("#cm_cr-pagination_bar > ul > li.a-last > a").scrollIntoView();')
        WebDriverWait(driver,3).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'))
        )
        driver.find_element(By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
        time.sleep(2)


def scrapeNReviewsFast(n_times,driver):
    REVIEWS_LIST=[]
    while(n_times):
        for review in driver.find_elements(By.CSS_SELECTOR,".review-text-content span"):
            if (not n_times):
                return REVIEWS_LIST
            REVIEWS_LIST.append(review.text.strip())
            n_times-=1
        #load next pageQ
        print("\nPage Changed\n")
        # driver.execute_script('document.querySelector("#cm_cr-pagination_bar > ul > li.a-last > a").scrollIntoView();')
        WebDriverWait(driver,3).until(
            EC.element_to_be_clickable((By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'))
        )
        driver.find_element(By.XPATH,'//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').click()
        time.sleep(2)
    return REVIEWS_LIST
            
if __name__=="__main__":
    userLink="https://www.amazon.in/GUNAHO-KA-DEVTA-DHARAMVEER-BHARTI/dp/B01MFDA7D5/ref=sr_1_1?crid=3CK67C7RWOT8Y&dib=eyJ2IjoiMSJ9.R_6lnmmAU5zgJpshyz9Dp4v9jOhm9J-1rTVwAEAmz-YFTkxWk9C46qtTXl5O4Zw4qOARqzj2x4dT2ZJHku-A_OYghSsxh_QasIStGjLUTE9HNAJdX1Ylj_mX_Rjm5_JGzbg-nBba-eBeTDa08_bKbzPXtk3nACFn3ybMucq4Z8IbmmnuyT9jmgLYfZLA3-TihRMJwJDOlMrJj7hrbViH_e-TRdHOpl6vzb5IBb8RrPM.-Mq2N-sdlLnl-URvZV-JTgk0NhkQ9BP1hJ5-mdDq2o0&dib_tag=se&keywords=gunaho+ka+devta&qid=1744238755&sprefix=gunaho+ka+dev%2Caps%2C362&sr=8-1"
    driver=prepareChromeDriver()
    openingReviewSite(userLink,driver)
    # for i in scrapeNReviewsHumanoid(40,driver):
    #     print(i)
    scraped_reviews_generator=scrapeNReviewsHumanoid(2,driver)
    reviews_list=[]
    latest_review={"rNo":-1,"reviewText":"NULL"}
    k=0
    for i,val in enumerate(scraped_reviews_generator):
        latest_review["rNo"]=i
        latest_review["reviewText"]=val
        print(latest_review)