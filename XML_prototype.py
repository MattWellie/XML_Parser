#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree


#Testing 


#Read input arguments
fileName = sys.argv[1]
fileOutTitle = sys.argv[2]
fileOut = open(fileOutTitle, 'w')

try:
	#Optional option, genomic default
	option = sys.argv[3]
except:
	option = '-g'

tree = etree.parse(fileName)
root = tree.getroot()

for f in fileName:
	assert fileName == '*.xml', 'You have the wrong input file'   



#Printing things

#Check file name is valid/ file is present

#Import file

#Check file contents

#Read transcript as a variable

#Identify a list of exons

#For each exon, find corresponding stuff as string slices
