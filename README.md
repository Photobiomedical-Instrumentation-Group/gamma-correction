# gamma-correction

Code to use gamma correction in image using colorchart.

Reference:

TAKAHASHI, Masato et al. Development of a camera-based remote diagnostic system focused on color reproduction using color charts. Artificial life and robotics, v. 25, p. 370-376, 2020.

Link: [Development of a camera-based remote diagnostic system focused on color reproduction using color charts](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7372208/)

Using a calibrated colorchart image, it's possible to adjust a gamma function to correct the image. The adjustment of the function takes into consideration the reference RGB values of the colorchart and the values of the image.

Note: the colorchart must be properly aligned in the image to accurately obtain the values of each patch in the image.

![v2](https://github.com/Photobiomedical-Instrumentation-Group/gamma-correction/assets/32850913/9f1a183e-3902-4aad-9a56-a5d022d66b24)


For a different colorchart, the average RGB values of each patch on the grayscale scale, ranging from black to white, should be added to a .csv file in column A. /reference_RGB_Logitech_gray.csv/

The results are:

![Figure_1](https://github.com/Photobiomedical-Instrumentation-Group/gamma-correction/assets/32850913/7af1f87b-3e88-4c3a-9389-c3f42e37b599)


The according the reference [TAKAHASHI, Masato et al.]
First, we extract the color chart part of the photograph using AR markers. The portions of each square are further taken and averaged. The model is created through a multiple regression from the difference between the averaged numbers and the reference RGB values. Based on this, all pixels are converted to correct the color of the human face and tongue.

The details of the gamma correction are next described. First, such correction is applied based on the luminance of the grayscale portion of the color chart measured by a colorimeter against the RGB value when the grayscale was photographed. Similarly, this is also conducted for the grayscale portion of the reference RGB value. Next, a gamma correction is applied for each RGB. In the case of R, the form is as shown in Eq:

\[ R_c = aY^\gamma + b \]

where Rc is the R-value of the image taken, and Y is the luminance of the color chart’s grayscale. In the grayscale of the color chart, the brightness of the grayscale is transformed to within the range of zero to 1 by normalizing with the brightness value of white such that black has a value zero and white has a value of 1. This model can be used to correct the gamma for any RGB value. Specifically, we compute the gamma-corrected RGB values by multiplying the inverse function of Eq. (6) for each value.

Next, we construct a model using multiple regression on the color of each gamma-corrected color patch. In the case of R, we have Eq. (7):

\[R′_{c}=aRr+bGr+cBr+d\]

where R'c is the R value of the corrected image and Rr, Gr, Br indicate an un-corrected RGB value. Each parameter is calculated by a multiple regression with every color patch.

Finally, the color correction is completed by performing a transformation on each pixel of the captured image
