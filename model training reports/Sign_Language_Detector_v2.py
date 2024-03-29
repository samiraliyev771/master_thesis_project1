#!/usr/bin/env python
# coding: utf-8

# ##### Reference: https://www.kaggle.com/rafaeletereo/convolutional-model

# ### Importing Libraries

# In[1]:


import numpy as np
import time
import random
# data visualization and plotting imports
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import os
from sklearn.utils.multiclass import unique_labels
import cv2
import matplotlib.pyplot as plt
import seaborn as sn

# deep learning imports
# import keras
import tensorflow
layers = tensorflow.keras.layers
BatchNormalization = tensorflow.keras.layers.BatchNormalization
Conv2D = tensorflow.keras.layers.Conv2D
Flatten = tensorflow.keras.layers.Flatten
MaxPooling2D = tensorflow.keras.layers.MaxPooling2D
Dropout = tensorflow.keras.layers.Dropout
Dense = tensorflow.keras.layers.Dense
ImageDataGenerator = tensorflow.keras.preprocessing.image.ImageDataGenerator
Sequential = tensorflow.keras.Sequential

TensorBoard = tensorflow.keras.callbacks.TensorBoard
ModelCheckpoint = tensorflow.keras.callbacks.ModelCheckpoint
Adam = tensorflow.keras.optimizers.Adam
regularizers = tensorflow.keras.regularizers
categorical_crossentropy = tensorflow.keras.losses
K = tensorflow.keras.backend
plot_model = tensorflow.keras.utils.plot_model


# word library import
from nltk.corpus import words


os.environ['KMP_DUPLICATE_LIB_OK']='True'


# ### Global Variables 

# In[2]:


# setting up global variables
DATADIR = "../master_thesis_project1/asl-alphabet/asl_alphabet_train/"   #training data directory
CATEGORIES = ['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
              'N', 'nothing', 'O', 'P', 'Q', 'R', 'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
test_dir = "../master_thesis_procet1/asl-alphabet/asl_alphabet_test"     #testing data directory
#own_dir = "../input/ishaan/ishaan_pics/ishaan_pics"


# ### Getting Training Data

# #### Testing experiment on the image array

# In[3]:


from matplotlib import pyplot as plt
test_array = []
print('generating test_array data')
path = os.path.join(DATADIR, CATEGORIES[0])
print(path)
#sorted_files = sorted(os.listdir(path)[0:10])
for img_tst in sorted(os.listdir(path)[0:10]):
    img_tst_array = cv2.imread(os.path.join(path,img_tst), cv2.IMREAD_COLOR)
    print(img_tst)
    plt.imshow(img_tst_array)
    plt.show()
    test_array.append([img_tst_array, CATEGORIES.index('A')])
#print(test_array)


# In[4]:


def create_training_data(modeltype):
    '''This function can run for each model in order to get the trainin data from the filepath
        and convert it into array format'''
    training_data = []
    print('generating training data')
    if(modeltype == 'cnn'):
        for category in CATEGORIES:
            path = os.path.join(DATADIR, category)   #path to alphabets. e.g. ../../../asl_alphabet_train/A/
            class_num = CATEGORIES.index(category)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_COLOR)
                    new_array = cv2.resize(img_array, (64, 64))
                    final_img = cv2.cvtColor(new_array, cv2.COLOR_BGR2RGB)
                    training_data.append([final_img, class_num])
                except Exception as e:
                    pass
    else:
        for category in CATEGORIES:
            path = os.path.join(DATADIR, category)   #path to alphabets
            class_num = CATEGORIES.index(category)
            for img in os.listdir(path):
                try:
                    img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                    new_array = cv2.resize(img_array, (64, 64))
                    training_data.append([new_array, class_num])
                except Exception as e:
                    pass
    return training_data
    


# ### Pre-processing Training Data

# In[5]:


def make_data(modeltype, training_data):
    '''This function formats the training data into the proper format and passes it through an generator
    so that it can be augmented and fed into the model'''
    X = []
    y = []
    for features, label in training_data:
        X.append(features)
        y.append(label)
    if(modeltype == "cnn"):
        X = np.array(X).reshape(-1, 64, 64, 3)           #reshaping the array into the 4-D.
        X = X.astype('float32')/255.0                    #to normalize data
        y = tensorflow.keras.utils.to_categorical(y)     #one-hot encoding
        y = np.array(y)
        datagen = ImageDataGenerator(
                                     validation_split = 0.1,
                                     rotation_range = 20,
                                     width_shift_range = 0.2,
                                     height_shift_range = 0.2,
                                     horizontal_flip = True)
        train_data = datagen.flow(X, y, batch_size=64, shuffle=True, subset='training')
        val_data = datagen.flow(X, y, batch_size=64, shuffle=True, subset='validation')
        return (train_data, val_data, X, y)
    else:
        X = np.array(X).flatten().reshape(-1, 4096)
        X = X.astype('float32')/255.0
        y = tensorflow.keras.utils.to_categorical(y)
        y = np.array(y)
        return (X, y)


