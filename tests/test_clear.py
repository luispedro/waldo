from .backend import create_sessionmaker

import waldo.mgi.load
import waldo.go.load
import waldo.goslim.load
import waldo.uniprot.load
import waldo.locate.load
import waldo.hpa.load
import waldo.sequences.load
import waldo.nog.load
import waldo.uniprot.models
import waldo.go.models
import waldo.goslim.models
import waldo.mgi.models
import waldo.locate.models
import waldo.hpa.models
import waldo.translations.models
import waldo.predictions.models
import waldo.sequences.models
import waldo.nog.models



def test_all_clear():
    sessionmaker = create_sessionmaker(waldo.uniprot.models.Base.metadata)

    waldo.go.load.clear(sessionmaker)
    waldo.mgi.load.clear(sessionmaker)
    waldo.go.load.clear(sessionmaker)
    waldo.goslim.load.clear(sessionmaker)
    waldo.uniprot.load.clear(sessionmaker)
    waldo.locate.load.clear(sessionmaker)
    waldo.hpa.load.clear(sessionmaker)
    waldo.sequences.load.clear(sessionmaker)
    waldo.nog.load.clear(sessionmaker)
