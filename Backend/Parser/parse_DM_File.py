#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

import os
from Errors import exceptions as e
from Parser.domain_model import Domain_Model
from Parser import datatypes as dt
import xml.etree.ElementTree as ET

class analyzer:

    def xmiPrefixAppender(self, key, xmiPrefix):
        return '{' + xmiPrefix + '}' + key

    def DM_File_Analyze(self,PROJECT_DIR, config):
        if not os.path.exists(PROJECT_DIR):
            raise e.SimpleException("Project Home Directory not created, run project initialize first.")
        DM_File_type = config['DM_Input_type']
        if DM_File_type == "Simple_XML":
            retObj = self.parseSimpleXML(PROJECT_DIR)
            if retObj is None:
                raise e.SimpleException("xml file not provided in the directory, check if file with extension .xml is uploaded")
            return retObj


    def SimpleXMLUtil(self,dmoFile, _dmoName):
        # NITIN : TODO : check how to handle namepspaces dynamically later
        namespaces = {"xmi_namespace": "http://schema.omg.org/spec/XMI/2.1"}
        myDMO = ET.parse(dmoFile)
        root = myDMO.getroot()
        

        # NITIN : TODO : Change parsing after correcting assumptions about the XML structure
        definition = root.find('xmi_namespace:Extension', namespaces)   
        elements = definition.find("elements")
        if elements is not None : elements = elements.findall("element")

        dmo = Domain_Model(_dmoName)


        # NITIN : NOTE : Adding elements and their attributes/operations into model
        for element in elements:
            # NITIN : NOTE : If element is a definition of a class, then extract it's name, definition, attributes, relations
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":
                elemId = element.get(self.xmiPrefixAppender('idref', namespaces["xmi_namespace"] ))
                elemName = element.get('name').strip()
                dmo.declareElement( elemName , elemId)
                
                # NITIN : NOTE : Check if the element has any attributes defined and aadd them
                elemAttributes = element.find('attributes')
                if elemAttributes is not None:
                    for elemAttribute in elemAttributes:
                        elemAttributeName = elemAttribute.get('name')
                        elemAttributeType = elemAttribute.find('properties').get('type')
                        # NITIN : TODO : implementation only for simple attributes, check how complex attributes are represented in xml
                        if elemAttributeType == "int" : elemAttributeTypeSetter = dt.Integer()
                        if elemAttributeType == "string" : elemAttributeTypeSetter = dt.String()
                        # NITIN : TODO : implement checker for other data datatypes like float etc.
                        dmo.defineSimpleAttribute(elemName, elemAttributeName, elemAttributeTypeSetter)
                        # NITIN : TODO : extract other features like upper and lower bounds, scope,

                # NITIN : TODO : Check if the element has any operations defined and aadd them, implement operations on domain model

                
        # NITIN : NOTE : Adding relations on elemnets into model
        for element in elements:
            if element.get(self.xmiPrefixAppender('type', namespaces["xmi_namespace"] )) == "uml:Class":

                elemRelations = element.find('links')
                if elemRelations is None : continue
                for elemRelation in elemRelations:
                    relationId = elemRelation.get(self.xmiPrefixAppender('id',namespaces["xmi_namespace"]))
                    dmo.defineRelation(relationId, str(elemRelation.get('start')), str(elemRelation.get('end')) , str(elemRelation.tag))

                    






        #print dmo.toString()

        return dmo.toJson()




    def parseSimpleXML(self,PROJECT_DIR):
        # NITIN : NOTE : Only a single dm file needs to placed per project directory
        for f in os.listdir(PROJECT_DIR):
            if f.endswith('.xml'):
                return self.SimpleXMLUtil(PROJECT_DIR + "/" + f, f[:-4])
        return None
