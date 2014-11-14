#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import glob
import re

#Read input arguments
fileName = sys.argv[1]
#Check file name is valid/ file is present
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

  
#fileOutTitle = sys.argv[2]
#fileOut = open(fileOutTitle, 'w')

#try:
	#Optional option, genomic default
	#option = sys.argv[3]
#except:
	#option = '-g'

tree = etree.parse(fileName)
root = tree.getroot()
#fileexist = glob.glob(sys.argv[2])
#if len(fileexist) > 0:
	#WARN about file overwrite

#Check the version of the file we are openeing is correct
assert root.attrib['schema_version'] == '1.8', 'This file is not the correct version'

out = open('output',"a")

fixannot = root.find('fixed_annotation')


sequences = []
for element in fixannot.iter():
	if element.tag == 'sequence':
		sequences.append(element.text)
		genseq = max(sequences, key=len)
		protseq = min(sequences,key=len)
		

nucleotides = ['A','T','C','G']

for l in genseq:
	if l not in nucleotides:
		print "this is not the genomic sequence"
		exit()
		

print protseq

exons = []
for items in fixannot.iter(tag="transcript"):
    if 'name' in items.attrib.keys():
        if items.attrib['name'] == "t1":
            exons = items.iter('exon')

##REGEX
'''regex = re.compile('LRG_*')
for exon in exons:
	for coordinates in exon:
		print coordinates.attrib['coord_system']
		if re.match(regex, coordinates.attrib['coord_system']):
			print  coordinates.attrib['coord_system']'''


for exon in exons:
	exonNumber = exon.attrib['label']  
	for coordinates in exon:
		if coordinates.attrib['coord_system'][-2] not in ['t','p']:
			print coordinates.attrib['coord_system']
			startIndex = int(coordinates.attrib['start'])
			endIndex = int(coordinates.attrib['end'])
			exonLength = endIndex - startIndex
			print 'For exon ', exonNumber, ', the start is ', startIndex, ' and the end is ', endIndex
			print >>fileOut, '>Exon ',exonNumber, ' | Length : ', exonLength



#Import file

#Check file contents

#Read transcript as a variable

#Identify a list of exons

#For each exon, find corresponding stuff as string slices
