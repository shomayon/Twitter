import wikipedia
import csv

# Using Wiki API return list of mental health disorders
p = wikipedia.page("List of antidepressants")
import re

print(p.url)
print(p.title)

# Getting Wikipedia section list of medication

s = p.section('Selective serotonin reuptake inhibitors (SSRIs)')
output = s.split('\n')
output2 =[]
a=[]
del output[6]
for line in output:
  k= re.sub('[()]', '', line)
  k1 = k.replace(',', '')
  output2.append(k1)
for words in output2:
    t =words.split()

    for i in range(len(t)):
       a.append(t[i])

with open("List of antidepressants.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for m in a:
        writer.writerow([m])




