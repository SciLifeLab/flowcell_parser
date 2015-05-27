import couchdb
import yaml
import logging

log=logging.getlogger(__name__)


def setupServer(conf):
    db_conf = conf['statusdb']
    url="http://{0}:{1}@{2}:{3}".format(db_conf['username'], db_conf['password'], db_conf['url'], db_conf['port'])
    return couchdb.Server(url)

def update_doc(db, obj):
    view = db.view('info/name')
    #If there is already a flowcell with that name in the DB
    if len(view[obj['name']].rows) == 1:
        remote_doc = view[obj['name']].rows[0].value
        #remove id and rev for comparison
        doc_id = remote_doc.pop('_id')
        doc_rev = remote_doc.pop('_rev')
        if remote_doc != obj:
            #if they are different, though they have the same name, upload the new one
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

