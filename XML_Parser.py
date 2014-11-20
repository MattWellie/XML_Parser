#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import os
#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Padding length (intronic surrounding exons)
#Read input file name from arguments

fileName = sys.argv[1]

assert len(sys.argv) <4, "Too many arguments!" #check no additional arguments provided on command line

#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

#Scan for the optional argument specifying genomic/protein etc (extension - not used)
#option = ''
#try:
#	option = sys.argv[3]
#except:
#	option = '-g'

#Read in the specified input file into a variable
try:
	tree = etree.parse(fileName)
	root = tree.getroot()
	fixannot = root.find('fixed_annotation') #ensures only exons from the fixed annotation will be taken
	genename = root.find('updatable_annotation/annotation_set/lrg_locus').text
	refseqname = root.find('fixed_annotation/sequence_source').text
except IOError as fileNotPresent:
	print "The specified file cannot be located: " + fileNotPresent.filename
	exit()

try:
	pad = int(sys.argv[2])
except:
	pad = 0
	print "Invalid/No padding provided: Padding defaulting to zero"

assert pad <= 2000, "Padding too large, please use a value below 2000 bases" #LRG files have 2000 additional genomic sequence on 

#Check the version of the file we are opening is correct
if root.attrib['schema_version'] <> '1.8':
	print 'This LRG file is not the correct version for this script'
	print 'This is designed for v.1.8'
	print 'This file is v.' + root.attrib['schema_version']

#Grabs the sequence string from the <sequence/> tagged block
def grab_element(path, root):
	'''Grabs specific element from the xml file from a provided path'''
	try:
		for item in root.findall(path):
			result = item.text
		return result
	except:
		print "No sequence was identified"

#Grab exon coords and sequences from the xml file 
def get_exoncoords(level,padding,genseq):
	'''Traverses the XML eTree to identify all the exons for the sequence
	   Returns a dictionary containing exon numbers, start and finish
	   co-ordinates, and the appropriate chunk of sequence.
	   The dictionary is designed to be passed to a dedicated write function
	   which will print the appropriate sequence elements and identifiers to
	   an output file'''
	transcriptdict = {}	#LRG files can contain more than one transcript in fixed annotation section
	for items in level.findall('transcript'):
		transcript = items.attrib['name']
		tranexons = []
		for exon in items.iter('exon'):
			for coordinates in exon:
				if coordinates.attrib['coord_system'][-2] not in ['t','p']:
					#ensures only genomic coords are taken
					startIndex = int(coordinates.attrib['start'])
					endIndex = int(coordinates.attrib['end'])
					assert startIndex >= 0, "Exon index out of bounds"
					assert endIndex <= len(genseq), "Exon index out of bounds"
					seq = genseq[startIndex-1:endIndex]
					if padding > 0:					
						assert startIndex - pad >= 0, "Exon index out of bounds"
						assert endIndex + pad <= len(genseq), "Exon index out of bounds"
						pad5 = genseq[startIndex-padding-1:startIndex]
						pad3 = genseq[endIndex:endIndex+padding+1]
						seq = pad5.lower() + seq + pad3.lower()
					tranexons.append((exon.attrib['label'],startIndex, endIndex,seq))
				#can add extra elif options to grab other sequence types
		transcriptdict[transcript] = tranexons
	return transcriptdict

def print_exons(exoncoordlist,transcript,gene,refseqid,outfile):
	'''Prints the exon sequences with headers to a fasta file'''
	for ex in exoncoordlist:
		header = ">Exon_" + ex[0] + "|" + gene + "|" + refseqid +'|LengthOfExon:' + str(ex[2]-ex[1])
		print >>outfile, header,"\n",ex[-1]


#if elif options for which sequences need to be grabbed 
x = grab_element('fixed_annotation/sequence',root)
td = get_exoncoords(fixannot,pad,x)
for y in td.keys():
	outputfile = fileName.split('.')[0]+'_'+y+"_"+str(pad)+'_Out.fasta'
	outputFilePath = os.path.join('outputFiles',outputfile)
	existingFiles = os.listdir('outputFiles')
	if outputfile in existingFiles:
		#tests whether file already exists
		print 'The output file already exists in the present directory'
		print 'Would you like to overwrite the file? y/n'
		c = 0
		while c == 0:
	  		userChoice = raw_input('> ')
			if userChoice == 'n':
				print "Program exited without creating file"
				exit() # can change later to offer alternate filename
			elif userChoice == 'y':
				c += 1
			else:
				print "Invalid selection please type y or n"
	out = open(outputFilePath, "w")
	print_exons(td[y],y,genename,refseqname,out)
