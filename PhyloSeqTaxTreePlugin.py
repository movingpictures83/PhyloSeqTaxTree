import PyPluMA

class PhyloSeqTaxTreePlugin:
   def input(self, filename):
        infile = open(filename, 'r')
        self.parameters = dict()
        for line in infile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

        taxafile = open(PyPluMA.prefix()+"/"+self.parameters["tax"])
        taxafile.readline()
        self.taxamap = dict()
        for line in taxafile:
            contents = line.strip().split(',')
            # NCBI ID maps to taxaname
            self.taxamap[contents[len(contents)-1]] = contents[0][1:len(contents[0])-1]

        print(self.taxamap)
        treefile = open(PyPluMA.prefix()+"/"+self.parameters["tree"])
        # One line
        self.treecontents = treefile.readline()

   def run(self):
        delimiters = [',', '(', ')', ';', ':']
        # Strategy: Go character by character
        # Parse up to the next delimiter
        # Check ID
        self.finaltreecontents = ""
        currentID = ""
        for i in range(len(self.treecontents)):
            if (self.treecontents[i] in delimiters):
               if (len(currentID) != 0):
                   IDtoCheck = currentID
                   if (IDtoCheck.startswith('INT')):
                       IDtoCheck = IDtoCheck[3:]
                   print(IDtoCheck)
                   if (IDtoCheck in self.taxamap):
                       self.finaltreecontents += self.taxamap[IDtoCheck]
                   else:
                       self.finaltreecontents += currentID
                   currentID = "" # Reset
               self.finaltreecontents += self.treecontents[i] # Write the delimiter
            else:
               # Not a delimiter, add to currentID
               currentID += self.treecontents[i]

   def output(self, filename):
       outfile = open(filename, 'w')
       outfile.write(self.finaltreecontents)
