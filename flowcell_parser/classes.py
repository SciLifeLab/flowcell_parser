
import os
import csv
import xml.etree.ElementTree as ET
import logging

from bs4 import BeautifulSoup #html parser

class XTenParser(object):
    def __init__(self, path):
        if os.path.exists(path):
            self.log=logging.getLogger('XTenParser')
            self.path=path
            self.parse()
            self.create_db_obj()
        else:
            raise os.error("XTen flowcell cannot be found at {0}".format(path))

    def parse(self):
        fc_name=self.path[-9:]
        rinfo_path=os.path.join(self.path, 'RunInfo.xml')
        rpar_path=os.path.join(self.path, 'runParameters.xml')
        ss_path=os.path.join(self.path, 'SampleSheet.csv')
        lb_path=os.path.join(self.path, 'Demultiplexing', 'Reports', 'html', fc_name, 'all', 'all', 'all', 'laneBarcode.html')

        try:
            self.runinfo=XTenRunInfoParser(rinfo_path)
        except OSError as e:
            self.log.info(str(e))
            self.runinfo=None
        try:
            self.runparameters=XTenRunParametersParser(rpar_path)
        except OSError as e:
            self.log.info(str(e))
            self.runParameters=None
        try:
            self.samplesheet=XTenSampleSheetParser(ss_path)
        except OSError as e:
            self.log.info(str(e))
            self.samplesheet=None
        try:
            self.lanebarcodes=XTenLaneBarcodeParser(lb_path)
        except OSError as e:
            self.log.info(str(e))
            self.lanebarcodes=None


    def create_db_obj(self):
        self.obj={}
        bits=os.path.basename(self.path).split('_')
        name="_".join(bits[0], bits[-1])
        self.obj['name']=name
        if self.runinfo:
            self.obj['RunInfo']=self.runinfo.data
        if self.runparameters:
            self.obj['RunParameters']=self.runparameters.data
        if self.samplesheet:
            self.obj['samplesheet_csv']=self.samplesheet.data
        if self.lanebarcodes:
            self.obj['illumina']={}
            self.obj['illumina']['Demultiplex_Stats']={}
            self.obj['illumina']['Demultiplex_Stats']['Barcode_lane_statistics']=self.lanebarcodes.sample_data
            self.obj['illumina']['Demultiplex_Stats']['Flowcell_stats']=self.lanebarcodes.flowcell_data
        




class XTenLaneBarcodeParser(object):
    def __init__(self, path ):
        if os.path.exists(path):
            self.path=path
            self.parse()
        else:
            raise os.error("XTen laneBarcode.html cannot be found at {0}".format(path))

    def parse(self):
        self.sample_data=[]
        self.flowcell_data={}
        with open(self.path) as htmlfile:
            bsoup=BeautifulSoup(htmlfile)
            flowcell_table=bsoup.find_all('table')[1]
            lane_table=bsoup.find_all('table')[2]

            
            keys=[]
            values=[]
            for th in flowcell_table.find_all('th'):
                keys.append(th.text)
            for td in flowcell_table.find_all('td'):
                values.append(td.text)

            self.flowcell_data = dict(zip(keys, values))

            keys=[]
            rows=lane_table.find_all('tr')
            for row in rows[1:]:
            #I want to skip the first row
                if len(row.find_all('th')):
                    #this is the header row
                    seen_clusters=False
                    for th in row.find_all('th'):
                        key=th.text.replace('<br/>', ' ').replace('&gt;', '>')
                        if key == '#':
                            key='Lane'
                        elif key == 'Clusters':
                            if not seen_clusters:
                                key= 'Raw Clusters'
                                seen_clusters=True


                        keys.append(key)
                elif len(row.find_all('td')):
                    values=[]
                    for td in row.find_all('td'):
                        values.append(td.text)

                    d=dict(zip(keys,values))
                    self.sample_data.append(d)




class XTenDemultiplexingStatsParser(object):
    def __init__(self, path ):
        if os.path.exists(path):
            self.path=path
            self.parse()
        else:
            raise os.error("XTen DemultiplexingStats.xml cannot be found at {0}".format(path))

    def parse(self):
        data={}
        tree=ET.parse(self.path)
        root = tree.getroot()
        self.data=xml_to_dict(root)


