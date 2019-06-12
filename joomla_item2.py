#! python3

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

wait_time = 20

sitename = r'https://___.com'

file = r'C:\___'

cat_item = "___"

menu_name = "___"

cat_menu = "___"

with open(file) as f:
    file_text = f.read().splitlines()
    n = file_text.index('Header')
    title = file_text[n+1]
    n1 = file_text.index('Alias')
    alias = file_text[n1+1]
    n2 = file_text.index('Fulltext')
#    fulltext = "".join(file_text[n2+1:])
    fulltext_c = pyperclip.copy("\n".join(file_text[n2 + 1:]))

driver.get(f'{sitename}/administrator/')

passwd = driver.find_element_by_id('mod-login-password')
passwd.send_keys('___[')
username = driver.find_element_by_id('mod-login-username')
username.send_keys('___')

button = driver.find_element_by_class_name('btn-group')
button.click()

driver.get(f'{sitename}/administrator/index.php?option=com_k2&view=item')

title_box = driver.find_element_by_id('title')
title_box.send_keys(title)

title_box = driver.find_element_by_id('alias')
title_box.send_keys(alias)

driver.implicitly_wait(wait_time)
driver.find_element_by_class_name('chzn-single').click()
driver.find_element(By.XPATH, '//li[text()="'+cat_item+'"]').click()

driver.implicitly_wait(wait_time)
textarea = driver.find_element_by_class_name('mce_editable')
# textarea.send_keys(fulltext)
textarea.send_keys(Keys.CONTROL, 'v')

driver.find_element_by_class_name('button-save').click()

driver.implicitly_wait(wait_time)
driver.get(f'{sitename}/administrator/index.php?option=com_menus&view=item&layout=edit')
driver.find_element_by_id('jform_menutype_chzn').click()
driver.find_element(By.XPATH, '//li[text()="'+menu_name+'"]').click()

jform_title = driver.find_element_by_id('jform_title')
jform_title.send_keys(title)

jform_alias = driver.find_element_by_id('jform_alias')
jform_alias.send_keys(alias)

driver.find_element_by_class_name('btn-primary').click()
frame0 = driver.find_elements_by_tag_name('iframe')
for i in range(0, len(frame0)):
    driver.switch_to.frame(i)
    find_k2 = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "K2"))
        )
    find_k2.click()
    find_item = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Item"))
        )
    find_item.click()

driver.find_element_by_class_name('fa-file-text-o').click()
frame1 = driver.find_elements_by_tag_name('iframe')
for i in range(0, len(frame1)):
    driver.switch_to.frame(i)
    select_latest = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "k2ListItemDisabled"))
    )
    select_latest.click()

select_parent_menu = WebDriverWait(driver, wait_time).until(
    EC.element_to_be_clickable((By.ID, "jform_parent_id_chzn"))
)
select_parent_menu.click()
driver.find_element(By.XPATH, '//li[text()="'+cat_menu+'"]').click()

driver.execute_script("document.getElementById('k2AlertContainer').remove();")

driver.find_element_by_xpath("//button[@onclick=\"Joomla.submitbutton('item.save');\"]").click()
