#analyzing tweets

import pandas as pd
import matplotlib.pyplot as plt

tweets = pd.read_csv("tweets.csv")
tweets.head()

def get_candidate(row):
    candidates = []
    text = row["text"].lower()
    if "clinton" in text or "hillary" in text:
        candidates.append("clinton")
    if "trump" in text or "donald" in text:
        candidates.append("trump")
    if "sanders" in text or "bernie" in text:
        candidates.append("sanders")
    return ",".join(candidates)
tweets["candidate"] = tweets.apply(get_candidate, axis=1)
counts = tweets["candidate"]. value_counts()
print(counts)
plt.bar(range(len(counts)),counts)
plt.show()

