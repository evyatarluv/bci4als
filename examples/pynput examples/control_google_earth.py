import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

from pynput.keyboard import Key, Controller

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument(r"user-data-dir=C:\Users\noam\AppData\Local\Temp\scoped_dir26260_1359799219\Default")

print("Loading Browser")
browser = webdriver.Chrome(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
                           options=options)
# browser.implicitly_wait(10)
print("Loading Avi's Auto Repair Shop")
url = r'https://earth.google.com/web/search/%d7%9e%d7%95%d7%a1%d7%9a+%d7%90%d7%91%d7%99-%d7%93%d7%9f+2000+%d7%91%d7%a2%22%d7%9e,+Sorek+Street,+Be%27er+Sheva/@31.2247942,34.81324266,283.98703003a,0d,60y,190.93940552h,95.17478397t,0r/data=CqcBGn0SdwolMHgxNTAyNjYyYjkzN2E2ZjEzOjB4MTdmZjc3YWQ1MWE1YTcxNhlc3sH0Yjk_QCFajkb0IWhBQCo8157Xldeh15og15DXkdeZLdeT158gMjAwMCDXkdeiIteeLCBTb3JlayBTdHJlZXQsIEJlJ2VyIFNoZXZhGAEgASImCiQJ3OMoc5tGP0AR3hCKaZ1EP0AZQtIz6xpiQUAhyzTmmG1hQUAiGgoWeU9tVnpZQnNTLUhTNG9jemtaMUhvZxAC'
url = r'https://www.google.com/maps/@30.624906,34.8271508,3a,75y,291.9h,89.66t/data=!3m6!1e1!3m4!1slAyOvjLlHutpFrBl1fGQgg!2e0!7i13312!8i6656'
browser.get(url)

# browser.implicitly_wait(35)
# switch to main window
browser.switch_to.frame(browser.find_element_by_xpath(r'//*[@id="splash-screen-frame"]'))

# start controlling with pynput
time.sleep(25)
print("now here")
print("pressing buttons")
keyboard = Controller()
with keyboard.pressed(Key.shift):
    with keyboard.pressed(Key.up):
        time.sleep(4)
print("finished pressing buttons")
#
#
#
# mouse = Controller()
#
# # Read pointer position
# print('The current pointer position is {0}'.format(
#     mouse.position))
#
# # Set pointer position
# mouse.position = (10, 20)
# print('Now we have moved it to {0}'.format(
#     mouse.position))
#
# # Move pointer relative to current position
# mouse.move(5, -5)
#
# # Press and release
# mouse.press(Button.left)
# mouse.release(Button.left)
#
# # Double click; this is different from pressing and releasing
# # twice on macOS
# mouse.click(Button.left, 2)
#
# # Scroll two steps down
# mouse.scroll(0, 2)
