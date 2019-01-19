import numpy as np
import os

class program:
    def __init__(self): 
        self.Running = True
        # total dataset
        dataset_size = 500 
        self.dataset = self.get_dataset()
        # initial image dataset
        self.initial_size = 30
        self.image_set = self.initial_set(self.initial_size)
        # initialise similarity average container
        self.similarity_average = [0]*len(self.dataset)
        # counter for number of images that have been considered
        self.count = 0
    def get_dataset(self):
        '''
        get array of image names from dataset
        '''
        b = []
        for _ in range(500):
            b.append('b')
        return b
        

    def get_image(self, face_id=None, num_images = 1):
        '''
        Get the next image from database randomly. Number of images returned = num_images
        If face_id is specified, get the corresponding image.  
        return array of image_name
        '''
        a = []
        for _ in range(100):
            a.append('a')
        return a

    def initial_set(self, init_size = None):
        images = self.get_image(num_images=init_size)
        return images

    def update_similarity_average(self, image, response, init=False):
        def get_similarity(image):
            '''
            Function to get similarity scores for images in the dataset

            Args: 
                image: image file name

            Returns: 
                confidence: An array of confidence values
            '''
            # initialise values for unit testing
            return np.arange(len(self.similarity_average))/(len(self.similarity_average))
            

        new_similarities = get_similarity(image)

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

    def run(self):
        '''
        Need to swipe through 30 images. 
            For each image, get confidence values for the whole dataset. +ve for yes, -ve for no
                load image to website
                calculate confidence values for whole dataset
                find average for whole dataset
        
        while running: 
        Output best image from the dataset with the best confidence values. 
            remove this image from the dataset
            Recalculate the confidence values for the dataset.     
        '''
        # array of images to use for initial average calculation
        for i in range(len(self.image_set)):
            image = self.image_set[i]
            # receive a +1 for YES, -1 for NO from user response
            response = self.send_image_to_console(image)
            self.update_similarity_average(image, response)
        
        print("Initialisation finished")
        # self.Running is set true/false
        while len(self.similarity_average) > 0: 
            # get best image from the dataset and remove the used image
            image, choice = self.get_best_image()
            response = self.send_image_to_console(image)
            self.update_similarity_average(image, response)

            # remove image name from the dataset and the average
            self.dataset.pop(choice)
            self.similarity_average.pop(choice)
        
        print("Ran out of images to give")
            

if __name__ == "__main__":
    prog = program()
    prog.run()