#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

import os
from Errors import exceptions as e
from Parser.domain_model import Domain_Model
import xml.etree.ElementTree as ET

class analyzer:

    def DM_File_Analyze(self,PROJECT_DIR, config):
        if not os.path.exists(PROJECT_DIR):
            raise e.SimpleException("Project Home Directory not created, run project initialize first.")
        DM_File_type = config['DM_Input_type']
        if DM_File_type == "Simple_XML":
            retObj = self.parseSimpleXML(PROJECT_DIR)
            if retObj is None:
                raise e.SimpleException("XSD file not provided in the directory, check if file with extension .XSD is uploaded")
            return retObj


    def SimpleXMLUtil(self,dmoFile):
        # NITIN : TODO : check how to handle namepspaces dynamically later
        namespaces = {"xml_namespace": "http://www.w3.org/2001/XMLSchema"}
        myDMO = ET.parse(dmoFile)
        root = myDMO.getroot()

        # NITIN : TODO : Change parsing after correcting assumptions about the XML structure
        # NITIN : NOTE : Assuming all the Elements are declared and then defined as complexType
        entity_definition = list(root.findall('xml_namespace:complexType', namespaces))
        #entity_declaration = list(root.findall('xml_namespace:element', namespaces))
        

        dmo = Domain_Model()


        for entity in entity_definition:
            name =  entity.attrib['name']
            #print name
            dmo.declareElement(name)

        print dmo.tostring()

        return "parsed"


    def parseSimpleXML(self,PROJECT_DIR):
        # NITIN : NOTE : Only a single dm file needs to placed per project directory
        for f in os.listdir(PROJECT_DIR):
            if f.endswith('.XSD'):
                return self.SimpleXMLUtil(PROJECT_DIR + "/" + f)
        return None
