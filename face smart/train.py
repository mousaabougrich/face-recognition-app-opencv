import os
import cv2
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'

def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]
    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        # Removed the display of images during training
    return np.array(IDs), faces

IDS, faces = getImagesWithID(path)
recognizer.train(faces, IDS)
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()  # This can also be removed if not needed
