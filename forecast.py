import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

def prepare_lstm_data(df, sequence_length=10):
    df = df.sort_values('date')
    data = df['amount'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i])
    return np.array(X), np.array(y), scaler

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def forecast_spending(df, epochs=10):
    X, y, scaler = prepare_lstm_data(df)
    model = build_lstm_model((X.shape[1], X.shape[2]))
    model.fit(X, y, epochs=epochs, verbose=0)
    prediction = model.predict(X[-1].reshape(1, X.shape[1], X.shape[2]))
    return scaler.inverse_transform(prediction)[0][0]
