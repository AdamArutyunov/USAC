from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input
import os
from keras.models import Sequential
from keras.layers import Dropout, Dense
from keras.optimizers import Adam
from keras.models import model_from_json
import numpy as np
import cv2


class DetailChecker:
    
    def __init__(self):
        # Все загруженные модели в структуре имя-модель
        self.models = {}
        # Текущая выбранная модель
        self.curent_model = None
        # Имя текущей модели
        self.current_model_name = None
        # Модель для получения репрезентаций
        json_file = open(os.getcwd() + '/AIModule/model3Dscanner.json')
        loaded_model_json = json_file.read()
        json_file.close()
        self.GetModel = model_from_json(loaded_model_json)
        self.GetModel.load_weights(os.getcwd() + '/AIModule/model3Dscanner.h5')
        
    def preprocess_image(self, img):
        img = cv2.resize(img,(224, 224))
        img = img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        return img
        
    def load_model(self, modelname):
        '''Загрузка модели'''
        # Проверка, загружена ли модель
        if modelname not in self.models:
            try: 
                ResultModel = Sequential()   
                ResultModel.add(Dense(1000, input_dim=25088, activation='relu'))
                ResultModel.add(Dropout(0.4))
                ResultModel.add(Dense(1000, activation='relu'))
                ResultModel.add(Dropout(0.4))    
                ResultModel.add(Dense(1, activation='sigmoid'))
                ResultModel.compile(loss='binary_crossentropy',
                              optimizer=Adam(lr=1e-5), 
                              metrics=['accuracy'])
                ResultModel.load_weights(os.path.join(os.getcwd() + '/AIModule/models', modelname + '.h5'))
                self.models[modelname] = ResultModel
                
                if self.current_model_name is None:
                    self.set_model(modelname)
                    
            except FileNotFoundError:
                print('Модель не существует')
        else:
            print('Модель уже загружена')
        
    def set_model(self, modelname):
        '''Установка текущей модели'''
        if self.current_model_name != modelname:
            try:
                self.curent_model = self.models[modelname]
                self.current_model_name = modelname
                print('Текущей моделью установлена {}'.format(modelname))
            except KeyError:
                print('Модель не загружена, загружаю...')
                self.add_model(modelname)
            
    def check(self, cv2_object):
        '''Распознавание фото детали'''
        if self.current_model_name is None:
            print('Модель не выбрана')
        else:
            img = self.preprocess_image(cv2_object)
            representation = self.GetModel.predict(img)
            result = self.curent_model.predict(representation)[0][0]
            return (True if result >=.75 else False), round(result, 3)
    
    def models_list(self):
        '''Возвращает список доступных моделей'''
        return list(i.split('.h5')[0] for i in os.listdir(os.getcwd() + '/AIModule/models') if i.endswith('.h5') and 
                    i.split('.h5')[0] not in self.models)
        
    def loaded_model_list(self):
        '''Возвращает список загруженных моделей'''
        return list(self.models.keys())


'''
if __name__ == '__main__':
    checker = DetailChecker()
    checker.load_model(checker.models_list()[0])
    
    img = cv2.imread('72.jpg')
    prediction, result = checker.check(img)
    prediction = checker.current_model_name if prediction else 'Wrong'
    cv2.imshow(prediction + ', ' + str(result) + '    Press any key to exit', img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
'''
