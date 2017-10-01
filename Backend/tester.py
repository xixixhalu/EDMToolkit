#import Parser.parse_DM_File as p
import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

from Parser.parse_DM_File import analyzer as p
from Parser.domain_model import Domain_Model as dmo

ana = p()
print ana.DM_File_Analyze('/Users/nitin/Documents/Academics/USC/UnpaidIntern/Misc', {'DM_Input_type': "Simple_XML"})

#object1 = dmo.Element('SIMPL')
#object1.test = "Nitin"

#print object1.test


# class t1:
# 	def __init__(self,a=1):
# 		self.a = a

# class t2(t1):
# 	def __init__(self,a=2,b=3):
# 		t1.__init__(self,a)
# 		self.b = b

# class t3(t2):
# 	def __init__(self,a=4,b=5,c=6):
# 		t2.__init__(self,a,b)
# 		self.c = c

# x = t3()
# print x.a
# print x.b
# print x.c