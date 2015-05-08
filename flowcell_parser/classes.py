
import os
import csv
import xml.etree.ElementTree as ET

class XTenSampleSheetParser(object):
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

            self.data=data
            self.settings=settings
            self.header=header
            self.reads=reads


class XTenRunInfoParser(object):
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
        self.data=self.xml_to_dict(root)
        

    def xml_to_dict(self,root):
        current={}
        if root.attrib:
            current[root.tag]= root.attrib

        children=list(root)
        if children:
            duplicates={}
            for child in children:
                if len(root.findall(child.tag))>1:
                    if child.tag not in duplicates:
                        duplicates[child.tag]=[]
                    lower=self.xml_to_dict(child)
                    duplicates[child.tag].extend(lower.values())
                    current.update({child.tag:duplicates})
                else:
                    lower=self.xml_to_dict(child)
                    current.update(lower)
        if root.text and root.text.strip() != "":
            if root.tag in current:
                if 'text' not in current[root.tag]:
                    current[root.tag]['text']=root.text
                else:
                    #you're really pushing here, pal
                    current[root.tag]['xml_text']=root.text
            else:
                current[root.tag]=root.text
        if not current:
            current=None
        return {root.tag:current}

            

