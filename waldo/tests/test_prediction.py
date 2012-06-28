from sqlalchemy import create_engine, and_         
import waldo.predictions.models
from sqlalchemy.orm import sessionmaker            
def test_smoke():
    metadata = waldo.predictions.models.Base.metadata 
    engine = create_engine('sqlite://')
    metadata.bind = engine                       
    metadata.create_all()
    sessionmaker_ = sessionmaker(engine)
    session = sessionmaker_()
    p = waldo.predictions.models.Prediction('MultiLoc2', 'ENSMUSG00000007564', 'mitochondria', 0.2)
    session.add(p)
    session.commit()
    assert session.query(waldo.predictions.models.Prediction) \
            .filter_by(protein='ENSMUSG00000007564').count() 

