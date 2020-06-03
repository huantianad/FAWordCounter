from collections import Counter
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np


def count_words(text):
    text = text.lower()
    skips = [".", ",", ":", ";", '"', "!", "?",]
    for ch in skips:
        text = text.replace(ch, "")
    word_count = Counter(text.split(" "))
    return word_count


with open("downloads.txt", "r") as file:
    text = file.read()

counted = count_words(text)

for thing in list(counted):
    if counted[thing] < 100:
        del counted[thing]


print(counted)

keys = []
values = []
items = sorted(counted.items(), key = lambda x: x[1])
for item in items:
    keys.append(item[0]), values.append(item[1])


words = keys
amount = values


y_pos = np.arange(len(words))
plt.figure(figsize=(20,20))
plt.bar(y_pos, amount, align='center', alpha=0.5)
plt.xticks(y_pos, words, rotation=90)
plt.ylabel('Times used')
plt.title('Word count')

plt.show()