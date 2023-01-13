# What did I try?
To begin with I tried with a structure almost identical to the one used in the source code of handwriting.py, and the results were pathetic-0.05 accuracy- so, I decided
to add another layer to see if the accuracy improved or if the problem was something else
than the number of units. 

Now the accuracy improved by a lot, but I decided to try if I could get to a higher accuracy, but instead of adding another layer (two seemed like they worked fine) I decided to increase the number of filters to read by half of what they previously were (32 previously, 48 after). The accuracy improved, but I thought that I could do better so finally I decided to increase the number of units in the hidden layer by doubling of what they previously were (128 previously, 256 after) but the results were worse that in the previous runs.

## What worked well?
After adding a second the layer the accuracy improved significantly, around 95 percent accuracy, after applying more filters (48 instead of 32), the model improved around 1-2% percent, to 96-97%. After the change of the number of units in the hidden layer the results were around the same 96% or worse, in conclusion: The best model that I could get was the third one: 

```python

        model = tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(
                48, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
                    
            tf.keras.layers.Conv2D(
                48, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
            ),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),


            tf.keras.layers.Flatten(),

            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.5),


            tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
        ])
```

## What didn't work well?
One layer was extremely inefficient, after adding another the results were consistently more
precise, after adding more units in the hidden layer, the results were worse than in previous runs with less units.
