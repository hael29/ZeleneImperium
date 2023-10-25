import functions as fc
import gui as g
import time

driver = fc.setup_driver()
driver.get("https://s2.zeleneimperium.cz/main.php?page=garden")
fc.login("mtlapak", "61509fd6", driver)
time.sleep(1)
fc.accept_cookies(driver)

g.create_gui(driver)
