import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import ezgmail


#recipient of email
to = "wbrhyne@gmail.com"
#subject of email
subject = "CHECK THE WAVES MAN"
# body of email
body = " is looking good for surfing go check it"




def scrape_surfline(url):
  firefox_options = Options()
  firefox_options.add_argument("--headless")

  service = Service(GeckoDriverManager().install())
  driver = webdriver.Firefox(service=service, options=firefox_options)

  try:
    driver.get(url)

    # Wait for 3 seconds for the website to load
    time.sleep(3)

    # Get the title of the website
    title = driver.title 

    # Find all the h4 elements on the page (wave height data is stored in h4 elements)
    h4_elements = driver.find_elements(By.TAG_NAME, "h4")

    # Extract the text from each h4 element and store them in a list
    h4_texts = [element.text for element in h4_elements]

    #EXTRACT title
    print(title)
    # Filter the h4_texts list to only include text that includes "ft" - wave heights
    wave_heights = [text for text in h4_texts if "ft" in text]
    waves = []
    finalwaves = []
    for wave_height in wave_heights:
      waves.append(wave_height.split("-"))

    for wave in waves:
      finalwaves.append(wave[1].replace("ft", ""))

    finalwaves = [int(wave) for wave in finalwaves]

    return finalwaves, title

  finally:
    driver.quit()

def sendEmail(to, subject, body):
    #adding this here since now I have the title to add to the body
    body = title + body
    ezgmail.send(to, subject, body)
    print(f"Email sent to {to}")





# scrape surfline
url = "https://www.surfline.com/surf-report/61st-street/5842041f4e65fad6a7708b8c?view=table"
finalwaves, title = scrape_surfline(url)
print(finalwaves, title)
#checking to see if the values are equal to or greater than 3ft
# Checking if any waves worth surfing, 3ft haha
surf_flag = 0
for wave in finalwaves:
  if wave >= 3:
    surf_flag = 1
    break
else:
  surf_flag = 0
  
if surf_flag == 1:
  print("GET YOUR SURFBOARD and I'm sending an email")
  ezgmail.send(to, subject, body)
  print("email sent")

  
elif surf_flag == 0:
  print("staying home")
  
