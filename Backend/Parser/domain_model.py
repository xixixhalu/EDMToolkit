# -*- coding: utf-8 -*-
import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

from Errors import exceptions as e
from Parser import datatypes as dt
import uuid


class Domain_Model:
	

	def __init__(self):
		# NITIN : NOTE : Directory holds the id to object reference for the elements
		self.ElementDirectory = {}
        # NITIN : NOTE : Directory holds the name to id reference for the elements
 		self.ElementReference = {}

 	# NITIN : Element must be declared before being used
	def declareElement(self , _ElementName):
		# NITIN : NOTE : create a unique id for each element, used for associations
		elementId = uuid.uuid4().hex
		newElement = self.Element(_ElementName , elementId)
		self.ElementDirectory[elementId] = newElement
		self.ElementReference[_ElementName] = elementId

	# NITIN : NOTE : Define simple atrribute on a declared element
	def defineSimpleAttribute(self , _ElementName , _AttributeName , _AttributeType): 
		try:
			assert isElementDeclared(_ElementName)
		except:
			raise e.SimpleException("No such element declared, check for declaration of element :" + _ElementName)
		
		id = self.ElementReference[_ElementName]
		self.ElementDirectory[id].addSimpleAttribute(_AttributeName, _AttributeType)

	# NITIN : NOTE : Define a attribute of the type of another element
	def defineComplexAttribute(self, _ElementName , _AttributeName , _AttributeElementName , _AttributeType):
		try:
			assert isElementDeclared(_ElementName)
		except:
			raise e.SimpleException("No such element declared, check for declaration of element :" + _ElementName)

		if not isElementDeclared(_AttributeElementName) : raise e.SimpleException("Attempt to create attribute of type " + _AttributeElementType + " which is not declared .")

		id = self.ElementReference[_ElementName]
		self.ElementDirectory[id].addComplexAttribute(_AttributeName, _AttributeElementName, _AttributeType)

	# NITIN : NOTE : Make an element an extension of another element, basically imports all the base element's attributes and functions
	def extendElement(self, _ElementName, _ExtensionType):
		if not isinstance(_ExtensionType, dt.ExtensionType): raise e.SimpleException("_AttributeType has to be ExtensionType.")

		id = self.ElementReference[_ElementName]
		self.ElementReference[id].extendElement(_ExtensionType)

	# NITIN : NOTE : Utility function to check if element is declared
	def isElementDeclared(self, _ElementName):
		return self.ElementReference.has_key(_ElementName)

	# NITIN : NOTE : Utility function to display state of domain model
	def tostring(self):
		returnString = ""
		returnString += "Elements and their descriptions  :\n\n"
		for key,value in self.ElementReference.iteritems():
			returnString += key + " : \n" + str(self.ElementDirectory[value].tostring()) + "\n"
		return returnString

	class Element:
		
		def __init__(self, _ElementName , _id):
			self.id = _id
			# NITIN : NOTE : Keep tab if the element is an extension of another element
			self.isExtension = False
			self.ElementName = _ElementName
			# NITIN : NOTE : maps attribute name to a SimpleType Object
			self.SimpleAttributes = {}
			# NITIN : NOTE : maps attribute name to a tupl (ElementName, ComplexType Object)
			self.ComplexAttributes = {}
			# NITIN : TODO : add fucntionality to add custom functions on Domain Models
			self.Functions = {}
		
		def addSimpleAttribute(self, _AttributeName , _AttributeType):
			if not isinstance(_AttributeType,dt.SimpleType) : raise e.SimpleException("Trying to add a non SimpleType attribute in the function addSimpleAttribute .") 
			self.SimpleAttributes[_AttributeName] = _AttributeType
		
		def addComplexAttribute(self, _AttributeName , _AttributeElementName , _AttributeType):
			if not isinstance(_AttributeType, dt.ComplexType) : raise e.SimpleException("Trying to add a non ComplexType attribute in the function addComplexAttribute .")
			self.ComplexAttributes[_AttributeName] = (_AttributeElementName, _AttributeType)

		def extendElement(self, _ExtensionType):
			self.isExtension = True
			self.ExtensionType = _ExtensionType

		# NITIN : NOTE : Utility function to display state of Element	
		def tostring(self):
			returnString = ""
			returnString += "Simple attributes : \n"
			for key,value in self.SimpleAttributes.iteritems():
				returnString += key + ","
			returnString += "\nComplex attributes : \n"
			for key,value in self.SimpleAttributes.iteritems():
				returnString += key + ","
			returnString += "\n"

