
import flowcell_parser.classes as classes

import pprint


def test_samplesheet():
    k=classes.XTenSampleSheetParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/SampleSheet.csv')
    pprint.pprint(k.data)
    print k.header
    print k.settings
    print k.reads

def test_runinfo():
    k=classes.XTenRunInfoParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/RunInfo.xml')
    pprint.pprint(k.data)

def test_runparameters():
    k=classes.XTenRunParametersParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/runParameters.xml')
    pprint.pprint(k.data)
    

def test_demuxstats():
    k=classes.XTenDemultiplexingStatsParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/DemultiplexingStats.xml')
    pprint.pprint(k.data)

def test_laneBarcode():
    k=classes.XTenLaneBarcodeParser('../test_data/laneBarcode.html')
    pprint.pprint(k.flowcell_data)
    pprint.pprint(k.sample_data)

def test_parser():
    k=classes.XTenParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX')
    pprint.pprint(k.obj)


test_samplesheet()
