import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. URLs and download folder
LOGIN_URL     = "https://2minutetabletop.com/my-account/"
DOWNLOADS_URL = "https://2minutetabletop.com/my-account/downloads/"
DOWNLOAD_DIR  = os.path.abspath("downloads")

# 2. Prepare download directory
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 3. Chrome options to auto-download without prompt
chrome_opts = Options()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_opts.add_experimental_option("prefs", prefs)
# chrome_opts.add_argument("--headless")  # Uncomment to run headless

driver = webdriver.Chrome(options=chrome_opts)
wait   = WebDriverWait(driver, 300)  # up to 5 minutes for manual login

try:
    # 4. Open the login page and wait for you to log in manually
    driver.get(LOGIN_URL)
    print("Please log in manually in the opened browser window.")
    
    # 5. Wait until the “Downloads” link appears (indicating a successful login)
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Downloads")))
    print("Login detected. Navigating to Downloads page…")
    
    # 6. Go to Downloads section
    driver.get(DOWNLOADS_URL)
    wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//a[normalize-space(text())='Master ZIP']")
    ))
    
    # 7. Helper: wait for a new file without .crdownload
    def wait_for_new_file(before_set, timeout=120):
        deadline = time.time() + timeout
        while time.time() < deadline:
            current = set(os.listdir(DOWNLOAD_DIR))
            new = current - before_set
            if new and all(not f.endswith(".crdownload") for f in current):
                return new.pop()
            time.sleep(1)
        raise TimeoutError("Download did not complete within timeout.")
    
    # 8. Find and download each Master ZIP link
    links = driver.find_elements(By.XPATH, "//a[normalize-space(text())='Master ZIP']")
    total = len(links)
    print(f"Found {total} Master ZIP link{'s' if total!=1 else ''}. Starting downloads…")
    
    for idx in range(total):
        # re-fetch to avoid stale elements
        links = driver.find_elements(By.XPATH, "//a[normalize-space(text())='Master ZIP']")
        before = set(os.listdir(DOWNLOAD_DIR))
        
        print(f"[{idx+1}/{total}] Clicking link…")
        links[idx].click()
        
        filename = wait_for_new_file(before)
        print(f" → Downloaded: {filename}")
    
    print("All downloads complete!")
    
finally:
    driver.quit()
