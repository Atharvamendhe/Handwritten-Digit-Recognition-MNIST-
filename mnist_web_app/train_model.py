# train_model.py
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import tensorflow as tf
import os

# Optional: disable file locking issues on some systems
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

# 1) Load & preprocess
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test  = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

# 2) Data augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.08,
    height_shift_range=0.08,
    zoom_range=0.08
)
datagen.fit(x_train)

# 3) Build model
def make_model():
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
        BatchNormalization(),
        MaxPooling2D((2,2)),

        Conv2D(64, (3,3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2,2)),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

model = make_model()
model.summary()

# 4) Callbacks
checkpoint = ModelCheckpoint(
    "mnist_cnn_model.keras", monitor="val_accuracy",
    save_best_only=True, verbose=1
)
early = EarlyStopping(monitor="val_accuracy", patience=6, restore_best_weights=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1)

# 5) Train
batch_size = 64
epochs = 25

history = model.fit(
    datagen.flow(x_train, y_train, batch_size=batch_size),
    steps_per_epoch = x_train.shape[0] // batch_size,
    validation_data = (x_test, y_test),
    epochs=epochs,
    callbacks=[checkpoint, early, reduce_lr]
)

print("Training finished. Best model saved to mnist_cnn_model.keras")

