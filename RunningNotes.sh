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
