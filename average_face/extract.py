#!/usr/bin/python

# Find frontal human faces in an image and extract landmarks
# Based on the dlib example: http://dlib.net/face_landmark_detection.py.html

import sys
import os
import glob
import dlib
from skimage import io

# if len(sys.argv) != 3:
#     print(
#         "Missing argument. Please provide a predictor model and the path to your image folder.\n"
#         "A predictor model can be downloaded from: "
#         "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2\n"
#         "Usage example: python extract.py shape_predictor_68_face_landmarks.dat ./images\n"
#     )
#     exit()

def extract(rewrite_existing=False):
    # predictor_path = sys.argv[1]
    # faces_folder_path = sys.argv[2]

    # predictor_path = "./average_face/shape_predictor_68_face_landmarks.dat"
    # faces_folder_path = "static/faces"
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    faces_folder_path = "../static/faces"

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    removed = 0
    for f in glob.glob(os.path.join(faces_folder_path, "*.txt0")):
        os.remove(f)
        os.remove(os.path.join(faces_folder_path, f.split("\\")[1][:-5]))
        removed += 1
    print(f"Removed {removed} files")

    c = -1
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
        c += 1
        print("Processing file: {}".format(f))
        if os.path.isfile(f + ".txt") and not rewrite_existing:
            print("Exist, skipping")
            continue
        try:
            img = io.imread(f)

            # Find the bounding boxes of each face.
            dets = detector(img, 1)
            print("Number of faces detected: {}".format(len(dets)))
            if len(dets) < 1:
                raise Exception

            for k, d in enumerate(dets):
                results = []

                print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                    k, d.left(),
                    d.top(),
                    d.right(),
                    d.bottom()
                ))

                # Get the landmarks/parts for the face in box d.
                shape = predictor(img, d)
                print("Part 0: {}, Part 1: {} ...".format(
                    shape.part(0),
                    shape.part(1)
                ))

                # Save each landmark as xy coordinate
                for n in range(0, 68):
                    results.append(str(shape.part(n).x) + " " + str(shape.part(n).y))

                with open(f + ".txt", "w") as output:
                    output.write("\n".join(results))
                break
        except:
            print("\n\n\nERROR\n\n\n")
            with open(f + ".txt0", "w") as output:
                output.write("\n")
        print(f"Processed {c} images")

extract()
