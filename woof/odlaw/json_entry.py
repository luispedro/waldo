import json
import sqlalchemy
from sqlalchemy.orm.collections import InstrumentedList

class EntryEncoder(json.JSONEncoder):

    def default(self, entry):
        '''
            Introspectively generates a json object from a database entry
        '''
        json_set = []
        
        for a in dir(entry) :
            if not (a.startswith("_")) :
                val = getattr(entry, a)
                if type(val) is unicode or type(val) is int:
                    json_set.append((a, val))
                elif type(val) is sqlalchemy.orm.collections.InstrumentedList :
                    #recurse on relations
                    subset = []
                    for item in val:
                        subset.append(self.default(item))
                    json_set.append((a, subset))

        json_set = dict(json_set)
        return json_set
