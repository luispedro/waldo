import json
import sqlalchemy
from sqlalchemy.orm.collections import InstrumentedList

class EntryEncoder(json.JSONEncoder):

    def default(self, entry):
        '''
        json = E.default(entry)

        Introspectively generates a json object from a database entry
        '''
        res = {}
        for name in dir(entry) :
            if name.startswith('_'):
                continue
            val = getattr(entry, name)
            if isinstance(val, (unicode, str, int)):
                res[name] = val
            elif isinstance(val, InstrumentedList):
                res[name] = map(self.default, val)
        return res
