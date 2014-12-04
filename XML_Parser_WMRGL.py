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
prot_path = 'fixed_annotation/transcript/coding_region/translation'
prot_transcript = ''
DNA_transcript = ''
fileName = sys.argv[1]

assert len(sys.argv) <=4, "Too many arguments!" #check no additional arguments provided on command line

#Check file name is valid .xml
assert fileName[-4:] == '.xml', 'You have the wrong input file' 

#Scan for the optional argument specifying genomic/protein etc.
#If option is not identified, use genomic only
option = ''
try:
	option = sys.argv[3]
except:
	option = '-g'


print 'option: ', option


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
		DNA_transcript = items.attrib['name']
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
		transcriptdict[DNA_transcript] = tranexons
	return transcriptdict


#03/12/2014 at request of WMRGL
def get_protein_exons(prot_level, exon_level, root):
    proteindict = {} #to contain exons from protein sequence
    for item in root.findall(prot_level):
        try:
            prot_block = item.find("sequence")
            protein_seq = prot_block.text
            #print protein_seq    
            prot_transcript = item.attrib['name']
            #print transcript
        except:
            print "No protein sequence was found"   
        protexons = []
        #print 'for exon in...'
        for exon_item in root.findall(exon_level):
            for exon in exon_item.iter('exon'):
                #print 'for coord in exon'
                for coordinates in exon: 
                    #print 'if...'
                    if coordinates.attrib['coord_system'][-2:] == prot_transcript:
                        start_index = int(coordinates.attrib['start'])
                        end_index = int(coordinates.attrib['end'])
                        assert start_index >= 0, "Exon index out of bounds"
                        assert end_index <= len(protein_seq), "Exon index out of bounds"
                        seq = protein_seq[start_index-1:end_index]
                        protexons.append((exon.attrib['label'], start_index, end_index,seq))
        proteindict[prot_transcript] = protexons
    return proteindict


def print_exons(exoncoordlist,transcript,gene,refseqid,outfile):
	'''Prints the exon sequences with headers to a fasta file'''
	for ex in exoncoordlist:
		header = ">Exon_" + ex[0] + "|" + gene + "|" + refseqid +'|LengthOfExon:' + str(ex[2]-ex[1]) + "|StartPos:"+str(ex[1]) + "|EndPos:"+str(ex[2])
		print >>outfile, header,"\n",ex[-1]


def print_both(prot_list, exon_list,gene,refseqid,outfile):
    '''Prints the file header, DNA seq, and protein seq for each exon.
       Not strictly FastA, but required for WMRGL'''
    for exon in range(len(prot_list)):
        DNA_exon = exon_list[exon]
        PROT_exon = prot_list[exon]
        header = ">Exon_" + DNA_exon[0] + "|" + gene + "|" + refseqid +'|LengthOfDNA:' + str((DNA_exon[2]+1)-DNA_exon[1])+'|LengthOfProt:' + str((PROT_exon[2]+1)-PROT_exon[1]) + "|DNA_StartPos:"+str(DNA_exon[1]) + "|DNA_EndPos:"+str(DNA_exon[2])+"|PROT_StartPos:"+str(PROT_exon[1]) + "|PROT_EndPos:"+str(PROT_exon[2])
        print >>outfile, header
        print >>outfile, DNA_exon[-1]
        print >>outfile, PROT_exon[-1]
       
#if elif options for which sequences need to be grabbed 
if option == '-g':
    x = grab_element('fixed_annotation/sequence', root)
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

elif option == '-p':
    dnaSeq = grab_element('fixed_annotation/sequence', root)
    pd = get_protein_exons(prot_path, 'fixed_annotation/transcript', root)
    for y in pd.keys():
        outputfile = fileName.split('.')[0]+'_'+y+"_"+'_Prot_Out.fasta'
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
        print_exons(pd[y],y,genename,refseqname,out)

else:
    dnaSeq = grab_element('fixed_annotation/sequence', root)
    td = get_exoncoords(fixannot,pad,dnaSeq)
    pd = get_protein_exons(prot_path, 'fixed_annotation/transcript', root)
    assert len(pd) == len(td), "The number of transcripts are different, please check file"
    for entry in range(len(td)):
        y = td[td.keys()[entry]]
        p = pd[pd.keys()[entry]]
        #print p
        assert len(y) == len(p), "The number of exons are different, please check file"
        outputfile = str(fileName.split('.')[0])+'_DNA'+DNA_transcript+"-Prot"+prot_transcript+"_"+str(pad)+'intronic_DNA_PROT_Out.fasta'
        print outputfile
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
        print_both(p,y,genename,refseqname,out)
