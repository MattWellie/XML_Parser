#Program to import a specified LRG file and export corresponding fasta
import sys
import xml.etree.ElementTree as etree
import os
#Read input arguments - should be
# [0] - program name
# [1] - Input XML file name
# [2] - Padding length (intronic surrounding exons)
# [3] - "-g" for genomic sequence, "-p" for protein
#Read input file name from arguments

fileName = sys.argv[1]

assert len(sys.argv) <= 4, "Too many arguments!" #check no additional arguments provided on command line

#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

#Scan for the optional argument specifying genomic/protein etc.
#If option is not identified, use genomic only
option = ''
try:
	option = sys.argv[3]
except:
	option = '-g'

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

#Padding option only needs to be specified for genomic sequence
#Choice should be possible for genomic AND protein (ref sequences)
if option in ['-g', '-gp', '-pg']:
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

	'''Grabs specific element from the xml file from a provided path'''
path = 'fixed_annotation/sequence'
try:
    for item in root.findall(path):
        result = item.text
        print "DNA: ", result
        
except:
    print "No sequence was identified"
    

#03/12/2014 at request of WMRGL
for item in root.findall('fixed_annotation/transcript/coding_region/translation'):
    try:
        prot_block = item.find("sequence")
        protein_seq = prot_block.text
        print protein_seq
    except:
        print "No protein sequence was found"   
    transcript = item.attrib['name']
    print transcript

##if elif options for which sequences need to be grabbed 
# if option == '-g':
    # x = grab_element(, root)
    # td = get_exoncoords(fixannot,pad,x)
# elif option == '-p':
    # dnaSeq = grab_element('fixed_annotation/sequence', root)
    # td = get_exoncoords(fixannot,pad,x)
    # pd = get_proteincoords(
# for y in td.keys():
	# outputfile = fileName.split('.')[0]+'_'+y+"_"+str(pad)+'_Out.fasta'
	# outputFilePath = os.path.join('outputFiles',outputfile)
	# existingFiles = os.listdir('outputFiles')
	# if outputfile in existingFiles:
		#tests whether file already exists
		# print 'The output file already exists in the present directory'
		# print 'Would you like to overwrite the file? y/n'
		# c = 0
		# while c == 0:
	  		# userChoice = raw_input('> ')
			# if userChoice == 'n':
				# print "Program exited without creating file"
				# exit() # can change later to offer alternate filename
			# elif userChoice == 'y':
				# c += 1
			# else:
				# print "Invalid selection please type y or n"
	# out = open(outputFilePath, "w")
	# print_exons(td[y],y,genename,refseqname,out)
