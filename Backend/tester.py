#import Parser.parse_DM_File as p
import sys
import os
edm_root_dir = os.environ['EDM_ROOT_DIR']
sys.path.append('edm_root_dir' + 'Backend')

from Parser.parse_DM_File import analyzer as p
from Parser.domain_model import Domain_Model as dmo
from DatabaseSetup.setup import DBUtilities as dbu


ana = p()
dom = ana.DM_File_Analyze('/Users/nitin/Documents/Academics/USC/UnpaidIntern/Misc', {'DM_Input_type': "Simple_XML"})


dbutils = dbu()
dbutils.setup(configDictionary={"host":"127.0.0.1","port":32768})
dbutils.createOrUpdateDB(dom)
dbutils.shutdown()