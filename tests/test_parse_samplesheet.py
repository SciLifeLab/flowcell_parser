
import flowcell_parser.classes as classes


def test_samplesheet():
    k=classes.XTenSampleSheetParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/SampleSheet.csv')
    assert(k.header is not None)
    assert(k.settings is not None)
    assert(k.reads is not None)

def test_runinfo():
    k=classes.XTenRunInfoParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/RunInfo.xml')
    assert(k.data is not None)

def test_runparameters():
    k=classes.XTenRunParametersParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/runParameters.xml')
    assert(k.data is not None)
    

def test_demuxstats():
    k=classes.XTenDemultiplexingStatsParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/DemultiplexingStats.xml')
    assert(k.data is not None)

def test_laneBarcode():
    k=classes.XTenLaneBarcodeParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/laneBarcode.html')
    assert(k.flowcell_data is not None)
    assert(k.sample_data is not None)

def test_lane():
    k=classes.XTenLaneBarcodeParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/laneBarcode.html')
    assert(k.sample_data is not None)

def test_parser():
    k=classes.XTenParser('../test_data/150424_ST-E00214_0031_BH2WY7CCXX')
    assert(k.obj is not None)
    assert(k.obj is not {})
    assert(k.runinfo.data is not None)
    assert(k.runparameters.data is not None)
    assert(k.samplesheet.data is not None)
    assert(k.lanebarcodes.flowcell_data is not None)
    assert(k.lanebarcodes.sample_data is not None)
    assert(k.lanes.sample_data is not None)


