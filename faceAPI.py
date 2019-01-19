# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 16:26:22 2019

@author: benwi
"""
import requests
from IPython.display import HTML

subscription_key = '6d1691bf159940679209d2d734d2e2e0'
assert subscription_key

faceListId = '19012019facelist'

def findFaceInImage(image_url):
    '''Find faces in an image'''
    faceDetect_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/detect'
    
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
        
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    
    response = requests.post(faceDetect_api_url, params=params, headers=headers, json={"url": image_url})
    faces = response.json()
    
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
    
def allocateToFaceList(image_url, face, facelistname):
    '''Allocate new faces to FaceList'''
    faceListName = facelistname
    newFaceToFaceList_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/facelists/'+faceListName+'/persistedFaces'
    
    left = face['left']; top = face['top']; width = face['width']; height = face['height']
    
    targetFace = 'targetFace='+str(left)+','+str(top)+','+str(width)+','+str(height)
    print(targetFace)
    
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
        
    params = {
        'faceListId': faceListName,
        'targetFace': targetFace,
    }
    
    response = requests.post(newFaceToFaceList_api_url, params=params, headers=headers, json={"url": image_url})
    print(response.json())
    
def findSimilarFaces(face, facelistname):    
    '''Face similarity'''
    faceListName = facelistname
    faceId = face['faceId']    
    
    faceSimilarity_api_url = 'https://northeurope.api.cognitive.microsoft.com/face/v1.0/findsimilars'
    
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
    
    response = requests.post(faceSimilarity_api_url, headers=headers, json={'faceId': faceId, 'faceListId': faceListName, 'mode': 'matchFace'})
    similarfaces = response.json() # Returns persistedFaceId and confidence for each response
    
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
    