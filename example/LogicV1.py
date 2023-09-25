import pickle
import numpy as np


class LogicV1(object):
    def __init__(self):
        self.model_path = "logic.mdl"
        # load model
        self.model = self.load_model()

    def load_model(self):
        with open(self.model_path, "rb") as pickle_file:
            model = pickle.load(pickle_file)
        return model

    def predict(self, data):
        result = np.array([])
        try:
            data_X = data['data_X']
            result = self.model.predict(data_X)
        except Exception as e:
            print(e)
        return result.tolist()
