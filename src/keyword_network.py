import json
import itertools
from collections import Counter

# Load the JSON data
with open('data/TAFFC_IEEEkeywords.json', 'r') as file:
    data = json.load(file)

# Extract the keywords from each paper
papers_keywords = [item['IEEE Keywords'] for item in data]

# Count co-occurrences of keyword pairs
co_occurrence_counter = Counter()
keyword_counter = Counter()

for keywords in papers_keywords:
    for keyword in keywords:
        keyword_counter[keyword] += 1
    for pair in itertools.combinations(sorted(keywords), 2):
        co_occurrence_counter[pair] += 1

# Create map file content
map_lines = ["id\tlabel\tx\ty\tcluster\tweight<Links>\tweight<Total link strength>\tweight<Documents>"]
keyword_to_index = {}
index = 1

# Assign an index to each keyword and create map entries
for keyword, count in keyword_counter.items():
    if keyword not in keyword_to_index:
        keyword_to_index[keyword] = index
        map_lines.append(f"{index}\t{keyword}\t0\t0\t1\t0\t0\t{count}")
        index += 1

# Save map file
map_file_path = 'data/keyword_co_occurrence_map.txt'
with open(map_file_path, 'w') as file:
    file.write("\n".join(map_lines))

# Create network file content
network_lines = []
for (k1, k2), weight in co_occurrence_counter.items():
    network_lines.append(f"{keyword_to_index[k1]}\t{keyword_to_index[k2]}\t{weight}")

# Save network file
network_file_path = 'data/keyword_co_occurrence_network.txt'
with open(network_file_path, 'w') as file:
    file.write("\n".join(network_lines))

(map_file_path, network_file_path)
