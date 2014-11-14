#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree


#Testing 


#Read input arguments
fileName = sys.argv[1]
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

print root.attrib['schema_version']

out = open('output',"a")
for element in root[0].iter():
    for i in element:
        if i.tag == 'sequence':
            genseq = i.text
            break

exons = []
for items in root.iter(tag="transcript"):
    if 'name' in items.attrib.keys():
        if items.attrib['name'] == "t1":
            exons = items.iter('exon')

for exon in exons:
	exonNumber = exon.attrib['label']
#	print exon    
	for coordinates in exon:
		if coordinates.attrib['coord_system'] == 'LRG_1':	
			startIndex = coordinates.attrib['start']
			endIndex = coordinates.attrib['end']
			print 'For exon ', exonNumber, ', the start is ', startIndex, ' and the end is ', endIndex

			exonLength = int(endIndex) - int(startIndex)
			print  '>Exon ',exonNumber, ' | Length : ', exonLength
#print >>fileOut, 








#Check file name is valid/ file is present

#Import file

#Check file contents

#Read transcript as a variable

#Identify a list of exons

#For each exon, find corresponding stuff as string slices
