import argparse
import yaml
import os
import re
import flowcell_parser.classes as parser
#from /home/hiseq.bioinfo/opt/flowcell_parser/flowcell_parser/classes.py import XTenRunParametersParser


def flowcell_stats(flowcell):
    import pdb
    pdb.set_trace()
    #demultiplexing_stats = parser.XTenDemultiplexingStatsParser("150508_ST-E00214_0034_BH3CYHCCXX/Demultiplexing/Stats/DemultiplexingStats.xml")    
    #demultiplexing_stats.parse() #now I parsed the file
    #LaneBarcodeParses = parser.XTenLaneBarcodeParser("150508_ST-E00214_0034_BH3CYHCCXX/Demultiplexing/)
    FC_re = r'(\d{6})_([ST-]*\w+\d+)_\d+_([AB]?)([A-Z0-9\-]+)'
    flowcell_dirname = os.path.basename(flowcell)
    m = re.match(FC_re, flowcell_dirname)
    FC_id = m.group(4)
    laneBarcodeParser = parser.XTenLaneBarcodeParser(os.path.join("{}".format(flowcell), "Demultiplexing/Reports/html/", "{}".format(FC_id), "all/all/all/laneBarcode.html"))
    FC_dict = {} # contains an element for each lane
    for element in laneBarcodeParser.sample_data:
        lane = element["Lane"]
        if  lane  not in FC_dict:
            FC_dict[lane] = {}
        sample   = element["Sample"]
        barcode  = element["Barcode sequence"]
        if sample not in FC_dict[lane]:
            FC_dict[lane][sample] = {}   
        #now populate the hash table
        FC_dict[lane][sample]["Reads"]           = element["Clusters"]
        FC_dict[lane][sample]["Yield (Mbases)"]   = element["Yield (Mbases)"]
        if sample is not "unknown":
            FC_dict[lane][sample]["% >= Q30bases"] = element["% >= Q30bases"]
            

    pdb.set_trace()
    #/srv/illumina/HiSeq_X_data/150508_ST-E00214_0034_BH3CYHCCXX/Demultiplexing/Reports/html/H3CYHCCXX/all/all/all/laneBarcode.html
    print "this is the end of the test\n"



def main():
    parser = argparse.ArgumentParser(description="Script to print basic stats on X-Ten flowcells")
    parser.add_argument('--flowcell', action='store', help="Flowecell directory")
    args = parser.parse_args()

    assert os.path.exists(args.flowcell), "Could not locate flowcell {}".format(args.flowcell)
    flowcell_stats(args.flowcell)

if __name__ == "__main__":
    main()
