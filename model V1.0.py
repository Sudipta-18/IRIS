# -*- coding: utf-8 -*-
"""Model V1.0

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NGHFiPSaD_Trya8PIvksAkzWp8KeQrFv
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from tqdm import tqdm

path = '/content/drive/My Drive/Anomaly detection/UCF/Anomaly-Detection-Dataset/Training-Normal-Videos-Part-1'
path_anom = '/content/drive/My Drive/Anomaly detection/UCF/Anomaly-Detection-Dataset/Anomaly-Videos-Part-1/Abuse'
model_path = '/content/drive/My Drive/Model'

batch = 5
img_dim = (128, 128)

def load(pth):
  videos = []
  vid_len = []
  for vd in pth:
    vid = cv2.VideoCapture(os.path.join(path, vd))
    frames = []
    cnt = 0
    
    while vid.isOpened():
      ret, frame = vid.read()
      if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
      cnt += 1
      gray = cv2.resize((cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))/256, img_dim).reshape([img_dim[0], img_dim[1], 1])
      #cv2.imshow(gray)

      frames.append(gray)
      if cnt >= 8000:
        break
      #if cv2.waitKey(25) & 0xFF == ord('q'): 
      # break
    vid.release()
    #cv2.destroyAllWindows()
    videos.append(frames)
    vid_len.append(cnt)
  return videos, vid_len

def augment(videos, stride, vid_len, frames = 10):
  agmted = np.zeros((frames, img_dim[0], img_dim[1], 1))
  cnt = 0
  clips = []
  for vid in range(len(vid_len)):
    for strd in stride:
      for frm in range(0, vid_len[vid], strd):
        agmted[cnt, :, :, :] = videos[vid][frm]
        cnt += 1
        if cnt == frames:
          clips.append(agmted)
          cnt = 0
  return np.array(clips)

"""keras"""

!pip install keras-layer-normalization

import keras
from keras.layers import Conv2DTranspose, ConvLSTM2D, BatchNormalization, TimeDistributed, Conv2D
from keras.models import Sequential, load_model
from keras_layer_normalization import LayerNormalization
#import tensorflow as tf
#import tf.compat.v1.keras.backend as K
#print(tf.compat.v1.keras.backend.tensorflow_backend._get_available_gpus())
#import keras
#config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 8} ) 
#sess = tf.Session(config=config) 
#keras.backend.set_session(sess)

def model(reload_model=True):
    training_set = videos
    if reload_model:
        seq = load_model('/content/drive/My Drive/Model',custom_objects={'LayerNormalization': LayerNormalization})
    else:   
      seq = Sequential()
      seq.add(TimeDistributed(Conv2D(128, (11, 11), strides=4, padding="same"), batch_input_shape=(None, frames, img_dim[0], img_dim[1], 1)))
      seq.add(LayerNormalization())
      seq.add(TimeDistributed(Conv2D(64, (5, 5), strides=2, padding="same")))
      seq.add(LayerNormalization())
      # # # # #
      seq.add(ConvLSTM2D(64, (3, 3), padding="same", return_sequences=True))
      seq.add(LayerNormalization())
      seq.add(ConvLSTM2D(32, (3, 3), padding="same", return_sequences=True))
      seq.add(LayerNormalization())
      seq.add(ConvLSTM2D(64, (3, 3), padding="same", return_sequences=True))
      seq.add(LayerNormalization())
      # # # # #
      seq.add(TimeDistributed(Conv2DTranspose(64, (5, 5), strides=2, padding="same")))
      seq.add(LayerNormalization())
      seq.add(TimeDistributed(Conv2DTranspose(128, (11, 11), strides=4, padding="same")))
      seq.add(LayerNormalization())
      seq.add(TimeDistributed(Conv2D(1, (11, 11), activation="sigmoid", padding="same")))
    print(seq.summary())
    seq.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=1e-4, decay=1e-5, epsilon=1e-6))
    seq.fit(training_set, training_set,
            batch_size=frames, epochs=epochs, shuffle=False)
    seq.save('/content/drive/My Drive/Model')
    #plt.imshow(seq.predict(videos))
    return seq

lst = os.listdir(path)

for s in tqdm(range(110, len(lst), batch)):
  if s+batch <= len(lst):
    pths = lst[s:s+batch]
    videos, vid_len = load(pths)
    frames = 10
    epochs = 10
    videos = augment(videos, [1, 2], vid_len,frames)
    if s == 0:
      seq = model(reload_model = False)
    else:
      seq = model(reload_model=True)
    videos = None
    video_len = None

def load_mdl(model_path):
  return load_model(model_path,custom_objects={'LayerNormalization': LayerNormalization})

def get_single_test(path_anom):
    sz = 400
    test = np.zeros(shape=(sz, 128, 128, 1))
    cnt = 0
    x = 0
    for f in os.listdir(path_anom):
        vid = cv2.VideoCapture(os.path.join(path_anom, f))
        cnt = 0
        while vid.isOpened:
          ret, img = vid.read()
          if cnt >= 0 and ret:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            test[cnt, :, :, 0] = cv2.resize(img/256 , (128, 128))
          cnt = cnt + 1
          if cnt == sz:
            break
        vid.release()
        break
    return test

def evaluate():
    model = load_mdl(model_path)
    print("got model")
    test = get_single_test(path_anom)
    print("got test")
    sz = test.shape[0] - 10
    sequences = np.zeros((sz, 10, img_dim[0], img_dim[1], 1))
    # apply the sliding window technique to get the sequences
    for i in range(0, sz):
        clip = np.zeros((10, img_dim[0], img_dim[1], 1))
        for j in range(0, 10):
            clip[j] = test[i + j, :, :, :]
        sequences[i] = clip
    test = None
    # get the reconstruction cost of all the sequences
    reconstructed_sequences = model.predict(sequences,batch_size=4)
    sequences_reconstruction_cost = np.array([np.linalg.norm(np.subtract(sequences[i],reconstructed_sequences[i])) for i in range(0,sz)])
    sa = (sequences_reconstruction_cost - np.min(sequences_reconstruction_cost)) / np.max(sequences_reconstruction_cost)
    sr = 1.0 - sa
    #print(sr)
    if (sr<=0.93).any():
      print('Anomaly Detected')
    else:
      print('everything is normal')
    # plot the regularity scores
    plt.plot(sr)
    plt.ylabel('regularity score Sr(t)')
    plt.xlabel('frame t')
    plt.show()

evaluate()

img_dim = (128, 128)
#videos, vid_len = load(os.listdir('/content/drive/My Drive/Anomaly detection/UCF/Anomaly-Detection-Dataset/Anomaly-Videos-Part-1/Abuse')[0:1])

pht = seq.predict(vid)



vid.shape

i = 2
plt.imshow(np.squeeze(pht[0][i]))

plt.imshow(np.squeeze(vid[0][i]))

a = np.ones(5)
a[3] = 0
print(a)
if a.any():
  print('True')
else:
  print('False')

print(a<=0.5)

|