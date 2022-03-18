## Final Project

For our project, we decided to combine a few different methods to solve the problem of detecting license plate numbers from a picture. This included the following steps:
  1. First, we needed to use features of the image, specifically contours, to detect the region of the image where the license plate is
  2. Next, we need to segment the license plate into images of individual characters
  3. Last, we need to train a classifier to output an alphaneumeric character based on an image of a character

The data we used to to evaluate our model on is courtest of [Pieter van Mill](https://www.kaggle.com/pcmill/license-plates-on-vehicles?select=04QSYty5zbXJKfpo.jpeg) on Kaggle. There were no labels provided for this dataset, so we had to hand label the data. Some images had obscured license plates or were too blurry to use, so we didn't use those.

### License Plate Bounding

The license plates are of a variety of colors, shapes, and lengths as they cover different types of vehicles from multiple European countries. Some images even had multiple license plates in them. As such, we faced difficulties in identifying the region of the image where the license plate was. The approach we used was to identify contours in the image by applying a filter to make the image black and white. The uniformity in color would make it easy for us to identify contours, approximate them as polygons, and then if one was in a rectangular shape (which we determined was if it had 4 sides), we would create a bounding rectangle to surround the contour. As an example, for this license plate:

![plate](https://user-images.githubusercontent.com/32994901/158915096-b01b7d45-7886-4976-90b4-ad5f9467b63f.jpg)

We identified this bounding box:

![box](https://user-images.githubusercontent.com/32994901/158915120-5e5df26f-d348-4d38-aa88-ab26206fcf5f.png)

For this section, we referenced this [article](https://www.section.io/engineering-education/license-plate-detection-and-recognition-using-opencv-and-pytesseract/) by Simon Kuriri.

### Plate Segmentation

For segmentation of individual characters within the license plate, we used a similar technique of looking for bounding rectangles after applying a filter and identifying contours. Specifically for the numbers within the license plate, we look for rectangles with a vertical orientation, as letters and numbers on a license plate are always more tall than wide. Essentially, this means we check if the bounding box's heigt is over twice its width. We could not make this assumption for the bounding box of the license plate itself because we had different orientations of rectangles in our data. Here is an example of what the license plate looks like before we identify the countours and bounding boxes:
![segment](https://user-images.githubusercontent.com/32994901/158922082-c4f736d5-0d12-40d5-b798-c2e4ae613e07.jpg)

For this section, we referenced this [article](https://medium.com/@quangnhatnguyenle/detect-and-recognize-vehicles-license-plate-with-machine-learning-and-python-part-2-plate-de644de9849f) by Quang Nguyen.

Once we identify the rectangular regions of the individual characters of the plate, we can run our trained character classifier to extract the entire plate number.

### Character Recognition

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/Gantcho/CSE455_Final_Project/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
