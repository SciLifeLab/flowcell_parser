import unittest
import flowcell_parser.classes as classes
import os
import datetime


class TestSampleSheetParser(unittest.TestCase):

    def test_sample_sheet_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_sample_sheet = classes.SampleSheetParser(
            os.path.join(
                path,
                '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/',
                'SampleSheet.csv'))
        expected_header = {'Investigator Name': 'Christian Natanaelsson',
                           'Date': '2015-04-23',
                           'Experiment Name': 'H2WY7CCXX'}
        assert parsed_sample_sheet.header == expected_header
        assert parsed_sample_sheet.settings == []
        assert parsed_sample_sheet.reads == []

    def test_samplesheet_missing(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(OSError):
            parsed_sample_sheet = classes.SampleSheetParser(
                os.path.join(
                    path,
                    '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/',
                    'missing_SampleSheet.csv'))

    def test_sample_sheet_header_issue(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(RuntimeError):
            parsed_sample_sheet = classes.SampleSheetParser(
                os.path.join(
                    path,
                    '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/',
                    'SampleSheet_with_bad_header.csv'))


class TestRunInfoParser(unittest.TestCase):

    def test_run_info_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_run_info = classes.RunInfoParser(
            os.path.join(
                path,
                '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/RunInfo.xml'))
        expected_data = {'Number': '31',
                         'FlowcellLayout': {'TileCount': '24',
                                            'LaneCount': '8',
                                            'SurfaceCount': '2',
                                            'SwathCount': '2'},
                         'Instrument': 'ST-E00214',
                         'Reads': [{'IsIndexedRead': 'N',
                                    'NumCycles': '151',
                                    'Number': '1'},
                                   {'IsIndexedRead': 'Y',
                                    'NumCycles': '8',
                                    'Number': '2'},
                                   {'IsIndexedRead': 'N',
                                    'NumCycles': '151',
                                    'Number': '3'}],
                         'Flowcell': 'H2WY7CCXX',
                         'Date': '150424',
                         'Id': '150424_ST-E00214_0031_BH2WY7CCXX'}
        assert parsed_run_info.data == expected_data
        assert parsed_run_info.recipe == "2x151"

    def test_run_info_file_missing(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(OSError):
            parsed_run_info = classes.RunInfoParser(
                os.path.join(
                    path,
                    '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/',
                    'missing_RunInfo.xml'))


class TestRunParametersParser(unittest.TestCase):

    def test_run_parameters_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_run_parameters = classes.RunParametersParser(
            os.path.join(
                path,
                '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/',
                'runParameters.xml'))
        expected_data = {'RunParameters':
                         {'Setup':
                          {'ScannerID': 'ST-E00214',
                           'FPGADynamicFocusSettings':
                           {'MaxInitialZJumpHalfUm': '3'},
                           'Reads': {'Read': [{'IsIndexedRead': 'N',
                                               'NumCycles': '151',
                                               'Number': '1'},
                                              {'IsIndexedRead': 'Y',
                                               'NumCycles': '8',
                                               'Number': '2'},
                                              {'IsIndexedRead': 'N',
                                               'NumCycles': '151',
                                               'Number': '3'}]},
                           'ReagentKits': {'Sbs': {'SbsReagentKit':
                                                   {'Prime': 'false',
                                                    'IsNew200Cycle': 'true',
                                                    'ID': 'Y'}},
                                           'Pe': {'ReagentKit': {'ID': 'Y'}}},
                           'TileWidth': '3200',
                           'TempFolder': 'O:\\Illumina\\HiSeqTemp\\'
                           + '150424_ST-E00214_0031_BH2WY7CCXX',
                           'BaseSpaceSettings': {'Username': None},
                           'SelectedSections': {'Section': {'Name': 'A_1'}},
                           'ExperimentName': 'H2WY7CCXX'}}}
        assert parsed_run_parameters.data == expected_data

        def test_run_parameters_file_missing(self):
            path = os.path.dirname(os.path.abspath(__file__))
            with self.assertRaises(OSError):
                parsed_run_parameters = classes.RunParametersParser(
                    os.path.join(
                        path,
                        '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/',
                        'missing_runParameters.xml'))


class TestLaneBarcodeParser(unittest.TestCase):

    def test_lane_barcode_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_lane_barcodes = classes.LaneBarcodeParser(os.path.join(
            path,
            '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/',
            'Reports/html/H2WY7CCXX/all/all/all/laneBarcode.html'))
        expected_flowcell_data = {u'Yield (MBases)': u'939,600',
                                  u'Clusters(PF)': u'3,111,257,766',
                                  u'Clusters (Raw)': u'4,966,525,440'}
        expected_sample_data = [{u'Sample': u'56.64',
                                 u'Lane': u'1',
                                 u'#': u'GAATTCGT',
                                 u'Filtered data': u'P1775_147',
                                 u'Project': u'351,637,396',
                                 u'Raw data': u'D_Moreno_15_01',
                                 u'Clusters': u'106,194',
                                 u'Barcode sequence': u'351,637,396'},
                                {u'Sample': u'43.36',
                                 u'Lane': u'1',
                                 u'#': u'unknown',
                                 u'Filtered data': u'unknown',
                                 u'Project': u'269,178,284',
                                 u'Raw data': u'default',
                                 u'Clusters': u'13,232',
                                 u'Barcode sequence': u'43,813,954'}]
        assert parsed_lane_barcodes.flowcell_data == expected_flowcell_data
        assert parsed_lane_barcodes.sample_data == expected_sample_data

    def test_lane_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_lane = classes.LaneBarcodeParser(os.path.join(
            path,
            '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/',
            'Reports/html/H2WY7CCXX/all/all/all/lane.html'))
        expected_sample_data = [{u'Yield (Mbases)': u'37.75',
                                 u'Lane': u'1',
                                 u'% One mismatchbarcode': u'63.70',
                                 u'% Perfectbarcode': u'119,426',
                                 u'#': u'95.00',
                                 u'Filtered data': u'100.00',
                                 u'Raw data': u'620,815,680',
                                 u'Clusters': u'88.69',
                                 u'% of thelane': u'395,451,350'}]
        assert parsed_lane.sample_data == expected_sample_data

    def test_lane_barcode_file_missing(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(OSError):
            parsed_run_parameters = classes.RunParametersParser(os.path.join(
                path,
                '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/Demultiplexing/',
                'Reports/html/H2WY7CCXX/all/all/all/missing_file.html'))


class TestCycleTimesParser(unittest.TestCase):

    def test_cycle_times_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_cycle_times = classes.CycleTimesParser(os.path.join(
            path,
            '../test_data/150424_ST-E00214_0031_BH2WY7CCXX/Logs/',
            'CycleTimes.txt'))
        expected_cycle_times_data = [{'start': datetime.datetime(2019, 5, 20, 15,
                                                                 3, 22, 11000),
                                      'cycle_number': 1,
                                      'end': datetime.datetime(2019, 5, 20, 15,
                                                               20, 3, 878000)},
                                     {'start': datetime.datetime(2019, 5, 20, 15,
                                                                 20, 4, 387000),
                                      'cycle_number': 2,
                                      'end': datetime.datetime(2019, 5, 20, 15,
                                                               42, 14, 893000)}]
        assert parsed_cycle_times.cycles == expected_cycle_times_data

    def test_cycle_times_file_empty(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_cycle_times = classes.CycleTimesParser(os.path.join(
            path,
            '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/Logs/',
            'CycleTimes.txt'))
        assert parsed_cycle_times.cycles == []

    def test_cycle_times_file_missing(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(OSError):
            parsed_cycle_times = classes.CycleTimesParser(os.path.join(
                path,
                '../test_data/191018_ST-E00214_0031_BH2WY7CCXX/Logs/',
                'missing_CycleTimes.txt'))


class TestRunParser(unittest.TestCase):

    def test_runfolder_valid_case(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_run = classes.RunParser(os.path.join(
            path, '../test_data/150424_ST-E00214_0031_BH2WY7CCXX'))
        assert parsed_run.obj is not None
        assert parsed_run.obj is not {}

    def test_runfolder_empty(self):
        path = os.path.dirname(os.path.abspath(__file__))
        parsed_run = classes.RunParser(os.path.join(
            path, '../test_data/191023_ST-E00214_0031_BH2WY7CCXX'))
        expected_run_data = {'name': '191023_BH2WY7CCXX'}
        assert parsed_run.obj == expected_run_data
        assert parsed_run.runinfo is None
        assert parsed_run.runparameters is None
        assert parsed_run.samplesheet is None
        assert parsed_run.lanebarcodes is None
        assert parsed_run.lanes is None
        assert parsed_run.undet is None
        assert parsed_run.time_cycles is None
        assert parsed_run.json_stats is None

    def test_missing_runfolder(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with self.assertRaises(OSError):
            parsed_run = classes.RunParser(os.path.join(
                path, '../test_data/missing-191023_ST-E00214_0031_BH2WY7CCXX'))
