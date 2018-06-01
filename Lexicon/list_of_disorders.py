import wikipedia
import csv

# Using Wiki API return list of mental health disorders
p = wikipedia.page("List of mental disorders")

print(p.url)
print(p.title)

s = p.links
l = len(s)
print('list of mental disorders:',s)

with open("list of mental disorders.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for m in s:
      writer.writerow([m])

