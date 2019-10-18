import flowcell_parser.classes as classes
import os


def test_samplesheet():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.SampleSheetParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/SampleSheet.csv'))
    expected_header = {'Investigator Name': 'Christian Natanaelsson', 'Date': '2015-04-23', 'Experiment Name': 'H2WY7CCXX'}
    assert k.header == expected_header
    assert k.settings == []
    assert k.reads == []

def test_runinfo():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.RunInfoParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/RunInfo.xml'))
    expected_data = {'Number': '31',
                     'FlowcellLayout': {'TileCount': '24', 'LaneCount': '8', 'SurfaceCount': '2', 'SwathCount': '2'},
                     'Instrument': 'ST-E00214',
                     'Reads': [{'IsIndexedRead': 'N', 'NumCycles': '151', 'Number': '1'},
                               {'IsIndexedRead': 'Y', 'NumCycles': '8', 'Number': '2'},
                               {'IsIndexedRead': 'N', 'NumCycles': '151', 'Number': '3'}],
                     'Flowcell': 'H2WY7CCXX',
                     'Date': '150424',
                     'Id': '150424_ST-E00214_0031_BH2WY7CCXX'}
    assert k.data == expected_data

def test_runparameters():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.RunParametersParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/runParameters_thin.xml'))
    expected_data = {'RunParameters':
                     {'Setup': {'ScannerID': 'ST-E00214',
                                'FPGADynamicFocusSettings': {'MaxInitialZJumpHalfUm': '3'},
                                'Reads': {'Read': {'IsIndexedRead': 'N', 'NumCycles': '151', 'Number': '1'}},
                                'ReagentKits': {'Sbs': {'SbsReagentKit': {'Prime': 'false', 'IsNew200Cycle': 'true', 'ID': 'Y'}}, 'Pe': {'ReagentKit': {'ID': 'Y'}}},
                                'TileWidth': '3200',
                                'TempFolder': 'O:\\Illumina\\HiSeqTemp\\150424_ST-E00214_0031_BH2WY7CCXX',
                                'BaseSpaceSettings': {'Username': None},
                                'SelectedSections': {'Section': {'Name': 'A_1'}},
                                'ExperimentName': 'H2WY7CCXX'}}}
    assert k.data == expected_data

def test_laneBarcode():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.LaneBarcodeParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/laneBarcode_thin.html'))
    expected_flowcell_data = {u'Yield (MBases)': u'939,600', u'Clusters(PF)': u'3,111,257,766', u'Clusters (Raw)': u'4,966,525,440'}
    expected_sample_data = [{u'Sample': u'56.64', u'Lane': u'1', u'#': u'GAATTCGT',
                             u'Filtered data': u'P1775_147', u'Project': u'351,637,396',
                             u'Raw data': u'D_Moreno_15_01', u'Clusters': u'106,194',
                             u'Barcode sequence': u'351,637,396'},
                            {u'Sample': u'43.36', u'Lane': u'1', u'#': u'unknown',
                             u'Filtered data': u'unknown', u'Project': u'269,178,284',
                             u'Raw data': u'default', u'Clusters': u'13,232',
                             u'Barcode sequence': u'43,813,954'}]
    assert k.flowcell_data == expected_flowcell_data
    assert k.sample_data == expected_sample_data

def test_lane():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.LaneBarcodeParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/Reports/html/H2WY7CCXX/all/all/all/lane_thin.html'))
    expected_sample_data = [{u'Yield (Mbases)': u'37.75',
                             u'Lane': u'1',
                             u'% One mismatchbarcode': u'63.70',
                             u'% Perfectbarcode': u'119,426',
                             u'#': u'95.00',
                             u'Filtered data': u'100.00',
                             u'Raw data': u'620,815,680',
                             u'Clusters': u'88.69',
                             u'% of thelane': u'395,451,350'}]
    assert k.sample_data == expected_sample_data

def test_parser():
    path = os.path.dirname(os.path.abspath(__file__))
    k = classes.RunParser(os.path.join(path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX'))
    assert k.obj is not None
    assert k.obj is not {}
    assert k.obj['run_setup'] == "2x151"


