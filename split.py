import re

f = open("kplat.html").read()
pages = re.split("<!-- Page \d+ -->", f)

assert len(pages) > 400
print(len(pages))
import json, html2text

pag=[html2text.html2text(page) for page in pages]
json.dump(pag, open("kplat.json", 'w'))