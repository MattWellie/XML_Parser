import sys
import xml.etree.ElementTree as etree
import glob

assert len(sys.argv) < 1, "Too many arguments!"
print len(sys.argv)

fileName = sys.argv[1]

tree = etree.parse(fileName)
root = tree.getroot()

fixannot = root.find('fixed_annotation')
genename = root.find('updatable_annotation/annotation_set/lrg_locus').text
refseqname = root.find('fixed_annotation/sequence_source').text

print genename
print refseqname
pad = 50 # change later to add padding for genomic sequence
output = open("out","w")

def grab_element(path,root):
	''' '''
	for item in root.findall(path):
		result = item.text
	return result

def get_exoncoords(level,padding,genseq):
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
					seq = genseq[startIndex-1:endIndex]
					if padding > 0:					
						pad5 = genseq[startIndex-padding-1:startIndex]
						pad3 = genseq[endIndex:endIndex+padding+1]
						seq = pad5.lower() + seq + pad3.lower()
					tranexons.append((exon.attrib['label'],startIndex, endIndex,seq))
				#can add extra options to grab other sequences
		transcriptdict[transcript] = tranexons
	return transcriptdict

def print_exons(exoncoordlist,transcript,gene,refseqid,outfile):
	''' '''
	for ex in exoncoordlist:
		header = ">Exon_" + ex[0] + "|" + gene + "|" + refseqid
		print >>outfile, header,"\n",ex[-1]
		

#if elif options for which sequences need to be grabbed 
x = grab_element('fixed_annotation/sequence',root)

td = get_exoncoords(fixannot,pad,x)

for y in td.keys():
	outfilename = "LRG1" + "_" + y
	out = open(outfilename,'w')
	print_exons(td[y],y,genename,refseqname,out)



