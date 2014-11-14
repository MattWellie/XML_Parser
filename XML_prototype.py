#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import glob
import re
import os

#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Output file name (optional argument)

#Read input file name from arguments
fileName = sys.argv[1]

#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

#Scan for the optional argument specifying genomic/protein etc (extension)
#try:
	#option = sys.argv[3]
#except:
	#option = '-g'

#Read in the specified input file into a variable
try:
	tree = etree.parse(fileName)
	root = tree.getroot()
except IOError as fileNotPresent:
	print "The specified file cannot be located: " + fileNotPresent.filename
	exit()

#Check the version of the file we are openeing is correct
assert root.attrib['schema_version'] == '1.8', 'This file is not the correct version'

#Read output file title from arguments
fileOutTitle = sys.argv[2]

#Check that the specified output file does not already exist
#List all files in present directory
existingOutputFiles = os.listdir('/home/swc/XML_Parser/outputFiles')


if fileOutTitle in existingFiles:
	print 'The output file already exists in the present directory'
	print 'Would you like to override the file? y/n'
	userChoice = raw_input('> ')
	if userChoice == 'n':
		exit()


#Open the specified output file
#fileOutPath = '/home/swc/XML_Parser/outputFiles'
#fileOut = open(fileOutPath, 'w')


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
			exonLength = int(endIndex) - int(startIndex)





#Read transcript as a variable

#Identify a list of exons

#For each exon, find corresponding stuff as string slices
