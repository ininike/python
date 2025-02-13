from deepface import DeepFace
import os
import asyncio

models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
detectors = ["opencv", "ssd", "mtcnn", "dlib", "retinaface"]

directory = 'out'
file_names = os.listdir(directory)
file_paths = [(os.path.join(directory, file_name)).replace('\\','/') for file_name in file_names]
loop_length = int((len(file_names))/2)


def compare(first, second):
    first= 0
    second= 1
    successes = 0
    fails = 0
    errors = 0
    for i in range(50):
        print('running ', i+1)
        try:
            matches = DeepFace.verify(file_paths[first],file_paths[second],model_name = models[0],detector_backend = detectors[4]) 
            if matches['verified']:
                successes += 1
                first += 2
                second += 2
                continue
            fails += 1
        except:
            errors += 1
        first += 2
        second += 2
    accuracy = successes * 0.25
    print(f'successes: {successes}\nfails: {fails}\nerrors: {errors}\naccuracy: {accuracy}')
    return

compare()



