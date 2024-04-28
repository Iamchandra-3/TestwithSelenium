import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Set the session name
session_name = 'BrowserStack Assignment'

# The webdriver management will be handled by the browserstack-sdk
# so this will be overridden and tests will run browserstack -
# without any changes to the test files!
options = ChromeOptions()
options.set_capability('sessionName', session_name)
driver = webdriver.Chrome(options=options)

try:
    # Navigate to flipkart.com
    driver.get('https://www.flipkart.com/')
    WebDriverWait(driver, 20).until(EC.title_contains('Online Shopping Site for Mobiles, Electronics, Furniture, Grocery, Lifestyle, Books & More. Best Offers!'))
    
    # Search for the product "Samsung Galaxy S10"
    search_box = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))
    search_box.send_keys('Samsung Galaxy S10')
    search_box.submit()
    
    # Click on "Mobiles" category in search results
    mobiles_category = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/div/section/div[3]/div/a')))
    mobiles_category.click()
    
    # Apply filters (Brand: Samsung, Flipkart assured)
    brand_filter = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[3]/div[2]/div/div/div/label/div[1]')))
    brand_filter.click()
    
    flipkart_assured_filter = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div[1]/div[1]/div/div[1]/div/section[4]/label/div[1]')))
    flipkart_assured_filter.click()
    
    # Select "Price -- High to Low" option
    price_high_to_low_option = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div[2]/div[1]/div/div/div[3]/div[4]')))
    price_high_to_low_option.click()
    
    # Create a list to store product details
    product_list = []
    
    # Iterate through the product boxes and extract details
    for i in range(2, 9):
        product_box_xpath = f'/html/body/div/div/div[3]/div/div[2]/div[{i}]/div/div/div'
        product_name_xpath = f'{product_box_xpath}/a/div[2]/div[1]/div[1]'
        display_price_xpath = f'{product_box_xpath}/a/div[2]/div[2]/div[1]/div[1]/div[1]'
        product_link = driver.find_element(By.XPATH, f'{product_box_xpath}/a').get_attribute('href')
        
        # Retry locating the elements if StaleElementReferenceException occurs
        attempts = 0
        while attempts < 3:
            try:
                product_name = driver.find_element(By.XPATH, product_name_xpath).text
                display_price = driver.find_element(By.XPATH, display_price_xpath).text
                
                product_details = {
                    'Product Name': product_name,
                    'Display Price': display_price,
                    'Link to Product Details Page': product_link
                }
                
                product_list.append(product_details)
                break  # Exit the retry loop if elements are successfully located
            except StaleElementReferenceException:
                attempts += 1
                if attempts == 3:
                    raise  # Raise exception if maximum attempts reached
    
    # Print the list of product details
    for product in product_list:
        print(product)
        print()

    # Set session status as passed
    session_status = 'passed'
    reason = 'Test completed successfully'
    executor_object = {
        'action': 'setSessionStatus',
        'arguments': {
            'status': session_status,
            'reason': reason
        }
    }
    browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
    driver.execute_script(browserstack_executor)

except NoSuchElementException as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except TimeoutException:
    message = 'Timeout Exception: Unable to locate elements within the specified time.'
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
except Exception as err:
    message = 'Exception: ' + str(err.__class__) + str(err.msg)
    driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
finally:
    # Stop the driver
    driver.quit()
