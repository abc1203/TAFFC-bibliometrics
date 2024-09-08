import os
import bibtexparser
from collections import defaultdict
from itertools import combinations

def parse_bib_file_for_journals(bib_file_path):
    """
    Parse a single .bib file and extract the journals from entries that have a "journal" field.
    """
    with open(bib_file_path, 'r') as bib_file:
        bib_content = bib_file.read()
    
    # Parse the .bib content using bibtexparser
    bib_database = bibtexparser.loads(bib_content)
    
    # Extract journal names
    journals = set()  # Use a set to ensure unique journals per file
    for entry in bib_database.entries:
        if 'journal' in entry:
            journals.add(entry['journal'])
    
    return journals

def process_bib_files_for_connections(directory_path):
    """
    Process all .bib files in the specified directory and record connections between journals.
    """
    journal_connections = defaultdict(int)
    unique_journals = set()
    
    # Iterate over all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.bib'):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing file: {file_path}")
            
            # Parse the .bib file and get the set of journals
            journals = parse_bib_file_for_journals(file_path)
            
            # Add journals to the unique journal set
            unique_journals.update(journals)
            
            # Find all pairs of journals in the same .bib file
            for journal1, journal2 in combinations(journals, 2):
                # Sort the journals alphabetically to avoid duplicate pairs in different order
                journal_pair = tuple(sorted([journal1, journal2]))
                # Add 1 to their connection strength
                journal_connections[journal_pair] += 1
    
    return unique_journals, journal_connections

def save_for_vosviewer(journals, journal_connections):
    """
    Save the journal nodes and connections in the format required by VOSViewer.
    """
    # Save the journals (nodes) into a file
    with open('data/author_publication_map.txt', 'w') as nodes_file:
        nodes_file.write("Id,Label\n")
        for idx, journal in enumerate(journals, 1):
            nodes_file.write(f"{idx},{journal}\n")
    
    # Save the journal connections (edges) into a file
    journal_index_map = {journal: idx + 1 for idx, journal in enumerate(journals)}
    
    with open('data/author_publication_network.txt', 'w') as edges_file:
        edges_file.write("Source,Target,Weight\n")
        for (journal1, journal2), strength in journal_connections.items():
            source = journal_index_map[journal1]
            target = journal_index_map[journal2]
            edges_file.write(f"{source},{target},{strength}\n")

if __name__ == "__main__":
    # Specify the directory containing the .bib files
    bib_directory = 'data/bib'
    
    # Step 1: Process all .bib files and compute the journal connections
    unique_journals, journal_connections = process_bib_files_for_connections(bib_directory)
    
    # Step 2: Save the data in a format required by VOSViewer
    save_for_vosviewer(unique_journals, journal_connections)

    print("VOSViewer files created successfully.")
