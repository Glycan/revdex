import random, json, re, pdb
"""
words = open("NaNoGenMo2014/words/adj.txt").read().split("\n"); f = open("example.tw",'w')
for i in range(1,4):
    for j in range(1,4): f.write(""::%s%sThis looks like the sort of %s place where you can go [[%s%s]], [[%s%s]], and [[%s%s]]." % (i,j, random.choice(words), i+1,j-1, i-1,j+1, random.randint(0,2), random.randint(0,2)))
f.close()
""""""entries = []
for line in open("index").readlines():
    if line and not line.startswith("INDEX"):
        if line[0].isupper(): entries.append(line)
        else: entries[-1] += " " + line
json.dump(entries, open("dex-entries.json", 'w'))
"""

entries = json.load(open("dex-entries.json"))

topic_pages = {}
bad_entries = []
# Prase index
for entry in entries:
    entry=entry.replace("\n", "").replace("\\n", "")
    try: 
        topic, rest = entry.split(":")
        topic_pages[topic] = []
        if "See" in rest:
            if (". _See also_" in rest):
                rest, see = rest.split(". _See also _")
                see = see.split(";")
                topic_pages[topic].extend(see)
            else:
                rest = rest.split(".")[0]
        parts = rest.split(";")
        for part in parts:
            items = part.split(", ")
            if items[0][0].isalpha() or items[0][1].isalpha():
                subtopic = ""
                num = ""
                for char in items[0]:
                    if char.isalpha() or char in " -":
                        subtopic += char
                    else:
                        break
                items.pop(0)
            while items:
                item = items.pop()
                if "," in item:
                    item, *rest = item.split(",")
                    items.extend(rest)
                item = item.replace("_", "")
                if item.startswith(" "): 
                    item = item[1:]
                if "-" in item:
                    start, stop = item.split("-")
                    #if start.isalpha() or stop.isalpha():
                    topic_pages[topic].extend([start,stop])
                    #else:
                    #    diff = len(start) - len(stop)
                    #    stop = start[:diff] +stop
                    #    topic_pages[topic].extend(range(int(start), int(stop)))
                else:
                    if "n." in item:
                        #page, note = item.split(" n. ")
                        item=item.split()[0]
                    topic_pages[topic].append(item)
    except ValueError:
        bad_entries.append(entry)
        continue
        
pages = json.load(open("kplat.json"))


class Chunk:
    def __init__(self, id, contents, parent=None, links=None):
        self.id = id
        self.contents = contents
        self.links = links if links else {}
        self.spacer = "\n\n"
        self.meta = {}
        if parent:
            try:
                parent.add(self)
            except AttributeError:
                pass
        
    def get_contents(self):
        try:
            return self.contents.render()
        except AttributeError:
            try:
                return self.spacer.join([
                    content.render() for content in self.contents
                ])
            except AttributeError:
                return self.contents
                
    def twee_render(self):
        output = "::" + str(self.id) + "\n"
        if "prev" in self.links:
            output += "\n[[previous page->%s]]\n\n" % self.links.pop("prev")
        output += self.get_contents()
        if "next" in self.links:
            output += "\n\n\n[[next page->%s]]\n\n" % self.links.pop("next")
        output += "\n\n".join(["[[%s->%s]]" % (link,target) for link, target in self.links.items()])
        return output
        
class Book(Chunk):
    def add(self, content):
        if type(content) == Page:
            if self.contents:
                content.links["prev"] = self.contents[-1].id
                self.contents[-1].links["next"] = content.id
            self.contents.append(content)
        else:
            self.meta[content.id] = content.id
    
    def lookup(self, id):
        try:
            page_no = int(id)
            return self.contents[page_no]
        except(IndexError, ValueError):
            return self.meta[id]
    
    def twee_render(self):
        return "\n".join([content.twee_render() for content in self.contents])
        
class Page(Chunk):
    pass            
            
class Meta(Chunk):
    pass

kplat = Book("A Thousand Plateaus", [])

for no, page in enumerate(pages[22:]):
    if "BookZZ" in page:
        page = page[94:]
    Page(no, page, parent=kplat)

for topic, links in topic_pages.items():
    if len(links) > 1:
        Meta(topic, topic + ":\n", parent=kplat, links={page:page for page in links})
        for page in links:
            try:
                kplat.lookup(page).links[topic] = topic
            except KeyError:
                print("bad topic, page:", topic, ",", page)
                 
with open("kplat.twee", 'w') as f:
    f.write(kplat.twee_render())
        