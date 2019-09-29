
# coding: utf-8

# In[1]:


from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.layers import Activation
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
import numpy
import pprint
import time
import os
import h5py
import json
#my code
import shared


# In[2]:


class TemperatureClassifier:
    
    loaded_model = ""
    labels_map = dict()
    
    def read_file_contents(self, file_name):
        with open(file_name,'r') as file_to_read:
            return file_to_read.read()

    def initialize(self):
        #create new model directory
        base_path = "assets/trained-models"
        base_path_model = "{}/{}".format(base_path, self.read_file_contents("{}/temperature-model.index".format(base_path)))

        print("Resolved base_path_state_model to: ", base_path_model)

        #resolve paths to files
        json_model_file = "{}/model.json".format(base_path_model)
        weight_model_file = "{}/model.h5".format(base_path_model)
        this_model_labels_path = ("{}/labels.json".format(base_path_model))

        print("Loading model from: ", json_model_file)
        print("Loading weights from: ", weight_model_file)
        print("Loading labels from: ", this_model_labels_path)

        #load model
        model_json = self.read_file_contents(json_model_file)
        self.loaded_model = model_from_json(model_json)
        #load weights
        self.loaded_model.load_weights(weight_model_file)

        #compile the model
        self.loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        #load labels
        labels_json = self.read_file_contents(this_model_labels_path)
        self.labels_map = json.loads(labels_json)
        

        print("Model successfully Loaded.")


# In[3]:


def getTestInput():
    day=26
    extHumidity=64
    extTemp=30
    fanspeed=0
    hour=19
    loungeHumidity=46
    loungeTemp=22
    minute=0
    mode=1
    month=10
    pirstatus=5
    
    return numpy.array([day,extHumidity,extTemp,fanspeed,hour,loungeHumidity,loungeTemp,minute,mode,month,pirstatus]).reshape((1,11))


# In[4]:


def test():
    classifier = TemperatureClassifier()
    classifier.initialize()

    input  = getTestInput()
    print(input)
    
    result = classifier.loaded_model.predict(input)
    for res in result:
        print(res)
        
    result = classifier.loaded_model.predict_classes(input)
    for res in result:
        print("class: ",res, "temperature: ", classifier.labels_map[str(res)])


# In[5]:


if __name__ == '__main__':
    test()

