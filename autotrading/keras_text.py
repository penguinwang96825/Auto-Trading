import os
import warnings
import logging
import transformers
import data_handler
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")
logger = tf.get_logger()
logger.setLevel(logging.ERROR)


def build_attention_model(MAXLEN=32, VOCAB=10000, EMBED_SIZE=100, RNN_UNIT=64, N_OUT=2):
    # tf.get_logger().setLevel('INFO')
    # tf.keras.backend.clear_session()
    input_ = tf.keras.layers.Input(shape=(MAXLEN, )) # [BS, MAXLEN]
    words = tf.keras.layers.Embedding(
        VOCAB,
        EMBED_SIZE,
        input_length=MAXLEN,
        embeddings_initializer="lecun_uniform")(input_) # [BS, MAXLEN, EMBED_SIZE]
    sen = tf.keras.layers.LSTM(RNN_UNIT, return_sequences=True)(words) # [BS, MAXLEN, RNN_UNIT]

    # Attention Mechanism
    attention_pre = tf.keras.layers.Dense(1)(sen) # [BS, MAXLEN, 1]
    attention_probs = tf.nn.softmax(attention_pre, axis=1) # [BS, MAXLEN, 1]
    attention_mul = tf.keras.layers.Lambda(lambda x: tf.keras.backend.sum(x[0]*x[1], axis=1))([attention_probs, sen]) # [BS, RNN_UNIT]

    # Fully Connected
    output = tf.keras.layers.Dense(128, activation="relu")(attention_mul) # [BS, 128]
    output = tf.keras.layers.Dense(N_OUT, activation="relu")(output) # [BS, N_OUT]
    model = tf.keras.Model(input_, output)
    return model


def main():
    data = pd.read_csv("./data/domesticnews_reuters.csv")
    data = data_handler.remove_unnamed_col(data)
    data = data.loc[(data["Category"] == "Business News") | (data["Category"] == "World News")]
    data = data.sample(frac=1)
    data['Title'] = data['Title'].map(str)
    train_size = int(len(data) * .8)
    train_posts = data['Title'][:train_size]
    train_tags = data['Category'][:train_size]
    test_posts = data['Title'][train_size:]
    test_tags = data['Category'][train_size:]

    # Deal with text data
    tokenizer = tf.keras.preprocessing.text.Tokenizer(
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=" ")
    tokenizer.fit_on_texts(train_posts)
    X_train = tokenizer.texts_to_matrix(train_posts)
    X_test = tokenizer.texts_to_matrix(test_posts)
    X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, maxlen=32)
    X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, maxlen=32)

    # Deal with text label
    encoder = LabelEncoder()
    labels = encoder.fit(train_tags)
    y_train = encoder.transform(train_tags)
    y_test = encoder.transform(test_tags)
    num_classes = 2
    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    model = build_attention_model(N_OUT=num_classes)
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["acc"])
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))


if __name__ == "__main__":
    main()
