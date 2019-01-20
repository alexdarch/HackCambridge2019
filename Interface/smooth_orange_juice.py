import numpy as np
from faceAPI import FaceAPI
import pandas as pd
import os

class SmoothOrangeJuice():
    def __init__(self): 
         # face list
        self._facelistname = 'facelist_1'
        self.fa = FaceAPI(self._facelistname)
        self.fa.create_new_face_list()
        # running flag
        self.Running = True

        # initialise similarity average container
        self.similarity_average = pd.DataFrame(data={'PersistedFaceId':[], 'ImagePath':[], 'Confidence':[],})
        # main image dataset
        self.dataset_dir = './Interface/images/main'
        self.dataset = self.get_dataset(init=False)
        # initial image dataset
        self.init_dir = './Interface/images/initial'
        self.initial_size = 30
        self.image_set = self.get_dataset(init=True)
        
        # counter for number of images that have been considered
        self.count = 0 
        # initialise dictionary from filename to faceid
        self.file_to_face = {}       

    def get_dataset(self, init=False):
        # Get list of images in directory
        if init is False:
            files = os.listdir(self.dataset_dir)
            root = self.dataset_dir

        if init is True: 
            files = os.listdir(self.init_dir)
            root = self.init_dir
        container = [None]*len(files)
        
        for i,f in enumerate(files): 
            # save filename into dataset container
            container[i] = f
            path = root + '/' + f
            # load the faces in the image to facelist
            persisted_face_id = self.fa.allocate_to_face_list(path)
            # initialise the whole dataset with pfaceid, path and confidence
            to_append = pd.DataFrame([[persisted_face_id, f, 0.0]], columns=['PersistedFaceId','ImagePath','Confidence'])
            self.similarity_average = (
                self.similarity_average.append(to_append, ignore_index=True)
                )
            print(self.similarity_average)
        return container

    def update_similarity_average(self, image, response, init=False):
        def get_similarity(image, init):
            '''
            Function to get similarity scores for images in the dataset

            Args: 
                image: image file name

            Returns: 
                confidence: An array of confidence values
            '''
            if init is False: 
                path = self.dataset_dir + '/' + image
            else: 
                path = self.init_dir + '/' + image
            # Detect faces in image
            faces = self.fa.find_face_in_image(path)
            # Find similar faces
            self.fa.find_similar_faces(faces)
            # Input new face data into facelist
            self.fa.allocate_to_face_list(path)
            # get similarities
            similar_faces = self.fa.find_similar_faces(faces)
            
            # create dictionary mapping filename to face_id and similar faces
            for f in similar_faces: 
                if f['persistedFaceId'] in self.similarity_average['persistedFaceId']:
                    # add confidences
                    print('worked\n\n\n')
                print('\n\n\n\n')
                
            
            
        new_similarities = get_similarity(image, init)

        self.count += 1
        print(self.count)
        self.similarity_average = (
            list((self.similarity_average + response*new_similarities)/self.count)
        )
        return None 

    def get_best_image(self):
        '''
        Rank the faces and output the fact id of the best face
        Args: 
            face_dict: dictionary with keys faceid, similarity, confidence and 
            array of top ten face_id, similarity and confidence scores as values.
        Returns: 
            best_face_id: The face id corresponding to the best ranking
        '''
        index = np.where(self.similarity_average==max(self.similarity_average))

        # choose random value from index in the case of multiple choices
        choice = np.random.choice(index[0])
        best_image_id = self.dataset[choice]

        return best_image_id, choice
    
    def send_image_to_console(self, image):
        a = np.random.choice([-1,1])
        print('send image to console')
        print('receive input')
        return a

    def initialisation_run(self):
        # array of images to use for initial average calculation
        for i in range(len(self.image_set)):
            image = self.image_set[i]
            # receive a +1 for YES, -1 for NO from user response
            response = self.send_image_to_console(image)
            self.update_similarity_average(image, response)
        
        print("Initialisation finished")
        # self.Running is set true/false
        return None

    def main_run(self):    
        while len(self.similarity_average) > 0: 
            # get best image from the dataset and remove the used image
            image, choice = self.get_best_image()
            response = self.send_image_to_console(image)
            self.update_similarity_average(image, response)

            # remove image name from the dataset and the average
            self.dataset.pop(choice)
            self.similarity_average.pop(choice)
        
        print("Ran out of images to give")
        return None
            
if __name__ == "__main__":
    prog = SmoothOrangeJuice()
    