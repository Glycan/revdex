import re

text = open("kplat.txt").read()

lines = text.split("\n")
pages = re.split("\\n+\d+.*\\n+", text)
for page in pages:
    if 