# EDMToolkit

**_Please remember to branch off and merge later, do not commit on master_**

## Basic Structure
- Backend : All the functionalities that execute once the file has been uploaded to server
  - Parser : Parser module for the uploaded files
  - Errors : Custom error modules
- Frontend :
- MiscScripts :
- OtherActionItems : Please upload any misc items like images, architecture design, templates, ideas, todos etc. here
  - [ ] @Vinitha, please upload Frontend templates here and then check off this box
  - [ ] @Nitin, upload architecture diagram
  - [ ] @Bo, please add any other action items here
  
  
## How to run:
- Clone the repository
- Navigate inside EDMToolkit
- **Before every execution, please run `sh clean_pycs.sh` on the root folder to clean all binaries**
- run the `sh trigger_script.sh <name_of_python_file_to_run>`. For example I run `sh trigger_script.sh Backend/tester.py` to run some tests on the backend code.
- Make sure that all the code in the Backend has a `__init.py__` file associated to make it a importable library.

