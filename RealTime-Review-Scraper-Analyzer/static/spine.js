const logs = document.getElementById('logs');
const liveReviewsContainer = document.getElementById('live-reviews-container');
const popup = document.getElementById('review-popup');
const loadingAnimation = document.getElementById('loading-animation');
const stopScrapeButton = document.getElementById('stop-scrape');
let scrapeInterval = null;

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Hide the popup initially
popup.style.display = 'none';

// Function to add a log message
function addLog(message){
  //creating a new div for message
  const logItem = document.createElement('div');
  logItem.className = 'log-item';
  logItem.textContent = `${message}`;
  //appending it to main logs div
  document.querySelector(".logs").appendChild(logItem);
  document.querySelector(".logs").scrollTop = logs.scrollHeight;
}
//Start button handler
// Modify the start-scrape click handler to reset everything first
document.getElementById('start-scrape')
.addEventListener('click', () => {
  // Reset everything first
  resetUI();
  
  const url = document.getElementById('product-url').value.trim();
  const speed = document.getElementById('speed').value;
  const reviewsToScrape = parseInt(document.getElementById('num-reviews').value) || 10;
  
  if (!url) {
    addLog('!!! Not A Valid Amazon product URL !!!');
    return;
  }
  
  document.getElementById('start-scrape').style.display = 'none';
  document.getElementById('in-process').style.display = 'block';
  
  // Add a log message 
  addLog(`Speed: ${speed}`);
  addLog(`Started analyzing ${reviewsToScrape} reviews...`);
  
  document.querySelector('.live-view-header h2').innerHTML = "Live Review Scraping";
  liveReviewsContainer.innerHTML = "";
  document.querySelector("#model-prediction").innerHTML = "";

  if (speed == "FAST") {
    // Show loading animation for fast mode too
    loadingAnimation.style.display = 'block';
    
    fetch('/fast-reviews-scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, reviewsToScrape }),
    })
    .then((response) => response.json())
    .then((result) => {
      // Hide loading animation
      loadingAnimation.style.display = 'none';
      
      document.querySelector('.live-view-header h2').style.fontSize = "40px";
      document.querySelector('.live-view-header h2').innerHTML = "Most Commonly Found Words:";
      const imgAddress = result["WordCloudAddress"];
      
      // Clear the animation container and add the WordCloud image
      const animationContainer = document.querySelector('.animation-container');
      // Make sure we keep the popup and loading elements
      const popupEl = document.getElementById('review-popup');
      const loadingEl = document.getElementById('loading-animation');
      animationContainer.innerHTML = ''; 
      animationContainer.appendChild(popupEl);
      animationContainer.appendChild(loadingEl);
      
      // Create and add the WordCloud image
      const wordCloudImg = document.createElement('img');
      wordCloudImg.src = `${imgAddress}?t=${new Date().getTime()}`;
      wordCloudImg.style.maxWidth = '90%';
      wordCloudImg.style.maxHeight = '90%';
      wordCloudImg.style.objectFit = 'contain';
      wordCloudImg.alt = 'WordCloud of most common words in reviews';
      animationContainer.appendChild(wordCloudImg);
      
      // Add reviews to the collected reviews panel
      let reviewIndex = 1;
      for (const text of result["ScrapedReviewsList"]) {
        addCollectedReview(reviewIndex, text);
        reviewIndex++;
      }
      
      displayMLResult(result["prediction"]);
      document.getElementById('in-process').innerHTML = "RESULTS READY";
      setTimeout(() => {
        document.getElementById('in-process').innerHTML = "IN PROCESS";
        document.getElementById('start-scrape').style.display = 'block';
        document.getElementById('in-process').style.display = 'none';
      }, 6000);
    })
    .catch(error => {
      addLog(`Error: ${error.message}`);
      document.getElementById('start-scrape').style.display = 'block';
      document.getElementById('in-process').style.display = 'none';
    });
  }
  else { 
    // Show loading animation
    loadingAnimation.style.display = 'block';
    
    fetch("/slower-reviews-scrape", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url, speed, reviewsToScrape}),
    })
    .then((response) => response.json())
    .then((result) => {
      delay(3000).then(() => {
        // Hide loading animation
        loadingAnimation.style.display = 'none';
        
        displayMLResult(result["prediction"]);
        document.getElementById('in-process').innerHTML = "RESULTS READY";
        setTimeout(() => {
          document.getElementById('in-process').innerHTML = "IN PROCESS";
          document.getElementById('start-scrape').style.display = 'block';
          document.getElementById('in-process').style.display = 'none';
        }, 6000);

        document.querySelector('.live-view-header h2').style.fontSize = "40px";
        document.querySelector('.live-view-header h2').innerHTML = "Most Commonly Found Words:";
        const imgAddress = result["WordCloudAddress"];
        
        // Clear the animation container and add the WordCloud image
        const animationContainer = document.querySelector('.animation-container');
        // Make sure we keep the popup and loading elements
        const popupEl = document.getElementById('review-popup');
        const loadingEl = document.getElementById('loading-animation');
        animationContainer.innerHTML = ''; 
        animationContainer.appendChild(popupEl);
        animationContainer.appendChild(loadingEl);
        
        // Create and add the WordCloud image
        const wordCloudImg = document.createElement('img');
        wordCloudImg.src = `${imgAddress}?t=${new Date().getTime()}`;
        wordCloudImg.style.maxWidth = '90%';
        wordCloudImg.style.maxHeight = '90%';
        wordCloudImg.style.objectFit = 'contain';
        wordCloudImg.alt = 'WordCloud of most common words in reviews';
        animationContainer.appendChild(wordCloudImg);
      });
    })
    .catch(error => {
        addLog(`Error: ${error.message}`);
        document.getElementById('start-scrape').style.display = 'block';
        document.getElementById('in-process').style.display = 'none';
      });
      
      let prevIndex = -1;
      const displayedReviews = new Set(); // Track displayed reviews
      
      const interval1 = setInterval(() => {
        fetch('/latest-review', {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        })
        .then((response) => response.json())
        .then((result) => {
          console.log(result);
          if (result["reviewText"] != "NULL") {
            const newIndex = result["rNo"]; // Properly declare with const
            const text = result["reviewText"];
            
            // Only display if we haven't shown this index yet
            if (!displayedReviews.has(newIndex)) {
              displayedReviews.add(newIndex);
              if (speed == "MEDIUM") {
                displayReview(newIndex + 1, text, 2000);
              }
              else if (speed == "SLOW") {
                displayReview(newIndex + 1, text, 2000);
              }
              prevIndex = Math.max(prevIndex, newIndex); // Update prevIndex
              
              // Update count display
              document.getElementById('review-count').textContent = displayedReviews.size;
            }
            
            if (displayedReviews.size >= reviewsToScrape) {
              clearInterval(interval1);
            }
          }
        })
        .catch(error => {
          console.error("Error fetching latest review:", error);
          addLog(`Error: ${error.message}`);
        });
      }, 500);
    }
  });

