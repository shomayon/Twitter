# Define Data
RESULTS = ['apple','cherry','orange','pineapple','strawberry']

# Open File
resultFyle = open("output1.csv",'w')

# Write data to file
for r in RESULTS:
    resultFyle.write(r + "\n")
resultFyle.close()