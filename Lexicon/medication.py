import wikipedia
import csv
import re

# Using Wiki API return list of mental health disorders
p = wikipedia.page("List of antidepressants")


print(p.url)
print(p.title)


sections = ['Selective serotonin reuptake inhibitors (SSRIs)',
            'Serotonin–norepinephrine reuptake inhibitors (SNRIs)','Serotonin modulators and stimulators (SMS)',
            'Serotonin antagonists and reuptake inhibitors (SARIs)',
            'Norepinephrine reuptake inhibitors (NRIs)','Tricyclic antidepressants (TCAs)',
            'Tetracyclic antidepressants (TeCAs)']

drugs =[]
sep = '-'

for section in sections:
    s = p.section(section)
    output = s.split('\n')
    for line in output:
        if line[-1] == '.':
            continue
        if sep in line:
            continue
        k= re.sub('[()]', '', line)
        k1 = k.replace(',', '')
        drugs.append(k1)


with open("List of antidepressants.csv",'w') as f:
    writer = csv.writer(f, dialect='excel')
    for line in drugs:
        for m in line.split():
            writer.writerow([m])