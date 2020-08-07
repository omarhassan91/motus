#!/bin/bash

pip3 install pandas
pip3 install tensorflow==1.5

#Source Environment Variables for OpenVINO First
source /opt/intel/openvino_2020.4.287/bin/setupvars.sh

#Change visualizer.cpp source code
cp bin/visualizer.cpp /opt/intel/openvino_2020.4.287/inference_engine/demos/interactive_face_detection_demo/

#Compile song classification model with current dataset
python3 src/song_model.py

#Download the correct models from OpenVINO
python3 /opt/intel/openvino_2020.4.287/deployment_tools/tools/model_downloader/downloader.py --name emotions-recognition-retail-0003 --precision FP32
python3 /opt/intel/openvino_2020.4.287/deployment_tools/tools/model_downloader/downloader.py --name face-detection-adas-0001 --precision FP32

echo " "
echo " @------------------------@"
echo " | Motus Setup Complete!  |"
echo " @------------------------@"
echo " "
