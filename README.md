# IntegrityCheck_IN_CharacterizationFramework
Installation:
1. To install the files, you have to create a project that include the folder CharacterizationFramework, JUNO_HELPER and MONGODBhandler
inside. Prefer to use programs like pyCharm, liClipse etc. 
2. For the integrity check, you have to put the file LinkedList.cpp in this path /media/oldDisk1/root/integrity_check_scripts of the
juno board files through WinSCP. Then, you have to compile the file with the following command:
g++ LinkedList.cpp -o LinkedList -std=c++11

Run:
To run integrity check, you have to run the file \CharacterizationFramework\src\_init_.py and set as a parameter an input file.
For example an input file that you can use is \CharacterizationFramework\inputs\asioko01junoA53_virus.json.

To get the output, you have to run the program printPassSDCcrashes.py  .

To be able to use the new version of the integrity check, you have to set the boolean value measureIntegrity to true. This parameter
is part of the executor.py file (measureIntegrity is set to true by default).
