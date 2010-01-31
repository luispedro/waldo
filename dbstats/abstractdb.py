import MySQLdb
try:
    import settings
except ImportError:
    quit('ERROR: Cannot find "settings.py" file in the directory containing %r. Please ensure the structure of the application is correct and retry.' % __file__)

"""
This is the framework for accessing, reading, and parsing out information
in the various protein database files. Each database has its own unique
format, so a separate class can be created specifically for parsing out
that format and inserting it into a relational database.

To extend this framework, simply create a subclass of AbstractDB. Each subclass
is required to have four methods:

install
-this creates all database tables and columns that are needed to store the information
from this data source. No data is added at this step

initialize_data
-this method populates the empty tables with data from the flat files. This can take
awhile and should not be called unless the datasource has just been installed

update
-this methods performs an incremental update on the data stored in the database relative
to what is in the flat files. Usually called after a new version has been downloaded

search
-allows a datasource-specific search on the information in the database
"""

class AbstractDB:
    def __init__(self, files):
        self.dbfiles = files
        self.dbconn = MySQLdb.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME) or quit('ERROR: Unable to connect to database "%s". Please check your connection settings.' % DB_NAME)
        try:
            getattr(self, "install")
            #getattr(self, "initialize")
            #getattr(self, "update")
            #getattr(self, "search")
        except AttributeError:
            quit('ERROR: Please ensure your class "%s" has all the required methods.' % self.__class__)

    def getFiles(self):
        return self.dbfiles

    def getDB(self):
        return self.dbconn

class eSLDB(AbstractDB):
    def __init__(self, filename, type):
        AbstractDB.__init__(self, [filename,])
        self.type = type
    
    def install(self):
        pass

    def initialize_data(self):
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

    def update(self):
        pass

    def search(self):
        pass

class Uniprot(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def install(self):
        pass

    def initialize_data(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

class MGI(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def install(self):
        pass

    def initialize_data(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

class LOCATE(AbstractDB):
    def __init__(self, filename):
        AbstractDB.__init__(self, filename)

    def install(self):
        pass

    def initialize_data(self):
        pass

    def update(self):
        pass

    def search(self):
        pass

if __name__ == '__main__':
    x = eSLDB('something')
    print x.__class__