# ## The Model

# In[6]:


''' The author added a regularizer and BatchNormalization because, as you will see below, 
the model runs into problems with overfitting since all the training_data is from one hand
and seems to be taken as a series of burst photos, which means that
it doesn't do well with data from other people's hands.
So the author added them in an attempt to reduce overfitting.'''

def build_model(modeltype):
    '''Builds the model based on the specified modeltype (either convolutional or fully_connected)'''
    
    model = tensorflow.keras.Sequential()
    print('Building model', modeltype)
    
    if(modeltype == 'cnn'):
         ## CNN 4 layers
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 3)))
        model.add(BatchNormalization())
        
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))
        
        model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        
        model.add(Flatten())
        
        model.add(Dense(256, activation='relu'))
        model.add(BatchNormalization())
        model.add(Dropout(0.25))
        
        model.add(Dense(29, activation='softmax'))
        
        
    else:
        model.add(layers.Conv2D(64, kernel_size=4, strides=1, activation='relu', input_shape=(64,64,3)))
        model.add(layers.Conv2D(64, kernel_size=4, strides=2, activation='relu'))
        model.add(Dropout(0.5))

        model.add(layers.Conv2D(128, kernel_size=4, strides=1, activation='relu'))
        model.add(layers.Conv2D(128, kernel_size=4, strides=2, activation='relu'))
        model.add(Dropout(0.5))

        model.add(Conv2D(256, kernel_size=4, strides=1, activation='relu'))
        model.add(Conv2D(256, kernel_size=4, strides=2, activation='relu'))

        model.add(BatchNormalization())

        model.add(Flatten())
        model.add(Dropout(0.5))
        model.add(Dense(512, activation='relu', kernel_regularizer = regularizers.l2(0.001)))
        model.add(Dense(29, activation='softmax'))
        
        
        
        
    model.compile(optimizer = Adam(lr=0.0005), loss = 'categorical_crossentropy', 
                  metrics = ["accuracy"]) # learning rate reduced to help problems with overfitting
    return model


# In[7]:


def fit_fully_connected_model(X, y, model):
    '''fits the fully connected model'''
    
    filepath = "weights2.best.h5"
    
    # saving model weights with lowest validation loss to reduce overfitting
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
    #tensorboard
    tensorboard_callback = TensorBoard("logs")
    model.fit(X, y, epochs = 10, validation_split = 0.1, callbacks = [checkpoint, tensorboard_callback])


# In[8]:


def fit_CNN_model(train_data, val_data, model):
    '''fits the CNN model'''
    
    filepath = "weights.mest.h5"
    
    # saving model weights with lowest validation loss to reduce overfitting
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False,
                                mode='auto', period=1)
    # tensorboard
    tensorboard_callback = TensorBoard("logs")
    
    # fitting model
    model.fit_generator(train_data, epochs=10, steps_per_epoch =1360, validation_data = val_data,
                       validation_steps = len(val_data), callbacks = [checkpoint, tensorboard_callback])


# ### Data Visualization and Evaluation

# In[9]:


def show_classification_report(X, y, input_shape, model):
    '''This function prints a classification report for the validation data'''
    start_time = time.time()
    validation = [X[i] for i in range(int(0.1 * len(X)))]
    validation_labels = [np.argmax(y[i]) for i in range(int(0.1 * len(y)))]
    validation_preds = []
    labels = [i for i in range(29)]
    for img in validation:
        img = img.reshape((1,) + input_shape)
        pred = model.predict_classes(img)
        validation_preds.append(pred[0])
    print(classification_report(validation_labels, validation_preds, labels, target_names = CATEGORIES))
    print("\n Evaluating the model took {:.0f} seconds".format(time.time()-start_time))
    return (validation_labels, validation_preds)


