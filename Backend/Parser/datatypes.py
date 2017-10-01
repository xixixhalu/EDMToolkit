import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

from Errors import exceptions as e


class BaseType:
	def __init__(self, _minOccurs=1, _maxOccurs = 1):
		self.minOccurs = 1
		self.maxOccurs = 1


class SimpleType(BaseType):
	def __init__(self,_minOccurs=1, _maxOccurs = 1):
		BaseType.__init__(self,_minOccurs,_maxOccurs)




class ComplexType(BaseType):
	def __init__(self , _minOccurs=1, _maxOccurs = 1):
		BaseType.__init__(self,_minOccurs,_maxOccurs)

# NITIN : extends a base element
class ExtensionType(BaseType):
	def __init__(self,_BaseElementName):
		BaseType.__init__(self)
		self.BaseElementName = _BaseElementName

class Integer(SimpleType):
	def __init__(self , _minOccurs=1, _maxOccurs = 1):
		SimpleType.__init__(self,_minOccurs,_maxOccurs)





# NITIN : TODO : Enumerate all the simple datatypes...int,string,float
# NITIN : TODO : Implement restrictions implementations for the SimpleTypes ... from xsd ... refer(https://www.w3schools.com/xml/schema_dtypes_string.asp)







