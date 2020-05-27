import cv2
import numpy as np
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image

trained_model = load_model('Arshad221b_model.h5')

#print(trained_model.summary())

#label_map = (generator.class_indices)
#print(label_map)

#y_prob = trained_model.predict(x) 
#y_classes = y_prob.argmax(axis=-1)
#print(y_classes)


def keras_predict(model, image):
    data = np.asarray(image, dtype="int32")
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def prediction(pred):
    return(chr(pred+ 65))



# example of loading an image with the Keras API
from keras.preprocessing.image import load_img
# load the image
test_img = load_img('../master_thesis_project1/asl-alphabet/asl_alphabet_test/B_test.jpg')
# report details about the image
#print(type(test_img))
#print(test_img.format)
#print(test_img.mode)
#print(test_img.size)
# show the image
#test_img.show()
from matplotlib import pyplot as plt
plt.imshow(test_img)
plt.show()

resized_test_img = np.resize(test_img, (28,28,1))
im5 = np.expand_dims(resized_test_img, axis=0)

pred_probab, pred_class = keras_predict(trained_model, im5)
print(pred_class)
curr = prediction(pred_class)
print(curr)



#########################################################################
# Alternative Prediction
predict = trained_model.predict(im5)
print(predict)