class XTenSampleSheetParser(object):
    """Parses Xten Samplesheets, with their fake csv format.
    Should be instancied with the samplesheet path as an argument.

    .header : a dict containing the info located under the [Header] section
    .settings : a dict containing the data from the [Settings] section
    .reads : a list of the values in the [Reads] section
    .data : a list of the values under the [Data] section. These values are stored in a dict format
    .datafields : a list of field names for the data section"""
    def __init__(self, path ):
        if os.path.exists(path):
            self.parse(path)
        else:
            raise os.error("XTen sample sheet cannot be found at {0}".format(path))

    def parse(self, path):
        flag=None
        header={}
        reads=[]
        settings=[]
        csvlines=[]
        data=[]
        with open(path) as csvfile:
            for line in csvfile.readlines():
                if '[Header]' in line:
                    flag='HEADER'
                elif '[Reads]' in line:
                    flag='READS'
                elif '[Settings]' in line:
                    flag='SETTINGS'
                elif '[Data]' in line:
                    flag='data'
                else:
                    if flag == 'HEADER':
                       header[line.split(',')[0]]=line.split(',')[1] 
                    elif flag == 'READS':
                        reads.append(line.split(',')[0])
                    elif flag == 'SETTINGS':
                        settings.append(line.split(',')[0])
                    elif flag == 'data':
                        csvlines.append(line)

            reader = csv.DictReader(csvlines)
            for row in reader:
                linedict={}
                for field in reader.fieldnames:
                    linedict[field]=row[field]
                data.append(linedict)

            self.datafields=reads.fieldnames
            self.data=data
            self.settings=settings
            self.header=header
            self.reads=reads


class XTenRunInfoParser(object):
    """Parses Xten RunInfo.xml.
    Should be instancied with the file path as an argument.

    .data : a list of hand-picked values :
     -Run ID
     -Run Number
     -Instrument
     -Flowcell name
     -Run Date
     -Reads metadata
     -Flowcell layout
    """
    def __init__(self, path ):
        self.data={}
        self.path=path
        if os.path.exists(path):
            self.parse()
        else:
            raise os.error("XTen run info cannot be found at {0}".format(path))

    def parse(self):
        data={}
        tree=ET.parse(self.path)
        root = tree.getroot()
        run=root.find('Run')
        data['Id']=run.get('Id')
        data['Number']=run.get('Number')
        data['Instrument']=run.find('Instrument').text
        data['Flowcell']=run.find('Flowcell').text
        data['Date']=run.find('Date').text
        data['Reads']=[]
        for read in run.find('Reads').findall('Read'):
            data['Reads'].append(read.attrib)
        layout=run.find('FlowcellLayout')
        data['FlowcellLayout']=layout.attrib

        self.data=data

        
        
class XTenRunParametersParser(object):
    """Parses a runParameters.xml file.
       This is a much more general xml parser, it will build a dict from the xml data.
       Attributes might be replaced if children nodes have the same tag as the attributes
       This does not happen in the current xml file, but if you're planning to reuse this, it may be of interest.
    """

    def __init__(self, path ):
        self.data={}
        self.path=path
        if os.path.exists(path):
            self.parse()
        else:
            raise os.error("XTen run parameters cannot be found at {0}".format(path))
        
    def parse(self):
        data={}
        tree=ET.parse(self.path)
        root = tree.getroot()
        self.data=xml_to_dict(root)
        

def xml_to_dict(root):
    current=None

    children=list(root)
    if children:
        current={}
        duplicates={}
        for child in children:
            if len(root.findall(child.tag))>1:
                if child.tag not in duplicates:
                    duplicates[child.tag]=[]
                lower=xml_to_dict(child)
                duplicates[child.tag].extend(lower.values())
                current.update(duplicates)
            else:
                lower=xml_to_dict(child)
                current.update(lower)
    if root.attrib:
        if current:
            if [x in current for x in root.attrib]:
                current.update(root.attrib)
            else:
                current.update({'attribs':root.attribs})
        else:
            current= root.attrib
    if root.text and root.text.strip() != "":
        if current:
            if 'text' not in current:
                current['text']=root.text
            else:
                #you're really pushing here, pal
                current['xml_text']=root.text
        else:
            current=root.text
    return {root.tag:current}

            

