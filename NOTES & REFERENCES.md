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

Freguesias files INFO:
- Header index row.
- Each party's info is split among three columns: accronym, votes, 0's column.
- The four columns preceeding the first party's information are total votes data.
- First column contains both Freguesia code and name, must be split.
- First column with party accronym, per file: {76:6, 79:8, 80:8, 83:8, 85:8, 87:8, 91:8, 95:8}