# nhanes_tools

## download all data in one click
run data_download.py，all .xpt data in continuous NHANES（1999-2018） will be downloaded automatically and saved in ./data

the data will be arranged as：

├─data
│  ├─1999-2000
│  │  ├─Demographics data
│  │  │      DEMO Data
│  │  │      
│  │  ├─Dietary data
│  │  │      DRXFMT Data
│  │          ....
│  │  │      
│  │  ├─Examination data
│  │  │      AUX1 Data
│  │  │      AUXAR Data
│  │          ....
│  │  │      
│  │  ├─Laboratory data
│  │  │      L02HBS Data
│  │  │      L02HPA_A Data
│  │          ....
│  │  │      
│  │  └─Questionnaire data
│  │          ACQ Data
│  │          ALQ Data
│  │          ....
│  │          
│  ├─2001-2003
│  │  ├─Demographics data
│  │  │      DEMO_B Data
│  │  │      
│  │  ├─Dietary data
│  │  │      DRXFMT_B Data
│  │          ....
