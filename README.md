# ocr

Optical character recognition using neural network. Implemented with Python and its libraries Numpy and OpenCV.

We recommend you to view the presentation file inside docs first, which will give you a brief analysis of this project.

Python libraries needed:
Numpy (Neural Network creation and data handling)
OpenCV (Image processing)
PyQT (GUI)

There are two parts to this project. First one is the neural network and the other is the image processing.

The OCR is performed in the following phases:

1. Image is retrieved
The image should be cropped in such a way that only text is present. Also, the background should be very lighter than the text. Ideal image would be black text on a white paper background.

2. Preprocessing
Noises are removed by blurring. The it is converted to binary image along with invert. For this we've used OpenCV methods such as gaussian blur and threshold.

3. Segmentation
Segmentation is divided into three parts. First we segment the image based on lines. Then the lines are separated into words. Lastly, the words are separated into characters. OpenCV methods such as projections and contour detections are used. The characters are then fed into the neural network.

4. Neural Network
There are two parts to neural network. First is Training Neural Network. For training the neural network, we first generated our own samples for each characters. That made a total of 260,000 samples. We used PHP's imagettftext() method using 10 different fonts. PHP generated each samples in an image format. So we then converted those images into numpy array and combined all samples with corresponding labels required by the neural network. Second is Recognizing characters. We used two NN for the classification. First is the classification for all characters. Second is based on the confusion classes. (For the detailed description of neural network and their implementaiton, we refered to the book at http://neuralnetworksanddeeplearning.com/ So if you want to know all about neural networks, their algorithms and workings, you should definitely give it a visit.)

5. Optimizations
Using two NNs for classification helped in better optimization of the recognition. Along with that, we also checked each words in the english dictionary to fix the spelling errors. (The dictionary was based on Peter Norvig's spell correct - http://norvig.com/spell-correct.html)
