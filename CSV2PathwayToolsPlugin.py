import sys
#import numpy

import pythoncyc
meta = pythoncyc.select_organism('meta')


from pythoncyc.PToolsFrame import PFrame


class CSV2PathwayToolsPlugin:
   def input(self, filename):
      self.myfile = filename
      filestuff = open(self.myfile, 'r')
      mapper = dict()
      for line in filestuff:
         contents = line.split('\t')
         mapper[contents[0]] = contents[1].strip()
      self.csvfile = mapper['csvfile']
      self.compounddb = mapper['compounddb']

   def run(self):
      filestuff = open(self.csvfile, 'r')
      # Find the location of the Group HMDB
      # And the COMP ID
      for line in filestuff:
         if (line.find('Group HMDB') != -1):
            headings = line.split(',')
            hmdbspot = headings.index('Group HMDB')
            compidspot = headings.index('COMP ID')
            pubchemspot = headings.index('PUBCHEM')
            break

      # Create a mapping from Comp ID to Group HMDB
      self.comp2hmdb = dict()
      for line in filestuff:
         contents = line.split(',')
         self.comp2hmdb[contents[compidspot]] = (contents[hmdbspot], contents[pubchemspot])          

      # Create a mapping from HMDB to Pathway ID
      self.hmdb2pathway = dict()
      self.pubchem2pathway = dict()
      filestuff2 = open(self.compounddb, 'r')
      
      for line in filestuff2:
         if (not line.startswith('#')):
            contents = line.split('\t')
            compound = contents[0].strip()
            print compound
            try:
               tmp = PFrame(compound, meta, getFrameData=True).__dict__
               if (tmp.has_key('dblinks') and tmp['dblinks'].has_key('|HMDB|')):
                  #print "INSERTING..."
                  #raw_input()
                  hmdbid =  tmp['dblinks']['|HMDB|'][0]
                  self.hmdb2pathway[hmdbid] = compound
               if (tmp.has_key('dblinks') and tmp['dblinks'].has_key('|PUBCHEM|')):
                  #print "INSERTING..."
                  #raw_input()
                  pubchemid =  tmp['dblinks']['|PUBCHEM|'][0]
                  self.pubchem2pathway[pubchemid] = compound
            except TypeError:
               pass

   def output(self, filename):
      outputfile = open(filename, 'w')
      outputfile.write('Compound\tPathwayToolsID\n')
      found = 0
      total = 0
      #print self.hmdb2pathway
      #raw_input()
      for compound in self.comp2hmdb.keys():
          #print compound, str(self.comp2hmdb[compound]), self.hmdb2pathway.has_key(str(self.comp2hmdb[compound]))
          #raw_input()
          if self.hmdb2pathway.has_key(str(self.comp2hmdb[compound][0])):
             outputfile.write(compound+"\t"+self.hmdb2pathway[str(self.comp2hmdb[compound][0])]+"\n")
             found += 1
          elif self.pubchem2pathway.has_key(str(self.comp2hmdb[compound][1])):
             outputfile.write(compound+"\t"+self.pubchem2pathway[str(self.comp2hmdb[compound][1])]+"\n")
             found += 1
          else:
             outputfile.write(compound+"\tNOTFOUND\n")
          total += 1

      print found, " compounds found out of ", total


