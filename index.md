## Final Project

For our project, we decided to combine a few different methods to solve the problem of detecting license plate numbers from a picture. This included the following steps:
  1. First, we needed to use features of the image, specifically contours, to detect the region of the image where the license plate is
  2. Next, we need to segment the license plate into images of individual characters
  3. Last, we need to train a classifier to output an alphaneumeric character based on an image of a character

The inputs we used to to evaluate our model on is courtesy of [Pieter van Mill](https://www.kaggle.com/pcmill/license-plates-on-vehicles?select=04QSYty5zbXJKfpo.jpeg) on Kaggle. There were no labels provided for this dataset, so we had to hand label the data. Some images had obscured license plates or were too blurry to use, so we didn't use those.

### License Plate Bounding

The license plates are of a variety of colors, shapes, and lengths as they cover different types of vehicles from multiple European countries. Some images even had multiple license plates in them. As such, we faced difficulties in identifying the region of the image where the license plate was. The approach we used was to identify contours in the image by applying a filter to make the image black and white. The uniformity in color would make it easy for us to identify contours, approximate them as polygons, and then if one was in a rectangular shape (which we determined was if it had 4 sides), we would create a bounding rectangle to surround the contour. As an example, for this license plate:

![plate](https://user-images.githubusercontent.com/32994901/158915096-b01b7d45-7886-4976-90b4-ad5f9467b63f.jpg)

We identified this bounding box:

![box](https://user-images.githubusercontent.com/32994901/158915120-5e5df26f-d348-4d38-aa88-ab26206fcf5f.png)

For this section, we referenced this [article](https://www.section.io/engineering-education/license-plate-detection-and-recognition-using-opencv-and-pytesseract/) by Simon Kuriri. Specifically, we followed the technique in the article for identifying a bounding rectangle based on the polygon approximation of a contour.

### Plate Segmentation

For segmentation of individual characters within the license plate, we used a similar technique of looking for bounding rectangles after applying a filter and identifying contours. Specifically for the numbers within the license plate, we look for rectangles with a vertical orientation, as letters and numbers on a license plate are always more tall than wide. Essentially, this means we check if the bounding box's height is over twice its width. We could not make this assumption for the bounding box of the license plate itself because we had different orientations of rectangles in our data. Here is an example of what the license plate looks like before we identify the countours and bounding boxes:

![segment](https://user-images.githubusercontent.com/32994901/158922082-c4f736d5-0d12-40d5-b798-c2e4ae613e07.jpg)

Once we identify the rectangular regions of the individual characters of the plate, we can run our trained character classifier to extract the entire plate number.

For this section, we referenced this [article](https://medium.com/@quangnhatnguyenle/detect-and-recognize-vehicles-license-plate-with-machine-learning-and-python-part-2-plate-de644de9849f) by Quang Nguyen. We borrowed the code for identifying segments based on bounding rectangle height-width ratio from the article, and the rest of the code is loosely based on the approaches in the article.



### Character Recognition

The last thing to train was an alphaneumeric character classifier so we could read out each individual character segment on the plate. There have been countless datasets and implementations of these types of classifiers, like CIFAR-10 for example. 

As a result, we drew inspiration from this [article](https://towardsdatascience.com/building-and-deploying-an-alphabet-recognition-system-7ab59654c676) written by Sakshi Butala in order to train a convolutional neural net with Max Pooling to classify characters. To train this classifier, we used this [dataset](https://github.com/quangnhat185/Plate_detect_and_recognize) from Quang Nguyen. For this section, we borrowed the neural net architecture and handled the data loading and data transformation ourselves.

### Results

With everything put together, our results ended up a bit disappointing. While our individual processes worked decently well, they heavily depended on a rectangular region to identify the plate and individual characters. As many of the plates in our dataset were at an angle, the bounding rectangle was not able to appropriately capture the plate, which compounded for even worse results while identifying the rectangular character segments within the plate. When we did have straight on, rectangular license plates however, our model performed well. In the image below, the model correctly predicted 31LNPG as the license plate (we chose to omit recognizing '-' in our model):

![test](https://user-images.githubusercontent.com/32994901/158928075-a8eda14a-d303-4543-9b49-26073480b157.jpeg)

We also were able to almost correctly read a plate with multiple vehicles in the frame. In the image below, our model predicted 54VN8N instead of 54VNBN, which is understandable as 8 and B look very similar:

![test2](https://user-images.githubusercontent.com/32994901/158928382-4b52e8fb-e46c-4106-b11e-ece78cf3e948.jpeg)

Overall, while we did have some success, our model greatly struggled without heavily standardized and easy to bound images. When we tested on more realistic and natural photos of vehicles at angles, the model was not able to generate a properly bounded rectangle and struggled. In the future, we might consider using a more flexible bounding technique, such as finding a bounding parallelogram to allow for angled inputs instead of a rectangle. Alternatively, we might want to try applying a perspective transform to the image in order to get a more straight-on view of the license plate.

### Video Presentation

Here is our [video](https://www.youtube.com/watch?v=ELPXl4PvVNI)

Here is the repo for our [code](https://github.com/Gantcho/CSE455_Final_Project/tree/master)
