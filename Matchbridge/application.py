import sys
import numpy as np
sys.path.insert(0,'./Interface')

from Interface import faceAPI
from Interface.smooth_orange_juice import SmoothOrangeJuice
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
app = Flask(__name__)


dummy_data = [
    {
        'team_member': 'Alex Darch',
        'position': 'HTML bish',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'Ben Williams',
        'position': 'Team Leader',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'John Clay',
        'position': 'No idea',
        'date_updated': '2018/01/19'
    },
    {
        'team_member': 'Ben Lee',
        'position': 'ML monkey',
        'date_updated': '2018/01/19'
    }
]

image_data = {'image_src': "../static/images/test_img.jpg"}
# Need some way of allocating the top 6 images at any given point
image1 = {'image_src': ""}
image2 = {'image_src': ""}
image3 = {'image_src': ""}
image4 = {'image_src': ""}
image5 = {'image_src': ""}
image6 = {'image_src': ""}

orange = SmoothOrangeJuice()
orange.count = 0

@app.route("/")
@app.route("/home")
def hello():
    image_data = orange.image_set[orange.count]
    orange.count += 1
    return render_template('home.html', image_data=image_data, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6)

@app.route('/switchnegativeimage', methods=['GET', 'POST'])
def switchnegative():
    if request.method == 'POST' or request.method=='GET':
        # Allocate image accordingly
        # Alter image_data to next image we want to load in
        # Alter image 1-6 as top 6 ranked images
        # use top_images = dataframe.nlargest(6, 'Confidence')
        if orange.count < len(orange.image_set):
            orange.initialisation_run()
        else:
            image = orange.main_run(response=-1.0)

        image_location = "../static/images/" + image.ImagePath.iloc[0]
        image_data = {'image_src': image_location}

        image1 = {'image1': "../static/images/" + image.ImagePath.iloc[1]}
        image2 = {'image2': "../static/images/" + image.ImagePath.iloc[2]}
        image3 = {'image3': "../static/images/" + image.ImagePath.iloc[3]}
        image4 = {'image4': "../static/images/" + image.ImagePath.iloc[4]}
        image5 = {'image5': "../static/images/" + image.ImagePath.iloc[5]}
        image6 = {'image6': "../static/images/" + image.ImagePath.iloc[6]}

        orange.count += 1
        return render_template('home.html', image_data=image_data,image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6)
    
@app.route('/switchpositiveimage', methods=['GET','POST'])
def switchpositiveimage():
    if request.method == 'POST' or request.method=='GET':
        # Allocate image accordingly
        # Alter image_data to next image we want to load in
        # Alter image 1-6 as top 6 ranked images
        # use top_images = dataframe.nlargest(6, 'Confidence')
        if orange.count < 38:
            orange.initialisation_run()
        else:
            image = orange.main_run(response=1.0)

        image_location = "../static/images/" + image.ImagePath.iloc[0]
        image_data = {'image_src': image_location}

        image1 = {'image1': "../static/images/" + image.ImagePath.iloc[1]}
        image2 = {'image2': "../static/images/" + image.ImagePath.iloc[2]}
        image3 = {'image3': "../static/images/" + image.ImagePath.iloc[3]}
        image4 = {'image4': "../static/images/" + image.ImagePath.iloc[4]}
        image5 = {'image5': "../static/images/" + image.ImagePath.iloc[5]}
        image6 = {'image6': "../static/images/" + image.ImagePath.iloc[6]}

        orange.count += 1
        return render_template('home.html', image_data=image_data,image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6)

@app.route("/about")
def about():
    return render_template('about.html', posts=dummy_data)


if  __name__ =='__main__':
    app.run(debug=True)

