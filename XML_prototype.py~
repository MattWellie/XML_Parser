#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import glob
import os

#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Output file name (optional argument)

#Read input file name from arguments
fileName = sys.argv[1]
#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file'   

#Read output file title from arguments
fileOutTitle = sys.argv[2]

##### Check that the file specified does not already exist
existingFiles = os.listdir('/home/swc/XML_Parser')
if fileOutTitle in existingFiles:
	print 'The output file already exists in the present directory'
	print 'Would you like to override the file? y/n'
	userChoice = raw_input('> ')
	if userChoice == 'n':
		exit()
	
#Open the specified file
#fileOut = open(fileOutTitle, 'w')

#try:
	#Optional option, genomic default
	#option = sys.argv[3]
#except:
	#option = '-g'
try:
	tree = etree.parse(fileName)
	root = tree.getroot()
except IOError as fileNotPresent:
	print "The specified file cannot be located: " + fileNotPresent.filename
	exit()

print root.attrib['schema_version']

#fileexist = glob.glob(sys.argv[2])
#if len(fileexist) > 0:
	#WARN about file overwrite

out = open('output',"a")

fixannot = root.find('fixed_annotation')


sequences = []
for element in fixannot.iter():
	if element.tag == 'sequence':
		sequences.append(element.text)
		genseq = max(sequences, key=len)
		protseq = min(sequences,key=len)
		
		

print protseq

exons = []
for items in fixannot.iter(tag="transcript"):
    if 'name' in items.attrib.keys():
        if items.attrib['name'] == "t1":
            exons = items.iter('exon')


for exon in exons:
	exonNumber = exon.attrib['label']
#	print exon    
	for coordinates in exon:
		if coordinates.attrib['coord_system'] == 'LRG_1':
			startIndex = int(coordinates.attrib['start'])
			endIndex = int(coordinates.attrib['end'])
			exonLength = endIndex - startIndex
			print 'For exon ', exonNumber, ', the start is ', startIndex, ' and the end is ', endIndex
			exonLength = int(endIndex) - int(startIndex)
#			print  '>Exon ',exonNumber, ' | Length : ', exonLength
#			print >>fileOut, '>Exon ',exonNumber, ' | Length : ', exonLength



#Import file

#Check file contents

#Read transcript as a variable

#Identify a list of exons

#For each exon, find corresponding stuff as string slices
