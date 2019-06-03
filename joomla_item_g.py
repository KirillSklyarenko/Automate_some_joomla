#! python3
# joomla_item.py - automate the process of publishing of a joomla item
# chrome edition of script
# prerequisites: k2, jce editor in code mode
# txt file is prepared with header, alias and fulltext of article (no metadata, keyword and tags are provided for in the script)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

sitename = r'https://___.com'

file = r'C:\___\___.txt'

# name of item category in k2 new item window
cat_item = "___"

# name of menu, where the new item is to be placed into
menu_name = "___"

# name of item category in new menu item window (yes, it can be a little different from cat_item)
cat_menu = "___"

# title of item from the txt file
def title():
    with open(file) as f:
        for line in f:
            if 'Header' in line:
                return next(f)

# alias of item from the txt file
def alias():
    with open(file) as f:
        for line in f:
            if 'Alias' in line:
                return next(f)

# fulltext of item from the txt file (with all tags already in text; text is prepared by prepare_text_for_joomla_item 2.py)
def fulltext():
    with open(file) as f:
        file_text = f.read().splitlines()
        n = file_text.index('Fulltext')
        item_text = file_text[n+1:]
    return "".join(item_text)


driver.get(f'{sitename}/administrator/')

passwd = driver.find_element_by_id('mod-login-password')
passwd.send_keys('___')
username = driver.find_element_by_id('mod-login-username')
username.send_keys('___')

button = driver.find_element_by_class_name('btn-group')
button.click()

driver.get(f'{sitename}/administrator/index.php?option=com_k2&view=item')

title_box = driver.find_element_by_id('title')
title_box.send_keys(str(title()))

title_box = driver.find_element_by_id('alias')
title_box.send_keys(str(alias()))

# wanted to try this code of wait and compare to the code of wait for frame blocks
driver.implicitly_wait(10)
driver.find_element_by_class_name('chzn-single').click()
driver.find_element(By.XPATH, '//li[text()="'+cat_item+'"]').click()

driver.implicitly_wait(10)
textarea = driver.find_element_by_class_name('mce_editable')
textarea.send_keys(str(fulltext()))

driver.find_element_by_class_name('button-save').click()

driver.implicitly_wait(10)
driver.get(f'{sitename}/administrator/index.php?option=com_menus&view=item&layout=edit')
driver.find_element_by_id('jform_menutype_chzn').click()
driver.find_element(By.XPATH, '//li[text()="'+menu_name+'"]').click()

jform_title = driver.find_element_by_id('jform_title')
jform_title.send_keys(str(title()))

jform_alias = driver.find_element_by_id('jform_alias')
jform_alias.send_keys(str(alias()))

driver.find_element_by_class_name('btn-primary').click()
frame0 = driver.find_elements_by_tag_name('iframe')
for i in range(0, len(frame0)):
    driver.switch_to.frame(i)
    find_k2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "K2"))
        )
    find_k2.click()
    find_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Item"))
        )
    find_item.click()

driver.find_element_by_class_name('fa-file-text-o').click()
frame1 = driver.find_elements_by_tag_name('iframe')
for i in range(0, len(frame1)):
    driver.switch_to.frame(i)
    select_latest = WebDriverWait(driver, 10).until(
        # all items in the list have this class name, but the new one is always the first one
        EC.element_to_be_clickable((By.CLASS_NAME, "k2ListItemDisabled"))
    )
    select_latest.click()

select_parent_menu = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "jform_parent_id_chzn"))
)
select_parent_menu.click()
driver.find_element(By.XPATH, '//li[text()="'+cat_menu+'"]').click()

# a problem arises after usage of frames on the page: some new div 'k2AlertContainer' obscures all necessary areas; the only way I found to work around this, is to remove it
driver.execute_script("document.getElementById('k2AlertContainer').remove();")

driver.find_element_by_xpath("//button[@onclick=\"Joomla.submitbutton('item.save');\"]").click()
