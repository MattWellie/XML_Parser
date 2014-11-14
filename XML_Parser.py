#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import glob
#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Output file name (optional argument)

#Read input file name from arguments
fileName = sys.argv[1]

#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

outputFileString = 'outputFiles/'+ fileName.split('.')[0]+ '-Out.fasta'
print outputFileString
out = open(outputFileString, "w")

#Scan for the optional argument specifying genomic/protein etc (extension)
option = ''
try:
	option = sys.argv[3]
except:
	option = '-g'

#Read in the specified input file into a variable
try:
	tree = etree.parse(fileName)
	root = tree.getroot()
	fixannot = root.find('fixed_annotation')
except IOError as fileNotPresent:
	print "The specified file cannot be located: " + fileNotPresent.filename
	exit()

#Check the version of the file we are opening is correct
assert root.attrib['schema_version'] == '1.8', 'This file is not the correct version'

#Grabs the sequence string from the <sequence/> tagged block
def grab_element(path):
	''' '''
	for item in root.findall(path):
		result = item.text
	return result

#Read through the transcript 
def get_exoncoords(level):
	''' '''
	transcriptdict = {}	
	for items in level.findall('transcript'):
		transcript = items.attrib['name']
		tranexons = []
		for exon in items.iter('exon'):
			for coordinates in exon:
				if coordinates.attrib['coord_system'][-2] not in ['t','p']:
					startIndex = int(coordinates.attrib['start'])
					endIndex = int(coordinates.attrib['end'])
					exonLength = endIndex - startIndex
					tranexons.append((exon.attrib['label'],startIndex, endIndex))
				#can add extra options to grab other sequences
		transcriptdict[transcript] = tranexons
	return transcriptdict

#Uses passed dictionary to populate the output file
def grab_seqslices(exoncoordlist,sequence):
	for coords in exoncoordlist:
		assert coords[1] < coords[2], "Sequence coordinates invalid "
		exonseq = sequence[coords[1]-1:coords[2]]
		print >>out, '>Exon ', coords[0], '| length ', coords[2] - coords[1]
		print >>out, exonseq

#def printtofasta():

#if elif options for which sequences need to be grabbed 
x = grab_element('fixed_annotation/sequence')
td = get_exoncoords(fixannot)
for y in td.keys():
	grab_seqslices(td[y],x)



