import numpy as np
import os

import tensorflow as tf

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

# Task 2) Load Traffic sign data for deep neural network processing.

# Defining parameters for loader..
batch_size = 32
img_height = 64
img_width = 64
data_dir = ".\GTSRB_subset_2"

train_ds = tf.keras.utils.image_dataset_from_directory( data_dir,
                                                        validation_split=0.2,
                                                        subset="training",
                                                        seed=123,
                                                        image_size=(img_height, img_width),
                                                        batch_size=batch_size )

print('\n')

val_ds = tf.keras.utils.image_dataset_from_directory(data_dir,
                                                     validation_split=0.2,
                                                     subset="validation",
                                                     seed=123,
                                                     image_size=(img_height, img_width),
                                                     batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)


plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")

print('\n')

for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break


# Task 3) Define the network in Keras.

# Configuring the dataset for 
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# Defining the model
model = tf.keras.models.Sequential()

# Normalization of the images
model.add(tf.keras.layers.Rescaling(1./255))

# Flatten the input image to 1D vector
model.add(tf.keras.layers.Flatten(input_shape=(64,64,3)))

# Add hidden layers
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dense(100,activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid')) # Output layer

model.build(input_shape=(None, 64, 64, 3)) # Build model 
print(model.summary())



# Task 4) Compile and train the net. (

model.compile(optimizer='SGD',
              loss=tf.keras.losses.BinaryCrossentropy(), metrics=["accuracy"])


history = model.fit(train_ds, validation_data=val_ds, epochs=10)


print(f'Accuracy: {history.history["accuracy"][-1]}')

plt.plot(history.history['loss'])