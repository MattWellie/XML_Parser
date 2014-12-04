## This project is to create an XML parser in Python capable of reading an LRG file
* **Goal: LRG IN; FASTA OUT**

### GUIDE:
- To run this program, open a command line terminal and navigate to the directory containing this program (XML_Parser.py) and desired LRG files. 
- Enter:    "python XML_Parser.py **LRG_FILE_TITLE INTRONIC_PADDING_LENGTH SEQ_TYPE**"
	- **LRG_FILE_TITLE** is an LRG format file ending in ".xml"
	- **INTRONIC_PADDING_LENGTH** is a number between 0 and 2000, specifying the length of intronic flanking sequence around the printed exons
		- As a default, flanking sequences are lower case, and exonic sequence is capitalized
	- **SEQ_TYPE** is an option:
		- *-g* to print only genomic values
		- *-p* to print only protein values
		- *-pg* or *-gp* to print both; genomic printed first
- This will run the program and create a new folder (if it does not already exist) called "outputFiles"
	- The file will be created in Unix, Windows will require the file to be created by User	
- If a file in the specified folder already exists, the program will report this at the command line and ask for a confirmation to continue
- To be duplicated a file will have to have been created with the same input and flanking length

### Input:
1) Pass file title to program as a string argument (CMD line)

2) Optional argument to specify intronic sequence length around exons

3) Pass optional command to specify genomic, cDNA, protein; defaults to genomic

4) Program creates an output file based on the sequences used
	
### Method:
	Command line arguments are supplied to specify the input file and specific parameters
	The appropriate sequence is read into a dictionary (multiple sequences where appropriate)
	Tree iteration is used to find the coordinate details for all exons
	The name of the output file is created using the input file title (LRG #)
	Using the coordinates and specific sequence type, the specific portions of sequence corresponding to each
		exon are output into a output file
	The presence of an existing file of the same title is checked
		If a file already exists, the user is prompted to overwrite (Y/N)
			If the user chooses to overwrite, the program continues
			If the user chooses not to, the program exits and reports that no output was created
	
	
### Output:
- FastA file format
- Each exon is indvidually identified and paired with corresponding sequence (DNA/Protein/Both)
- The description line identifies the exon number and transcript, so each can be used in isolation.
	- This line also contains the length of the exon for quality control checking, and reference sequence creation
	- 
- Output file name was created using:
	* the title of the input file
	* the amount of flanking intron requested
	* the transcript name (to prevent overwriting in the case of multiple transcripts)
	** An OS test is used to determine if a file with the specified name already exists, if so the user is prompted to continue or exit.
	** This meant that only a file which would be the exact duplicate of an existing file (all parameters same) would be capable of replacing the current version


### Testing:
1) Correct performance of this program was confirmed by a combination of assert statements and error handling techniques throughout the code. Try-catch blocks were used to handle loops and element access which could produce issues in faulty XML files. Deliberately faulty XML files were used to check the performance of these measures.
2) Assert statements have been used to prevent users from inserting the wrong inputs into the program, and to make sure that the number of valid command line arguments are not exceeded
3) Assert statements are used throughout the indexing for string-slicing to ensure that the indexes used are not out of bounds (such as when the exon coordinates for transcripts are used for protein sequences)
4) Try-catches are used during opening the input file, accessing th sequence elements and determining the intronic padding to be used when outputting the exons.
5) A loop to detect an additional option for genomic, transcript and protein sequences has been written. This would cause the program to choose between one of three separate methods, one for each type. Only one has been written as of 20/11/2014, although this program is extensible. Exceptions were also used to provide users with readable error messages if parameters or file contents were not found at runtime



*** Note: This program was edited 03/12/2014 to add the coordinates of the exon start/finish to the printed FastA file, and to add protein sequence printing functionality to the program
---
The added functionality is summarised below;
* The program now takes a third argument by default (program name, target LRG, intronic padding, **Option**)
* Options and padding are not mandatory, but currently padding is required to input an option (argument ordering, I'll look into changing this)
* Available options are 
    - '-g': default, genomic sequence only
    - '-p': protein sequence only
    - '-pg' | '-gp': genomic and protein sequence. Layout is header, DNA, protein

* The content of the string subsections isolated using this program have been validated against existing reference sequences for both length and content, with one caveat: 
	* In WMRGL it is generally standard practice to have the amino acid encoded by a codon above the third letter of the codon, mostly for reasons of appearance. In the LRG file, the coordinates of the amino acids correspond to the base which encodes the *final* base of the codon. This means that at times the amino acids may not appear exactly where they are expected in the reference sequence document, but they will correspond to the correct portion of the sequence.

M. Welland
    
