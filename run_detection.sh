#!/bin/bash

DIR=$PWD
CUR_DIR=~/omz_demos_build/intel64/Release/

###-CHANGE PATH OF PIC_DIR TO WHERE YOUR IMAGE IS STORED-###
PIC_DIR=${DIR}/images/angry.jpg #<--------------------------
############################################################

rm ${DIR}/output/detection_data.csv
rm ${DIR}/output/output.txt
rm ${DIR}/src/song_dictionary.txt


cd ${CUR_DIR}

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/data_processing/dl_streamer/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/data_processing/gstreamer/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/opencv/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/ngraph/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/external/hddl_unite/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/external/hddl/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/external/gna/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/external/mkltiny_lnx/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/external/tbb/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/opt/intel/openvino_2020.4.287/deployment_tools/inference_engine/lib/intel64

./interactive_face_detection_demo -i ${PIC_DIR} \
-m ${DIR}/intel/face-detection-adas-0001/FP32/face-detection-adas-0001.xml \
-m_em ${DIR}/intel/emotions-recognition-retail-0003/FP32/emotions-recognition-retail-0003.xml \
-d CPU | tee -a ${DIR}/output/output.txt

python3 ${DIR}/src/spotify_api_work.py >> ${DIR}/src/song_dictionary.txt
python3 ${DIR}/src/parse_deployment_results.py | tee -a ${DIR}/output/detection_data.csv
