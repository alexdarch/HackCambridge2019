# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 16:26:22 2019
@author: benwi
"""
import requests
from IPython.display import HTML
from PIL import Image
from io import BytesIO
import numpy as np

subscription_key = '6d1691bf159940679209d2d734d2e2e0'
assert subscription_key

faceListId = '19012019facelist'

image_url= "https://how-old.net/Images/faces2/main001.jpg"

def findFaceInImage(image_data):
    '''Find faces in an image'''
    faceDetect_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'

    headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
               'content-type': 'application/octet-stream'
               }

    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    response = requests.post(faceDetect_api_url, params=params, headers=headers, data=image_data)
    faces = response.json()
    print(faces)
    return faces

def createNewFaceList(facelistname):
    '''Create new FaceList'''
    faceListName = facelistname
    faceListCreate_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/facelists/' + faceListName

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = {
        'faceListId': faceListName,
    }

    response = requests.put(faceListCreate_api_url, params=params, headers=headers, json={"name": faceListName})
    print(response.json())

def allocateToFaceList(image_data, face, facelistname):
    '''Allocate new faces to FaceList'''
    faceListName = facelistname
    newFaceToFaceList_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/facelists/'+faceListName+'/persistedFaces'

    image_file = BytesIO(requests.get(image_url).content)
    image = Image.open(image_file)
    width, height = image.size

    faceRectangle = face['faceRectangle']
    left = np.round((faceRectangle['left']/width)*100)
    top = np.round((faceRectangle['top']/height)*100)
    width = np.round((faceRectangle['width']/width)*100)
    height = np.round((faceRectangle['height']/height)*100)
#    left = int(faceRectangle['left'] *100)
#    top = int(faceRectangle['top'] *100)
#    width = int(faceRectangle['width'] *100)
#    height = int(faceRectangle['height'] *100)

    targetFace = 'targetFace='+str(left)+','+str(top)+','+str(width)+','+str(height)
    print(targetFace)

    headers = { 'Ocp-Apim-Subscription-Key': subscription_key,
               'content-type': 'application/octet-stream'
               }

    params = {
        'faceListId': faceListName,
        'targetFace': targetFace,
    }

    response = requests.post(newFaceToFaceList_api_url, params=params, headers=headers, data=image_data)
    print(response.json())

def findSimilarFaces(face, facelistname):
    '''Face similarity'''
    faceListName = facelistname
    faceId = face['faceId']

    faceSimilarity_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/findsimilars'

    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    response = requests.post(faceSimilarity_api_url, headers=headers, json={'faceId': faceId, 'faceListId': faceListName, 'mode': 'matchFace', "maxNumOfCandidatesReturned": 30})
    similarFaces = response.json() # Returns persistedFaceId and confidence for each response
    print(similarFaces)

    return similarFaces

def getFaceList(facelistname):
    '''See what's in the FaceList'''
    faceListName = facelistname

    getFaceList_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/facelists/'+faceListName
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

    params = {
        'faceListId': faceListName,
    }

    response = requests.get(getFaceList_api_url, params=params, headers=headers)

    print(response.json())

    return response.json()

#faces = findFaceInImage(image_url)
#createNewFaceList(faceListId)
#
#for face in faces:
#    allocateToFaceList(image_url, face, faceListId)
#    findSimilarFaces(face, faceListId)
#
#getFaceList(faceListId)

image_path = 'test_img.jpg'
image_data = open(image_path, "rb")

faces = findFaceInImage(image_data)
© 2019 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
Pricing
API
Training
Blog
About
