from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# This will download and install the correct ChromeDriver for your OS and Chrome version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com")
print("✅ Chrome opened successfully")
driver.quit()
