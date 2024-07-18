Running notes



# navigate back to the parent directory
cd ../..    # you need to be in the home github repo folder to run the pipeline
source venv/bin/activate



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



# I'm exiting and entering venv
# still the same problem - The csv files look fine but I'll check again
# The csv files were correctly made but one image had no centrioles detected - it appears there must be something measured
# this is something that should be adjusted in the code to catch this error


### Now I will compare different thresholds for centrioles for the NPC and the neurons. 
## I will run each in cellprofiler then each here in the python pipeline.


# I've activated the environment now I need to get all the data paths and set an output
# remember to run from inside the main github folder
# neurons - all images have the same conversion factor

# high threshold Neurons
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NeuronsHighThresh -o /Users/rhalenathomas/Desktop/outs_May3/NeuronsHighThresh --scale 3.52

# Medium threshold Neurons
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NeuronsMedThresh -o /Users/rhalenathomas/Desktop/outs_May3/NeuronsMedThresh --scale 3.52

# Low threshold Neurons
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NeuronsLowThresh -o /Users/rhalenathomas/Desktop/outs_May3/NeuronsLowThresh --scale 3.52


### one folder of NPC only I only rand the 210310 NPC group and this is the 2.64 micron conversion
# High threshold NPC
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NPCHightThresh -o /Users/rhalenathomas/Desktop/outs_May3/NPCHightThresh --scale 2.64

# Med threshold NPC
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NPCMedThesh -o /Users/rhalenathomas/Desktop/outs_May3/NPCMedThesh --scale 2.64

# Low threshold NPC
python acm/script.py -i /Users/rhalenathomas/Desktop/outs_May3/NPCLowThresh -o /Users/rhalenathomas/Desktop/outs_May3/NPCLowThresh --scale 2.64
