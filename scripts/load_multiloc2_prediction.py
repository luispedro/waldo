from waldo.predictions.models import Prediction 

def load_multiloc2_predictions(inputfile, create_session=None):
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()
    for line in file(inputfile):
        if not line.startswith('ENS'): continue
        tokens = line.strip().split('\t')
        name = tokens[0]
        for tok in tokens[1:]:
            loc,value = tok.split(': ')
            if float(value) > .05:
                session.add(Prediction('MultiLoc2', name, loc, float(value)))
        session.commit()

if __name__ == '__main__':
    import sys
    load_multiloc2_predictions(sys.argv[1])

