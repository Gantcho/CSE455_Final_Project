## Problem Setup

For our project, we decided to combine a few different methods to solve the problem of detecting license plate numbers from a picture. This included the following steps:
  1. First, we needed to use features of the image, specifically contours, to detect the region of the image where the license plate is
  2. Next, we need to segment the license plate into images of individual characters
  3. Last, we need to train a classifier to output an alphaneumeric character based on an image of a character

The data we used to to evaluate our model on is courtest of [Pieter van Mill](https://www.kaggle.com/pcmill/license-plates-on-vehicles?select=04QSYty5zbXJKfpo.jpeg) on Kaggle.

The license plates are of a variety of colors, shapes, and lengths as they cover different types of vehicles from multiple European countries. As such, we faced difficulties in identifying the region of the image where the license plate was. The approach we used was to identify contours in the image, approximate them as polynomials, and then if it was in a rectangular shape (which we determined was if it had 4 sides), we would create a bounding rectangle to surround the contour. As an example, for this license plate:
![plate](https://github.com/Gantcho/CSE455_Final_Project/blob/ecc693ec717c004ba16fd30f3cf0f80f9297550f/test.jpg)

We identified this bounding box:
![box](https://github.com/Gantcho/CSE455_Final_Project/blob/ecc693ec717c004ba16fd30f3cf0f80f9297550f/test.jpg_bounding_box.png)

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
