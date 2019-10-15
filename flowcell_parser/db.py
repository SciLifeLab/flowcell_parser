import couchdb
import yaml
import logging

log = logging.getLogger(__name__)


def setupServer(conf):
    db_conf = conf['statusdb']
    url = "http://{0}:{1}@{2}:{3}".format(db_conf['username'], db_conf['password'], db_conf['url'], db_conf['port'])
    return couchdb.Server(url)

def update_doc(db, obj, over_write_db_entry=False):
    view = db.view('info/name')
    #If there is already a flowcell with that name in the DB
    if len(view[obj['name']].rows) == 1:
        remote_doc = view[obj['name']].rows[0].value
        #remove id and rev for comparison
        doc_id = remote_doc.pop('_id')
        doc_rev = remote_doc.pop('_rev')
        if remote_doc != obj:
            #if they are different, merge the old into the new
            if not over_write_db_entry:
                #do not merge if over_write option is specified
                obj = merge(obj, remote_doc)
            obj['_id'] = doc_id
            obj['_rev'] = doc_rev
            db[doc_id] = obj 
            log.info("updating {0}".format(obj['name']))
    elif len(view[obj['name']].rows) == 0:
        #it is a new doc, upload it
        db.save(obj) 
        log.info("saving {0}".format(obj['name']))
    else:
        log.warn("more than one row with name {0} found".format(obj['name']))

#merges d2 in d1, keeps values from d1
#taken from scilifelab
def merge(d1, d2):
    """ Will merge dictionary d2 into dictionary d1.
    On the case of finding the same key, the one in d1 will be used.
    :param d1: Dictionary object
    :param s2: Dictionary object
    """
    for key in d2:
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                merge(d1[key], d2[key])
            elif d1[key] == d2[key]:
                pass # same leaf value
            else:
                log.debug("Values for key {key} in d1 and d2 differ, using d1's value".format(key=key))
        else:
            d1[key] = d2[key]
    return d1
