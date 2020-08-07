import numpy as np
import tensorflow as tf
import os
import spotify_api_work as spot
import model_data as md
import json
print('starting...')
def prepare_data(data_dict):
    valence = []
    dance = []
    energy = []
    labels = []
    x_train = []
    y_train = []
    for song, label in data_dict.items():
        if song in spot.imp_features.keys():
            valence.append(spot.imp_features[song]['valence'])
            dance.append(spot.imp_features[song]['danceability'])
            energy.append(spot.imp_features[song]['energy'])
            labels.append(label)

    x_train = {'valence':np.array(valence), 'danceability':np.array(dance), 'energy': np.array(energy)}
    y_train = np.array(labels)
    return x_train, y_train


def input_fn(features, labels, training=True, batch_size=15):
    """An input function for training or evaluating"""
    # Convert the inputs to a Dataset.
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))

    # Shuffle and repeat if you are in training mode.
    if training:
        dataset = dataset.shuffle(1000).repeat()
    
    return dataset.batch(batch_size)


feats, labels = prepare_data(md.train)
test_data, test_labels = prepare_data(md.test)
batch = input_fn(feats, labels)
# Feature columns describe how to use the input.
my_feature_columns = []
for key in feats.keys():
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))

# Build a DNN with 2 hidden layers with 30,10 hidden nodes each.
classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    # Three hidden layers of 30,10 nodes respectively.
    hidden_units=[30, 10],
    # The model must choose between 5 classes.
    n_classes=5)

# Train the Model.
classifier.train(
    input_fn=lambda: input_fn(feats, labels, training=True),
    steps=5000)

eval_result = classifier.evaluate(
    input_fn=lambda: input_fn(test_data, test_labels, training=False))

print('\nTest set accuracy: {accuracy:0.3f}\n'.format(**eval_result))


# Generate predictions from the model

pred_songs = []
valence = []
dance = []
energy = []
pred_labels = []
for song, f in spot.imp_features.items():
    pred_songs.append(song)
    valence.append(f['valence'])
    dance.append(f['danceability'])
    energy.append(f['energy'])
pred_feats = {'valence':np.array(valence), 'danceability': np.array(dance), 'energy':np.array(energy)}



def input_fn_pred(features, batch_size=256):
    """An input function for prediction."""
    # Convert the inputs to a Dataset without labels.
    return tf.data.Dataset.from_tensor_slices(dict(features)).batch(batch_size)


predictions = classifier.predict(
    input_fn=lambda: input_fn_pred(pred_feats))
index = 0
song_emotions = {}
for pred_dict in predictions:
    class_id = pred_dict['class_ids'][0]
    probabilities = pred_dict['probabilities']
    probabilities = [str(x) for x in probabilities]
#     print("Song: {} was placed into class: {} with percentages: {}".format(pred_songs[index], class_id, probabilities))
    song_emotions[pred_songs[index]] = probabilities
    index +=1

json = json.dumps(song_emotions)
f = open("src/song_emotions.json", "w")
f.write(json)
f.close()

