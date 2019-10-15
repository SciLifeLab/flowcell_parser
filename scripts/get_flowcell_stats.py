import argparse
import yaml
import os
import re
import operator
import flowcell_parser.classes as parser


def flowcell_stats(flowcell):
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
        sample = element["Sample"]
        barcode = element["Barcode sequence"]
        if sample not in FC_dict[lane]:
            FC_dict[lane][sample] = {}
        #now populate the hash table
        FC_dict[lane][sample]["Reads"] = element["Clusters"]
        FC_dict[lane][sample]["Yield (Mbases)"] = element["Yield (Mbases)"]
        FC_dict[lane][sample]["% >= Q30bases"] = element["% >= Q30bases"]

    lanes = []
    for samples_lane in sorted(FC_dict.items(), key=operator.itemgetter(0)):
        lane = { "lane": samples_lane[0],
                "Reads": 0,
                "Yield (Mbases)": 0,
                "Raw Coverage": 0,
                "% >= Q30bases": 0,
                "Undetemined Reads": 0,
                "% Undetermined Reads": 0}
        #in case of demultiplexing the Q30 bases is belonging to one of the samples
        for sample_name, sample in samples_lane[1].iteritems():
            if sample_name == "unknown":
                lane["Undetemined Reads"] += int( re.sub(',', '', sample["Reads"]))
            else:
                lane["Reads"] += int( re.sub(',', '', sample["Reads"]))
                lane["Yield (Mbases)"] += int( re.sub(',', '', sample["Yield (Mbases)"]))
                lane["% >= Q30bases"] = sample["% >= Q30bases"]
        lane["Raw Coverage"] = lane["Yield (Mbases)"]*1000000/3200000000
        lane["% Undetermined Reads"] = (float(lane["Undetemined Reads"])/(lane["Reads"]+lane["Undetemined Reads"]))*100
        lanes.append(lane)

    print "FC\tLane\tReads\tYield(Mbases)\tRawCoverage\t%>Q30bases\tUndeteminedReads\t%Undetermined"
    for lane in lanes:
        import sys
        sys.stdout.write('{}\t'.format(FC_id))
        sys.stdout.write('{}\t'.format(lane["lane"]))
        sys.stdout.write('{}\t'.format(lane["Reads"]))
        sys.stdout.write('{}\t'.format(lane["Yield (Mbases)"]))
        sys.stdout.write('{}\t'.format(lane["Raw Coverage"]))
        sys.stdout.write('{}\t'.format(lane["% >= Q30bases"]))
        sys.stdout.write('{}\t'.format(lane["Undetemined Reads"]))
        sys.stdout.write('{}\n'.format(lane["% Undetermined Reads"]))


def main():
    parser = argparse.ArgumentParser(description="Script to print basic stats on X-Ten flowcells")
    parser.add_argument('--flowcell', action='store', help="Flowecell directory")
    args = parser.parse_args()

    assert os.path.exists(args.flowcell), "Could not locate flowcell {}".format(args.flowcell)
    flowcell_stats(args.flowcell)

if __name__ == "__main__":
    main()
