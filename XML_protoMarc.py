import sys
import xml.etree.ElementTree as etree
import glob

fileName = sys.argv[1]
tree = etree.parse(fileName)
root = tree.getroot()
fixannot = root.find('fixed_annotation')

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
		exonNumber = 0	
		tranexons = []
		for exon in items.iter('exon'):
			exonNumber += 1
			for coordinates in exon:
				if coordinates.attrib['coord_system'][-2] not in ['t','p']:
					startIndex = int(coordinates.attrib['start'])
					endIndex = int(coordinates.attrib['end'])
					exonLength = endIndex - startIndex
					print 'For exon ', exonNumber, ', the start is ', startIndex, ' and the end is ', endIndex
				#print >>fileOut, '>Exon ',exonNumber, ' | Length : ', exonLength

#def grab_seqslices():



td = get_exoncoords(fixannot)
#ec = get_coords(td)

#for y in td.keys():
#	print y, ":", td[y]

x = grab_element('fixed_annotation/sequence')
#print x
get_exoncoords(fixannot)
