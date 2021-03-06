# -*- coding: utf-8 -*-
"""ML RPS Submission.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G-Br7RpdpJ5ChNWsSxubZPEdyAcJBRen

Nama  : Wahyu Septiadi

Email : wahyusptd@gmail.com
"""

# Commented out IPython magic to ensure Python compatibility.
import tensorflow as tf
import zipfile,os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from google.colab import files
from keras.preprocessing import image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

!wget --no-check-certificate \
  https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip -O /tmp/rockpaperscissors.zip

# melakukan ekstraksi pada file zip
local_zip = '/tmp/rockpaperscissors.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('/tmp')
zip_ref.close()

# base direktori
base_dir = '/tmp/rockpaperscissors/rps-cv-images'

# image generator (preprocessing data, pelabelan sampel otomatis, dan augmentasi gambar)
train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,                    
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'wrap',
                    zoom_range=0.2,
                    validation_split=0.4) # data validasi 40 % dari data training

validation_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,                    
                    horizontal_flip=True,
                    shear_range = 0.2,
                    fill_mode = 'wrap',
                    zoom_range=0.2,)

# pembagian class (class index 0 = paper, class index 1 = rock, class index 2 = scissors)
train_generator = train_datagen.flow_from_directory(
        base_dir,  # direktori data latih
        target_size=(150, 150),
        shuffle = True,
        class_mode='categorical',
        subset = 'training')
 
validation_generator = train_datagen.flow_from_directory(
        base_dir, # direktori data validasi
        target_size=(150, 150),
        shuffle = True,
        class_mode='categorical',
        subset = 'validation')

# melakukan model sequential
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(130, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax') # 3 layer
])

# menjalankan model dengan metrics accuracy
model.compile(loss='binary_crossentropy',
              optimizer=tf.optimizers.Adam(),
              metrics=['accuracy'])

# melatih model dengan metode fit (selama [+-] 12 menit)
model.fit(
      train_generator,
      steps_per_epoch=25,  
      epochs=22, 
      validation_data=validation_generator, 
      validation_steps=5, 
      verbose=2)

# pengujian gambar
uploaded = files.upload()
 
for fn in uploaded.keys():
 
  path = fn
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
 
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10) # semisal nilai classes [[1. 0. 0.]] di analogikan [[paper. rock. scissors.]]
  check = np.argmax(classes) # output = PAPER
  print(fn)

  if check==0:
    print('paper')
  elif check==1:
    print('rock')
  else:
    print('scissors')