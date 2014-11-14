#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import glob


#Testing 


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
try:
	tree = etree.parse(fileName)
	root = tree.getroot()
except IOError as FileNotPresent:
	print "The specified file cannot be located: " + fileName
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
