# Motus

Application that uses OpenVINO and the Spotify API to deliver song recommendations based on facial moods. 

This application uses a pretrained model in OpenVINO that can classify 5 different emotions: 

* **happy, sad, angry, surprised, neutral**

**##############################################################**

**THE FOLLOWING INSTRUCTIONS WERE USED WITH UBUNTU 18.04**

**##############################################################**

Please visit our DevMesh page as well: https://devmesh.intel.com/projects/motus


# Setting up OpenVINO

* First, download the latest build of the OpenVINO Toolkit from here: https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/choose-download.html (*we used the Linux distribution*)



* Follow the steps of the OpenVINO Installation from here: https://docs.openvinotoolkit.org/2020.3/_docs_get_started_get_started_linux.html

# Setting up Motus for the first time

Once you've downloaded Motus for the first time, you will need to everything up:

	* Downloading the OpenVINO Pretrained Models
	* Modifying and Building the Face Detection Demo
	* Ensuring image directory is updated in run file

Luckily, running `sudo ./motus_setup.py` will complete the first two steps for you. In case *motus_setup.py* does not work, additional instructions on manually setting up Motus are provided below.

# Before running application

Make sure that you have an image taken of your face (using webcam or smartphone) and saved on your machine. In order for this to work, please change the input image directory in the *run_detection.sh* file.

* Also please make sure that all other directories match the file directories on your machine. The file names may vary with newer versions of the OpenVINO Toolkit

# Running the application

`./run_detection.sh` will invoke the Interactive Face Detection Demo, which uses your input image, as well as the *face-detection-adas-0001* and *emotions-recognition-retail-0003* models. The output of the
script should be a song recommendation using our own offline Tensorflow classification model.

# (1) Downloading the OpenVINO Pretrained Models

Motus uses two pre-trained models that are available in the OpenVINO Open Model Zoo: *emotions-recognition-0003* and *face-detection-adas-0001*.

* **emotions-recognition-0003:** https://docs.openvinotoolkit.org/2019_R1/_emotions_recognition_retail_0003_description_emotions_recognition_retail_0003.html
* **face-detection-adas-0001:** https://docs.openvinotoolkit.org/2019_R1/_face_detection_adas_0001_description_face_detection_adas_0001.html

`sudo python3 /opt/intel/openvino_2020.4.287/deployment_tools/model_downloader/downloader.py --name emotions-recognition-retail-0003 --precision FP32`

`sudo python3 /opt/intel/openvino_2020.4.287/deployment_tools/model_downloader/downloader.py --name face-detection-adas-0001 --precision FP32`

# (2) Modifying and Building the Face Detection Demo 

For this application to work, we will be leveraging the Face Detection Demo that's available in the OpenVINO 'demos' library. The location of the Demo's source code is here: `/opt/intel/openvino_2020.4.287/inference_engine/demos/interactive_face_detection_demo`.

The first step is to copy the modified *visualizer.cpp* file available into this directory. Then, we will need to build the demo.

`cd /opt/intel/openvino_2020.4.287/inference_engine/demos/`

`sudo ./build_demos.sh`

Now, all the executable demos should be contained in the directory `~/omz_demos_build/intel64/Release/`
