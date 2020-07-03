# CSV2PathwayTools
# Language: Python
# Input: TXT
# Output: NOA
# Tested with: PluMA 1.1, Python 3.6
# Dependency: PythonCyc 1.1, Pathway-Tools database, MetaCyc

Take a CSV file and map all internal metabolites to Pathway Tools identifiers (Karp et al, 2015)

The plugin takes as input a TXT file of tab-delimited keyword-value pairs:
csvfile: CSV file of metabolites
compounddb: Link to compound-links.dat in MetaCyc

The output file will be a simple NOA file (tabular) with metabolite identifiers from the CSV in one column, mapped to their PathwayTools identifier in the second.

