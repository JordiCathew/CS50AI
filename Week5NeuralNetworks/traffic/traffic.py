import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    # Required dimensions of the images
    dim = (IMG_WIDTH, IMG_HEIGHT)

    # We use os.path.join to get all of the paths to the directories inside data_dir, since we
    # know the name of each subdirectory we just use a for loop and pass the names
    # as an argument later.
    for category in range(NUM_CATEGORIES):
        category_dir = os.path.join(data_dir, str(category))
        print("category: ", category_dir)
        # Now we must follow the category_dir path and iterate through the files.
        for file in os.listdir(category_dir):
            #We get the path for each image and we read the image.
            img = cv2.imread(os.path.join(category_dir, str(file)))
            # We resize the image to the specified size.
            resized_img = cv2.resize(img, dim)
            images.append(resized_img)
            labels.append(category)
     
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        # Convolutional layer. Learn 48 filters using a 3x3 kernel.
        tf.keras.layers.Conv2D(
            48, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        # A smaller pool size can retain more of the fine-grained details in the data.
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                
        tf.keras.layers.Conv2D(
            48, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Flatten units
        tf.keras.layers.Flatten(),

        # Add a hidden layer with 128 units and a dropout that randomly drops out half from this
        # hidden layer, to prevent overfitting.
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.5),

        # Add an output layer with output units for all 43 categories
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])
    
    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()