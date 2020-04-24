# UTI-DEPUTI
48 hours project for HACK.MOSCOW V3.0 hackathon in **Data visualisation**

LIVE DEMO: http://utideputi.wndenis.space/ (Design is a bit messy, but it works!)

---
Our application focused on visualizing the most common human in every region of Russian Federation. We can show you the most medianized profile with such data - most popular name, median incomes, real estate square, gender and how the most common person looks like.
One of criteria was using some **external data** - not only from API and [dump](https://declarator.org/ "Dump source") provided by organizers. So, we decided to choose the main data for visualisation - images.  
![Median face 1](https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/img1.jpg)
<img src="https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/img2.jpg" alt="Median face 2" width="49.5%" height="49.5%" />
<img src="https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/img3.jpg" alt="Median face 2" width="49.5%" height="49.5%" />

### Approach
Using public data, we collected about 6000 public images of every person from database who was mentioned on Wikipedia.

![Collected photos](https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/photos.jpg)

To achieve summarized view to data, we heavily preprocessed images using [this](https://www.learnopencv.com/average-face-opencv-c-python-tutorial/), so that we can provide summarized image of 
(almost) every person in every region on interactive map.  
![Faces animation](https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/anim.gif)
![Map](https://github.com/wndenis/UTI-DEPUTI/blob/back/ReadmeContent/map.jpg)

