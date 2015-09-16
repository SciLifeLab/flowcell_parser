
import flowcell_parser.classes as classes
import os


def test_samplesheet():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.SampleSheetParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/SampleSheet.csv'))
    assert(k.header is not None)
    assert(k.settings is not None)
    assert(k.reads is not None)

def test_runinfo():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.RunInfoParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/RunInfo.xml'))
    assert(k.data is not None)

def test_runparameters():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.RunParametersParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/runParameters.xml'))
    assert(k.data is not None)
    

def test_demuxstats():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.DemultiplexingStatsParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/DemultiplexingStats.xml'))
    assert(k.data is not None)

def test_laneBarcode():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.LaneBarcodeParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/laneBarcode.html'))
    assert(k.flowcell_data is not None)
    assert(k.sample_data is not None)

def test_lane():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.LaneBarcodeParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/laneBarcode.html'))
    assert(k.sample_data is not None)

def test_parser():
    path = os.path.dirname(os.path.abspath(__file__))
    k=classes.RunParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX'))
    assert(k.obj is not None)
    assert(k.obj is not {})
    assert(k.obj['run_setup'] is not None)
    assert(k.runinfo.data is not None)
    assert(k.runparameters.data is not None)
    assert(k.samplesheet.data is not None)
    assert(k.lanebarcodes.flowcell_data is not None)
    assert(k.lanebarcodes.sample_data is not None)
    assert(k.lanes.sample_data is not None)


