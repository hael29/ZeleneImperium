from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
from crops import crop_class_dict as ccd

def setup_driver():
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver


def login(username, password, driver):
    login_user = driver.find_element("id", "logout_user")
    login_user.click()
    login_user.send_keys(username)
    login_password = driver.find_element("id", "logout_pass")
    login_password.click()
    login_password.send_keys(password)
    login = driver.find_element("id", "submitlogin_logout")
    login.click()


def accept_cookies(driver):
    driver.find_element("class name", "cookiemon-btn-accept").click()


def click_gnome(driver):
    # probably an unnecessarily long way to find the gnome but oh well (it had 2 classes at once.)
    gnome = None
    possible_gnomes = driver.find_elements("class name", "link")
    for possible_gnome in possible_gnomes:
        if possible_gnome.get_attribute('class') == 'link harvest':
            gnome = possible_gnome
            break
    if gnome:
        gnome.click()


# this part is fairly questionable
# clicks the harvest lad, then closes his gui, depending on if any crops were harvested

def close_harvest_gui(driver):
    try:
        close_button = driver.find_element("id", "baseDialogButton")
        close_button.click()
    except:
        close_button = driver.find_element("class name", "closeBtn")
        ac = ActionChains(driver)
        ac.move_to_element(close_button).click().perform()
        print("3")


def harvest(driver):
    click_gnome(driver)
    time.sleep(1)
    close_harvest_gui(driver)


def is_empty(tile_id, driver):
    tile = driver.find_element("id", tile_id)
    tile_html = tile.get_attribute("innerHTML")
    start_index = tile_html.find("produkte") + 9
    end_index = tile_html.find(".gif")
    return tile_html[start_index:end_index] == "0"


def select_crop(crop_name, driver):
    try:
        crop = driver.find_element("class name", ccd[crop_name])
        crop.click()
    except:
        print("crop not found")


def click_empty_tiles(driver):
    for tile_number in range(1, 205):
        tile_id = f'gardenTile{tile_number}'
        if is_empty(tile_id, driver):
            driver.find_element("id", tile_id).click()


def plant(crop_name, driver):
    select_crop(crop_name, driver)
    click_empty_tiles(driver)


def water_crops(driver):
    watering_can = driver.find_element("id", "giessen")
    watering_can.click()
    for tile_number in range(1, 205):
        tile_id = f'gardenTile{tile_number}'
        tile = driver.find_element("id", tile_id)
        if not is_obstacle(tile):
            tile.click()

    driver.find_element("id", "anpflanzen").click()  # deselects watering can at the end.


def is_obstacle(tile):
    obstacles = ['steine', 'unkraut', 'baumstumpf', 'maulwurf']

    tile_html = tile.get_attribute("innerHTML")
    start_index = tile_html.find("produkte") + 9
    end_index = tile_html.find(".gif")
    for obstacle in obstacles:
        if obstacle in tile_html[start_index:end_index]:
            return True

    return False


def get_supported_crops(dict):
    crops = ""
    for crop in dict:
        crops += f'{crop}, '
    return crops[:-2]