# In[10]:


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting 'normalize=True'
    """
    
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'
            
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix, without normalization")
        
        
    # print(cm)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    im = ax.imshow(cm, interpolation = 'nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax
np.set_printoptions(precision=2)


# In[30]:


def rotate_image(img):
    '''This function will be applied to the given test data to see how rotating the data effects prediction accuracy.
       It rotates it in a way such that no part of the image is lost'''
    (h, w) = img.shape[:2]
    
    # calculate the center of the image
    center = (w/2, h/2)
    
    angle90 = 90
    angle180=180
    angle270=270
    
    scale = 1.0
    
    # Perform the counter clockwise rotation holding at the center
    # 90 degrees
    M = cv2.getRotationMatrix2D(center, angle90, scale)
    rotated90 = cv2.warpAffine(img, M, (h, w))
    
    # 180 degrees
    M = cv2.getRotationMatrix2D(center, angle180, scale)
    rotated180 = cv2.warpAffine(img, M, (h, w))
    
    # 270 degrees
    M = cv2.getRotationMatrix2D(center, angle270, scale)
    rotated270 = cv2.warpAffine(img, M, (h, w))
    
    return(rotated90, rotated180, rotated270)


# ### Testing data and predictions

# In[32]:


def create_testing_data(path, input_shape, modeltype):
    '''This function will get and format the testing data from the dataset
       It works in almost the exact same way as training_data except it returns image names to evaluate predictions'''
    testing_data = []
    names = []
    for img in os.listdir(path):
        if(modeltype == 'cnn'):
            img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_COLOR)
            rotated_90, rotated_180, rotated_270 = rotate_image(img_array)  # in order to test predictions for rotated data
            imgs = [img_array, rotated_90, rotated_180, rotated_270]
            final_imgs = []
            for image in imgs:
                new_array = cv2.resize(image, (64, 64))
                final_img = cv2.cvtColor(new_array, cv2.COLOR_BGR2RGB)
                final_imgs.append(final_img)
        else:
            img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
            rotated_90, rotated_180, rotated_270 = rotate_image(img_array)
            imgs = [img_array, rotated_90, rotated_180, rotated_270]
            final_imgs = []
            for image in imgs:
                final_img = cv2.resize(image, (64, 64))
                final_imgs.append(final_img)
        # print(len(final_imgs))
        for final_img in final_imgs:
            testing_data.append(final_img)
            names.append(img)
            
    if modeltype == 'cnn':
        new_testing_data = np.array(testing_data).reshape((-1,) + input_shape)
    else:
        new_testing_data = np.array(testing_data).flatten().reshape((-1,) + input_shape)
    new_testing_data = new_testing_data.astype('float32')/255.0
    return (testing_data, new_testing_data, names)


def prediction_generator(testing_data, input_shape, model):
    '''This function generates predictions for sets of testing data'''
    predictions = []
    for img in testing_data:
        img = img.reshape((1,) + input_shape)
        pred = model.predict_classes(img)
        predictions.append(pred[0])
    predictions = np.array(predictions)
    return predictions


# In[34]:


def plot_predictions(testing_data, predictions, names):
    '''This function plots the testing data predictions along with the actual letter they represent
       so we can see the accuracy of the model.'''
    fig = plt.figure(figsize = (100, 100))
    fig.subplots_adjust(hspace = 0.8, wspace = 0.5)
    
    index = 0
    for i in range(1, len(testing_data)):
        y = fig.add_subplot(12, np.ceil(len(testing_data)/float(12)), i)
        
        str_label = CATEGORIES[predictions[index]]
        y.imshow(testing_data[index], cmap = 'gray')
        if(index%4==0):
            title = "prediction = {}\n {}\n unrotated".format(str_label, names[index])
        else:
            title = "prediction = {}\n {}".format(str_label,names[index])
        y.set_title(title, fontsize = 60)
        y.axes.get_xaxis().set_visible(False)
        y.axes.get_yaxis().set_visible(False)
        index+=1


# In[14]:


def calculate_loss(names, predictions):
    y_true = K.variable(np.array([CATEGORIES.index(name[0].upper()) for name in names]))
    y_pred = K.variable(np.array(predictions))
    print(y_true)
    print(y_pred)
    error = K.eval(categorical_crossentropy(y_true, y_pred))
    print('Loss:', error)


# ### TensorBoard

# In[15]:


get_ipython().run_line_magic('load_ext', 'tensorboard')
get_ipython().run_line_magic('tensorboard', '--logdir logs')


# ## Convolutional Neural Network

# In[16]:


modeltype2 = "cnn"
input_shape2 = 64, 64, 3

# getting training data
training_data2 = create_training_data(modeltype2)
random.shuffle(training_data2)


# In[17]:


# building model
model2 = build_model(modeltype2)

# formatting data
train_data2, val_data2, X2, y2 = make_data(modeltype2, training_data2)

# fitting model
fit_CNN_model(train_data2, val_data2, model2)
model2.load_weights("weights.best.h5")
graph2 = plot_model(model2, to_file="my_model2.png", show_shapes=True)


# In[18]:


model2.save('tfcnnmodel2')


# In[19]:


model2_json = model2.to_json()
with open("model2.json", "w") as json_file:
    json_file.write(model2_json)
# serialize weights to HDF5
model2.save_weights("model2.h5")
print("Saved model2 to disk")


# In[21]:


model2.save("cnnmodel2.h5")
print("Saved model to disk")


# In[22]:


# evaluating validation data
validation_labels2, validation_preds2 = show_classification_report(X2, y2, input_shape2, model2)


# In[23]:


# confusion matrix for validation data
plot_confusion_matrix(validation_labels2, validation_preds2, classes=CATEGORIES,
                      title='Confusion matrix, without normalization')
plt.show()


# In[35]:


# database testing data and predictions
test_dir = "../master_thesis_project1/asl-alphabet/asl_alphabet_test/"
testing_data2, new_testing_data2, names2 = create_testing_data(test_dir, input_shape2, modeltype2)
predictions2 = prediction_generator(new_testing_data2, input_shape2, model2)
plot_predictions(testing_data2, predictions2, names2)
calculate_loss(names2, predictions2)


# In[ ]:




