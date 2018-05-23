import wikipedia
import csv

# Using Wiki API return list of mental health disorders
p = wikipedia.page("List of antidepressants")

print(p.url)
print(p.title)

s = p.links
l = len(s)
print('List of antidepressants:',s)

with open("List of antidepressants.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for m in s:
        writer.writerow([m])

