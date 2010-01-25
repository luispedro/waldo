import MySQLdb

"""
This is the framework for accessing, reading, and parsing out information
in the various protein database files. Each database has its own unique
format, so a separate class can be created specifically for parsing out
that format and inserting it into a relational database.

To extend this framework, simply create a subclass of AbstractDB.

The abstract superclass, AbstractDB, is responsible for storing the settings
that are global to all subclasses, such as filesystem paths to the database
files, and the connection to the relational database.
"""

class AbstractDB:
    SYSTEMPATH = '../../databases/'
    DATABASE = 'waldo'
    DBUSER = 'researchuser'
    PASSWORD = 'r3NMYGccy7PLQp9b'

    def __init__(self, files):
        self.dbfiles = files
        self.dbconn = MySQLdb.connect('localhost', AbstractDB.DBUSER, AbstractDB.PASSWORD, AbstractDB.DATABASE) or quit('ERROR: Unable to open database "%s". Please check your connection settings.' % AbstractDB.DATABASE)
        try:
            getattr(self, "populate")
            #getattr(self,
        except AttributeError:
            quit('ERROR: Please ensure your class "%s" has all the required methods.' % self.__class__)

    def getFile(self, index):
        return self.dbfiles[index]

    def getDB(self):
        return self.dbconn()

class eSLDB(AbstractDB):
    def __init__(self, filename, type):
        AbstractDB.__init__(self, [filename,])
        self.type = type

    def populate(self):
        count = 0
        for line in file(self.getFile(0):
            # read each line in the eSLDB database file
            # split according to tabs
            count += 1
            if count == 1:
                # the first line of the db file is a bunch of labels
                continue

            # starting with the second line:
            esldb_id, ensembl_peptide, experimental_annot, uniprot_annot, uniprot_entry, similarity_annot, uniprot_homologue, e_value, prediction, aa_sequence, common_name = line.strip().split('\t')
            if e_value == 'None':
                e_value = '-1.0'
            query = 'INSERT INTO esldb (esldbid, experimental_annot, similarity_annot, uniprot_fulltext_annot, uniprot_entry_id, uniprot_homologue_id, prediction, db_type) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (esldb_id, experimental_annot, similarity_annot, uniprot_annot, uniprot_entry, uniprot_homologue, e_value, self.type)
            self.getDB().cursor().execute(query)

            # now, insert the ensembl id and map back to this


class Uniprot(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def populate(self):
        pass

class MGI(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def populate(self):
        pass

class LOCATE(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def populate(self):
        pass

if __name__ == '__main__':
    x = eSLDB('something')
    print x.__class__
