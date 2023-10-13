from collections import Counter

with open("text_file.txt") as f:
    print("Number of words in the file :", Counter(f.read().split()))
    
