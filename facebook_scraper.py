from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
import requests
import os
import time

idx = 0

def download_image(image_url):
    folder_path = 'downloaded_images'
    os.makedirs(folder_path, exist_ok=True)
    response = requests.get(image_url)
    if response.status_code == 200:
        global idx
        idx += 1
        with open(os.path.join(folder_path, f'image_{idx}.jpg'), 'wb') as file:
            file.write(response.content)

def scroll_into_view(driver, element):
    """Scroll element into view and center it"""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)



def click_and_download_images(driver, post):
    # click on the first image in the post with class "xz74otr x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"
    # filter from the post element
    try:
        image = post.find_element(By.CSS_SELECTOR, "img.xz74otr.x1ey2m1c.xds687c.x5yr21d.x10l6tqk.x17qophe.x13vifvy.xh8yej3")
    except Exception as e:
        print(e)
        return
    # scroll into view
    scroll_into_view(driver, image)
    for tries in range(3):
        try:
            image.click()
            # wait for the image css selector data-visualcompletion="media-vc-image"
            full_image = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[data-visualcompletion='media-vc-image']")))
            break
        except StaleElementReferenceException:
            return
        except TimeoutException as e:
            pass
        except ElementNotInteractableException as e:
            break
        except ElementClickInterceptedException as e:
            return
        return
    image_urls = []
    while True:
        # wait for the image css selector data-visualcompletion="media-vc-image"
        try:
            full_image = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[data-visualcompletion='media-vc-image']")))
            full_image_src = full_image.get_attribute('src')
            if full_image_src in image_urls:
                break
            image_urls.append(full_image_src)
        except StaleElementReferenceException:
            break
        except TimeoutException as e:
            break
        download_image(full_image_src)
        # click the next button <div aria-label="Next photo"
        try:
            next_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Next photo']")))
            next_button.click()
        except TimeoutException:
            break
        except ElementNotInteractableException:
            break
        except Exception:
            break

    # click the close button <div aria-label="Close"
    while True:
        try:
            close_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close']")))
            close_button.click()
            WebDriverWait(driver, 1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[aria-label='Close']")))
            break
        except TimeoutException as e:
            print(e)
            pass
    
                                     
    

def scrape_images(driver):
    idx = 0
    while True:
        idx += 1
        # post xpath is /html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[2]
        for tries in range(5):
            try:
                xpath_post = f"/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[2]/div/div[{idx}]"
                post = driver.find_element(By.XPATH, xpath_post)
                scroll_into_view(driver, post)
                click_and_download_images(driver, post)
                break
            except NoSuchElementException:
                # click the close button <div aria-label="Close"
                try:
                    close_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close']")))
                    close_button.click()
                    WebDriverWait(driver, 1).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[aria-label='Close']")))
                except Exception as e:
                    pass
                time.sleep(1)
                pass
            except StaleElementReferenceException:
                time.sleep(1)
                pass

def main():
    # options
    chrome_options = webdriver.ChromeOptions()
    # mute
    chrome_options.add_argument("--mute-audio")
    # headless
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the Chrome settings page
    driver.get('chrome://settings/')
    # Execute JavaScript code to set the default zoom level
    # driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.5);')
    
    try:
        # url = 'https://www.facebook.com/OCS.SAFTI/'
        url = 'https://www.facebook.com/SCS.SAFTI'
        # url = 'https://www.facebook.com/oursingaporearmy/'
        # url = 'https://www.facebook.com/OurSCDF/'
        # url = 'https://www.facebook.com/BMTCSAF/'
        driver.get(url)

        # click on the element
        WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Close'][role='button']"))
        ).click()

        scrape_images(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
