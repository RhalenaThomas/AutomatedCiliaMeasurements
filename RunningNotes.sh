Running notes

# neurons - all images have the same conversion factor

python acm/script.py -i /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/Neurons_cp_outs_csvs/ -o /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/Neurons/ --scale 3.52


# npc have 2 different magnifications 2.64 and 4.288

# input directory 1
/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/NPC_cp_outs_csvs/NPC_2.64px

# input directory 2
/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/NPC_cp_outs_csvs/NPC_4.288

# output directory 1
/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/NPC/NPC_264

#output directory 2
/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/NPC/NPC_4288


# NPC 1

python acm/script.py -i /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/NPC_cp_outs_csvs/NPC_2.64px -o /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/NPC/NPC_264 --scale 2.64

# NCP 2 - error?
python acm/script.py -i /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/NPC_cp_outs_csvs/NPC_4.288 -o /Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/PythonPipeline_outputs/NPC/NPC_4288 --scale 4.28

# error message
Traceback (most recent call last):
  File "/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/acm/script.py", line 284, in <module>
    main()
  File "/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/acm/script.py", line 33, in main
    c2c_df = c2c(nucleus_df, centriole_df, cilia_df)
  File "/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/acm/script.py", line 128, in c2c
    centriole_group = grouped_centriole.get_group(key)
  File "/Users/rhalenathomas/GITHUB/AutomatedCiliaMeasurements/venv/lib/python3.9/site-packages/pandas/core/groupby/groupby.py", line 817, in get_group
    raise KeyError(name)
KeyError: 9

# I'm exciting and entering venv
# still the same problem - The csv files look fine but I'll check again
# The csv files were correctly made but one image had no centrioles detected - it appears there must be something measured
# this is something that should be adjusted in the code to catch this error

