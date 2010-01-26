import backend
import mgi.files
import mgi.load
import go.files
import go.load
import uniprot.files
import uniprot.load

create_session = backend.create_session

go.load.load(go.files.inputfilename, create_session)
mgi.load.load(mgi.files.inputfilename, create_session)
uniprot.load.load(uniprot.files.inputfilename, create_session)

