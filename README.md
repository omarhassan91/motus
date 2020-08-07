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

# Manually Setting up Motus
In case `motus_setup.sh` does not work, here are some steps to manually setup Motus:

## (1) Install Dependencies
Make sure that you have numpy, pandas, and tensorflow installed using the following commands:

`pip3 install numpy`

`pip3 install pandas`

`pip3 install tensorflow==1.5` If you have a version newer than tensorflow 1.5, then our `song_model.py` script might throw an error

## (2) Run Song Model
The second step to setting up Motus is to run the song classification model using the command:

`python3 src/song_model.py`

### How the Song Model Works

This scripts collects the songs from our playlist on Spotify, trains the classification model, and runs all of the songs through the model to map them to emotions.  

We use the Spotify for Developers API to access our playlist, which we are using to represent the Motus song library.  The Spotify API also sends back the features of each song, and we use specifically the 3 features related to mood for our model.  Those features are **danceability**, **energy**, and **valence**.

To see the descriptions of the song features that Spotify API provides us, visit the reference docs here: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

Our song classification model takes in the three features: danceability, energy, and valence, and outputs an emotion that best fits to each song.  The emotions it outputs are the same emotions that the facial recognition/emotions recognition model outputs: **happy**, **sad**, **neutral**, **angry**, **surprised**.

You only need to run the *song_model.py* script once, because the songs only need to be classified once. Their classifications are then stored in a json file, which is accessed when finding a song that best matches the image uploaded.  Once you see a .json file in the /src directory, your model is all set and you are ready to run `run_detection.sh`.


# Optional Personalizations

Don't like the songs Motus recommends? Easy fix!  Here are some quick steps to take:

## Step 1: Make a playlist on Spotify

Put all of the songs that you like on this playlist.  Make it big.

## Step 2: Connect your playlist with Motus

On the Spotify desktop app, go to your playlist.  There should be a button with 3 dots near the top of the page. Click on the 3 dots, go to Share, and click "Copy Spotify URI". When you next paste from your clipboard, you should see something like "spotify:playlist:0sxxPBp8iOUBSuoj1pPkUI" The gibberish after playlist, in this case 0sxxPBp8iOUBSuoj1pPkUI, is your playlist's Spotify id.

Go into the file `src/spotify_api_work.py`. At the top of the file you should see a line that says `playlist_id = '0sxxPBp8iOUBSuoj1pPkUI'`.  Replace 0sxxPBp8iOUBSuoj1pPkUI with your playlist's Spotify id.  Now Motus will output songs from your own library

### Step 3 (OPTIONAL): Train model to your preferences

If you think Motus is outputting the right songs but at the wrong times, go into the `src/model_data.py` file and check out the training and testing data.  If you associate a song with a different mood, then go ahead and change it. If you want to add your own songs to the training data, add them to the end of the dictionary using the format `{'song_name:mood'}`  Make sure the songs added to the training and testing data are also in your playlist.

# Enjoy

We hope you have a great time using Motus! 

