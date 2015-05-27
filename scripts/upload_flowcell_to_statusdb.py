import argparse
import couchdb
import logging
import os
import yaml
import flowcell_parser.classes as cl
import flowcell_parser.db as db


def setupLog(args):
    mainlog = logging.getLogger('XTenParser')
    mainlog.setLevel(level=logging.INFO)
    mfh = logging.FileHandler(args.logfile)
    mft = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mfh.setFormatter(mft)
    mainlog.addHandler(mfh)
    return mainlog

def get_conf(conf_file):
    with open(conf,'r') as f:
        return yaml.load(f)

def main(args):
    log = setupLog(args)
    conf=get_conf(args.conf)
    couch = db.setupServer(conf)
    db=couch['x_flowcells']
    parser=cl.XTenParser(args.flowcell)
    db.update_doc(db,parser.obj)



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




    




