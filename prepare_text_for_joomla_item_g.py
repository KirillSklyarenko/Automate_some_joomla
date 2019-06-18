#! python3
# prepare text for publication on joomla sute:
# 1. Set tags for every paragraph
# 2. Remove litter (emppty paragraphs, replace double quotes, currency characters)

import pyperclip
import re
import os

# take text copied from a file
tp = pyperclip.paste()

# set tags for lines
lines = ['<strong>'+i+'</strong>' if i.startswith('____') or i.startswith('____') or i.startswith('____')
         else '<h3>'+i+'</h3>' if i.startswith('Chapter ') or i.startswith('Chapters ')
         else '<p style="padding-left: 20px">'+i+'</p>' if re.match(r'^[a-z]', i) or re.match(r'^\([a-z]{1,3}\).*$', i)
         else '<p style="text-align: center">'+i+'</p>' if re.match(r'^\w.*\w$', i) or re.match(r'^\w.*\)$', i)
         else '<p style="padding-left: 20px">'+i+'</p>' if re.match(r'^-', i)
         else '<p>'+i+'</p>'
         for i in tp.split('\r\n')
         ]

t = '\n\n'.join(lines)

# dict of litter to be removed or replaced
d = {'“': '&laquo;', '”': '&raquo;', '<p></p>': '', '\t': '', '<p> </p>': '', '\xa3': '&pound;'}

# replacement of litter
d = dict((re.escape(k), v) for k, v in d.items())
pattern = re.compile("|".join(d.keys()))
t1 = pattern.sub(lambda m: d[re.escape(m.group(0))], t)

# remove text of previous item from the file
file = r'C:\___\___.txt'
with open(file, 'r') as f:
    file_text = f.read().splitlines()
    n = file_text.index('Fulltext')
    file_text[n+1:] = []
    file_text.append(t1)

new = "\n".join(file_text)

# I could not replace fulltext with new one in the file,
# so write text to new file, remove the old one and rename the new one
with open(r'C:\translate\11.txt', 'w+') as ff:
    ff.write(str(new))

os.remove(file)

os.rename(r'C:\translate\11.txt', r'C:\translate\1.txt')
