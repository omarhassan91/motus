import os
from argparse import ArgumentParser
import pandas as pd
import random
import json
emotionData = []

CUR_DIR=os.path.dirname(os.path.realpath(__file__))

os.chdir(CUR_DIR)

with open("../output/output.txt", "r") as fid:
	lines = fid.read().splitlines()
	for line in lines:
		if "Emotion Names" in line:
			emotionData.append(line.split(": ")[-1])

#print(emotionData[0])
#print(emotionData[1])
#print(emotionData[2])
#print(emotionData[3])
#print(emotionData[4])


neutral = float(emotionData[0].split(" ")[-1])
happy = float(emotionData[1].split(" ")[-1])
sad = float(emotionData[2].split(" ")[-1])
surprise = float(emotionData[3].split(" ")[-1])
angry = float(emotionData[4].split(" ")[-1])

#print(neutral)
#print(happy)
#rint(sad)
#happy = emotionData[1]
#sad = emotionData[2]
#surprise = emotionData[3]
#angry = emotionData[4]

#with open("song_dictionary.txt", "r") as f:
#	lines = f.read()
#	lines = eval(lines)

emotions = {"neutral" : neutral, "happy" : happy, "sad" : sad, "surprise" : surprise, "angry": angry}
emo_dict = {'happy' : 0, 'sad' : 1, 'neutral' : 2, 'angry': 3, 'surprise': 4}
currentEmotion = max(emotions, key = emotions.get)

with open('../src/song_emotions.json') as f:
    song_emotions = json.load(f)

#print(currentEmotion)
playlist = {}
for song, str_emos in song_emotions.items():
    emos = [float(x) for x in str_emos]
    song_emo = max(range(len(emos)), key = emos.__getitem__)
    if emo_dict[currentEmotion] == song_emo:
        diff = abs(happy - emos[0]) + abs(sad - emos[1]) + abs(neutral - emos[2]) + abs(angry - emos[3]) + abs(surprise - emos[4])
        playlist[song] = diff

song_list = sorted(playlist.items(), key = lambda x: x[1], reverse = False)
print("\nCurrent Emotion: " + str(currentEmotion))


print("\nRecommendation: " + song_list[0][0])