// Function to reset UI state
function resetUI() {
// Reset review popup
popup.style.display = 'none';
popup.classList.remove('fade-in', 'fade-out');

// Reset loading animation
loadingAnimation.style.display = 'none';

// Reset collected reviews
liveReviewsContainer.innerHTML = "";
document.getElementById('review-count').textContent = "0";

// Reset model prediction
document.querySelector("#model-prediction").innerHTML = "";
document.getElementById('sentiment-indicator').style.left = "0%";

// Reset logs (but keep the initial message)
const initialLog = document.querySelector(".logs .log-item:first-child");
document.querySelector(".logs").innerHTML = "";
document.querySelector(".logs").appendChild(initialLog);

// Reset header
document.querySelector('.live-view-header h2').innerHTML = "Live Review Scraping";
document.querySelector('.live-view-header h2').style.fontSize = "30px";

// Reset animation container (keep popup and loading but remove any images)
const animationContainer = document.querySelector('.animation-container');
const popupEl = document.getElementById('review-popup');
const loadingEl = document.getElementById('loading-animation');
animationContainer.innerHTML = '';
animationContainer.appendChild(popupEl);
animationContainer.appendChild(loadingEl);
}

// Helper function to add a collected review without animation
function addCollectedReview(index, text) {
const item = document.createElement('div');
item.className = 'review-item';
item.innerHTML = `
  <div class="review-item-header">
    <span>Review #${index}</span>
  </div>
  <div>${text}</div>
`;

liveReviewsContainer.appendChild(item);

// Update count
document.getElementById('review-count').textContent = index;
}

function displayReview(index, text, POPDELAY) {
    // Set content first
    document.getElementById('review-number').textContent = index;
    document.getElementById('review-content').textContent = text;
    
    // Important: Reset all classes and make sure element is in DOM first
    popup.classList.remove('fade-in', 'fade-out');
    popup.style.display = 'block';
    popup.style.opacity = '0';  // Explicitly set opacity
    
    // Force a browser reflow before adding animation class
    void popup.offsetWidth;
    
    // Start animation after a tiny delay to ensure display:block has taken effect
    setTimeout(() => {
        popup.classList.add('fade-in');
        
        // After a delay, start fade out animation
        setTimeout(() => {
        popup.classList.remove('fade-in');
        void popup.offsetWidth; // Force reflow
        popup.classList.add('fade-out');
        
        // Wait for fade out to complete, then add to collected reviews
        setTimeout(() => {
            // Add to collected reviews with fade-in effect
            const item = document.createElement('div');
            item.className = 'review-item';
            item.innerHTML = `
            <div class="review-item-header">
                <span>Review #${index}</span>
            </div>
            <div>${text}</div>
            `;
            
            // Clear placeholder if it exists
            if (liveReviewsContainer.querySelector('.placeholder')) {
            liveReviewsContainer.innerHTML = '';
            }
            
            liveReviewsContainer.appendChild(item);
            liveReviewsContainer.scrollTop = liveReviewsContainer.scrollHeight;
            
            // Update count
            document.getElementById('review-count').textContent = index;
            
            // Log
            addLog(`Received review #${index}`);
            
            // Hide popup after animation completes
            setTimeout(() => {
            popup.style.display = 'none';
            }, 100);
        }, 450); // Add to container as the popup is finishing its fade out
        }, POPDELAY); // Show the popup for 2 seconds before fading out
    }, 20); // Small delay to ensure display:block has taken effect
}

// Display the ML model results
function displayMLResult(pred) {
  document.querySelector(".results-view h2").style.color="#00f7ff";
  document.querySelector(".sentiment-labels").style.color="white";
  sentiment="YOU CAN BUT IT.";
  if (pred<0.20){
    sentiment="YOU SHOULD NOT BUY IT."
  }
  else if (pred<0.35){
    sentiment="OKAYISH"
  }
  else if (pred>0.55){
    sentiment="YOU CAN DEFINITELY BUY IT."
  }
  document.getElementById('model-prediction').textContent =sentiment;
  document.getElementById('model-prediction').style.fontSize="30px";
  document.getElementById('model-prediction').style.textDecoration="underline";

  document.getElementById('sentiment-indicator').style.left=`${pred*100}%`
  
  // Log
  addLog(`Received model prediction: ${pred}`);
}