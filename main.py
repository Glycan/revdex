import random
words = open("NaNoGenMo2014/words/adj.txt").read().split("\n")
f = open("example.tw",'w')

for i in range(1,4):
    for j in range(1,4):
    
        f.write("""::%s%s
This looks like the sort of %s place where you can go [[%s%s]], [[%s%s]], and [[%s%s]].

""" % (i,j, random.choice(words), i+1,j-1, i-1,j+1, random.randint(0,2), random.randint(0,2))
    )
f.close()