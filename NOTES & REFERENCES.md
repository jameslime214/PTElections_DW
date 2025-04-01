## Notes and References

### To-Do List
- Check versions on main_server.ipynb and myMethods.py -- DONE
- Convert .txt to .csv or .xls for sql file creation -- DONE
- Correct these files -- DONE
- FIX Reading and Cleaning block of main_ddl to only process text files!! -- DONE
- Find headers for FC data files to use in creating their SQL scripts
- Run new sql files in server to upload data to server
**ANNOTATE ALL POINTS ABOVE IN THE REPORT**

### Notes on Extracted Files
Conselhos files:
- Header index row.
- Each party's info is split among three columns: accronym, votes, 0's column.
- The four columns preceeding the first party's information are total votes data.
- First column contains both Freguesia code and name, must be split.
- First column with party accronym, per file: {76:6, 79:8, 80:8, 83:8, 85:8, 87:8, 91:8, 95:8}
  - ar76c: Contains only one column between conselho names and total voting information. This column contains a string of numbers: '500       0' for conselho with no voting information and f'{some amount of 0's}{important number}{single trailing 0}' for every other conselho
  - ar79c and later: Contains 3 columns between conselho name and total votes info. 1st and 3rd are filled with 0's, useless. 2nd contains useful data.

Freguesias files INFO:
- Header index row.
- Each party's info is split among three columns: accronym, votes, 0's column.
- The four columns preceeding the first party's information are total votes data.
- First column contains both Freguesia code and name, must be split.
- First column with party accronym, per file: {76:6, 79:8, 80:8, 83:8, 85:8, 87:8, 91:8, 95:8}
  - ar76f: Contains only one column before total voting information and after freguesia names. Contains only 0's or 500 (followed by spaces and then a final 0) for freguesias without voting information 
  - ar79f and later: 3 columns between freguesia name and total voting information columns. The first of which is important, the latter two are useless because they are filled with 0's.