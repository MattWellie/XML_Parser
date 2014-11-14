import sys
import xml.etree.ElementTree as etree
import glob

fileName = sys.argv[1]
tree = etree.parse(fileName)
root = tree.getroot()
fixannot = root.find('fixed_annotation')

output = open("out","w")

def grab_element(path):
	''' '''
	for item in root.findall(path):
		result = item.text
	return result

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

def grab_seqslices(exoncoordlist,sequence):
	for coords in exoncoordlist:
		exonseq = sequence[coords[1]-1:coords[2]]
		print >>output, coords[0], exonseq

#def printtofasta():

#if elif options for which sequences need to be grabbed 
x = grab_element('fixed_annotation/sequence')
td = get_exoncoords(fixannot)
for y in td.keys():
	grab_seqslices(td[y],x)



