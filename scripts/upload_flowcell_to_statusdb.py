import argparse
import couchdb
import logging
import os
import yaml
import flowcell_parser.classes as cl


def setupLog(args):
    mainlog = logging.getLogger('XTenParser')
    mainlog.setLevel(level=logging.INFO)
    mfh = logging.FileHandler(args.logfile)
    mft = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mfh.setFormatter(mft)
    mainlog.addHandler(mfh)
    return mainlog

def setupServer(conf):
    with open(conf,'r') as f:
        db_conf = yaml.load(f)['statusdb']
        url="http://{0}:{1}@{2}:{3}".format(db_conf['username'], db_conf['password'], db_conf['url'], db_conf['port'])
        return couchdb.Server(url)
    return None

def update_doc(db, obj, log):
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


def main(args):
    log = setupLog(args)
    couch = setupServer(args.conf)
    db=couch['x_flowcells']
    parser=cl.XTenParser(args.flowcell)
    update_doc(db,parser.obj, log)



if __name__=='__main__':
    usage = "Usage:       python upload_flowcell_to_statusdb.py [options]"
    parser = argparse.ArgumentParser(description=usage)

    parser.add_argument("-f", "--flowcell", dest="flowcell", required=True,  
    help = "path to the flowcell to upload")

    parser.add_argument("-c", "--conf", dest="conf", 
    default=os.path.join(os.environ['HOME'],'opt/config/post_process.yaml'), 
    help = "Config file.  Default: ~/opt/config/post_process.yaml")

    parser.add_argument("-l", "--log", dest="logfile", 
    default=os.path.join(os.environ['HOME'],'flowcell_upload.log'), 
    help = "log file.  Default: ~/flowcell_upload.log")
    args = parser.parse_args()

    main(args)




    




