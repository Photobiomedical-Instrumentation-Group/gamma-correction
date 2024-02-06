# gamma-correction
>> Code to use gamma correction in image using colorchart. 

Reference:

TAKAHASHI, Masato et al. Development of a camera-based remote diagnostic system focused on color reproduction using color charts. Artificial life and robotics, v. 25, p. 370-376, 2020.

link: (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7372208/)


Using a calibrated colorchart image, it's possible to adjust a gamma function to correct the image. 
The adjustment of the function takes into consideration the reference RGB values of the colorchart and the values of the image.
For a different colorchart, the average RGB values of each patch on the grayscale scale, ranging from black to white, should be added to a .csv file in column A. /reference_RGB_Logitech_gray.csv/
The results is: 
![Figure_1](https://github.com/Photobiomedical-Instrumentation-Group/gamma-correction/assets/32850913/70d005df-2cd0-4a72-b7c5-73ba88076e3c)
