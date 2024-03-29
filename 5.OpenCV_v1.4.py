import cv2
import numpy as np
import tensorflow
from keras.models import load_model
from skimage.transform import resize, pyramid_reduce
import PIL
from PIL import Image

trained_model = tensorflow.keras.models.load_model('cnnmodel2.h5')


def prediction(pred):
    return(chr(pred+ 65))

def keras_predict(model, image):
    data = np.asarray(image, dtype="float32")
    pred_probab = model.predict(data)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def keras_process_image(img):
    image_x = 64
    image_y = 64
    img = cv2.resize(img, (3,64,64), interpolation = cv2.INTER_AREA)
    return img

def crop_image(image, x, y, width, height):
    return image[y:y+height, x:x+width]


def main():
    l = []

    global cam_capture
    cam_capture = cv2.VideoCapture(0)
    
    while True:
        #cam_capture = cv2.VideoCapture(0)
        _, image_frame = cam_capture.read()
    # Flip the image
        image_frame = cv2.flip(image_frame,1)

    # Select ROI (region of interest)
        # Checkpoint-1
        #cv2.imshow("frame", image_frame)
        #im2 = crop_image(image_frame, 300,300,300,300)
        im2 = crop_image(image_frame, 350,200,250,220)
        # Checkpoint-2
        #cv2.imshow("frame", im2)

        image_grayscale = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        # Checkpoint-3
        #cv2.imshow("frame", image_grayscale)

        image_grayscale_blurred = cv2.GaussianBlur(image_grayscale, (15,15), 0)
        # Checkpoint-4
        #cv2.imshow("frame", image_grayscale_blurred)

        im3 = cv2.resize(image_grayscale_blurred, (64,64), interpolation = cv2.INTER_AREA)
        # Checkpoint-5
        #cv2.imshow("frame", im3)

        im4 = np.resize(im3, (64,64,3))
        # Checkpoint-6
        #cv2.imshow("frame_6", im4)

        im5 = np.expand_dims(im4, axis=0)
        # Checkpoint-7 - wrong checkpoint. im5 is may not be a image
        #cv2.imshow("frame_7", im5)


        pred_probab, pred_class = keras_predict(trained_model, im5)


        curr = prediction(pred_class)
        cv2.putText(image_frame, curr, (580,50), cv2.FONT_HERSHEY_COMPLEX, 2.0, (255,255,255), lineType=cv2.LINE_AA)

    # Display cropped image
        cv2.rectangle(image_frame, (350,200),(600,420), (255,00,00), 3)
        cv2.imshow("frame", image_frame)

    #cv2.imshow("Image2", cropped_img)
        cv2.imshow("Image2", im2)
    #cv2.imshow("image_grayscale", image_grayscale)
        #cv2.imshow("image_grayscale", image_grayscale)
    #cv2.imshow("image_grayscale_blurred", image_grayscale_blurred)
        #cv2.imshow("image_grayscale_blurred", image_grayscale_blurred)

    #cv2.imshow("Image3", resized_img)
        #cv2.imshow("Image3", im3)
    #cv2.imshow("Image4", resized_img)
        #cv2.imshow("Image4", im4)


        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()

cam_capture.release()
cv2.destroyAllWindows()
