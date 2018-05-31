import wikipedia
import csv
import re

# Using Wiki API return list of mental health disorders
p = wikipedia.page("List of antidepressants")


print(p.url)
print(p.title)

# Getting Wikipedia section list of medication

s = p.section('Serotonin–norepinephrine reuptake inhibitors (SNRIs)')
output = s.split('\n')
output2 =[]
a=[]

for line in output:
    k= re.sub('[()]', '', line)
    k1 = k.replace(',', '')
    output2.append(k1)
for words in output2:
    t =words.split()

    for i in range(len(t)):
        a.append(t[i])

with open("List of antidepressants2.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for m in a:
        writer.writerow([m])

