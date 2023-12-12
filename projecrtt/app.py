
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid
app = Flask(__name__,template_folder='/Users/gurnam/projecrtt/template/'
            )



#for mail configuring some parameters 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Project04822@gmail.com'
app.config['MAIL_PASSWORD'] = 'ncllmyvfsqtyedsc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)







# model and necessary data
Job=pd.read_csv("jobprediction.csv")
Admission_Data = pd.read_csv("college admission prediction.csv")
model = joblib.load('Admission_Prediction.joblib')
college = np.unique(Admission_Data['College'])

comments_set1 = []
comments_set2 = []
current_set = comments_set1

@app.route('/')
def more():
    return render_template('more.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/index')
def index():
    return render_template('index.html')

#for mail
@app.route('/form',methods=["GET","POST"])
def form():
   if request.method=='POST':
    msg=request.form.get('message')
    email=request.form.get('email')
    name=request.form.get('name')
    field=request.form.get('field')
    bod=Message('HEY !',sender='Project04822@gmail.com',recipients=['Project04822@gmail.com'])
    bod.body='USER NAME : {} \n EMAIL : {} \n FIELD : {} \n MESSAGE : {}  \n '.format(name,email,field,msg)
    mail.send(bod)
   return render_template('contact.html')


#to update comment form at index page
@app.route('/comments', methods=['GET'])
def comments():
   global current_set
   print ("Got  Info")
   text = request.args.get('comment')
   current_set.append(text)
   if current_set is comments_set1:
        current_set = comments_set2
   else:
        current_set = comments_set1
   # redirects back to the '/' route
   return render_template('index.html',comments_set1=comments_set1, comments_set2=comments_set2)

IMAGE_DIR = os.path.join(app.root_path, 'images')
os.makedirs(IMAGE_DIR, exist_ok=True)

def generate_graph(user_state):
    filtered_data = Job[Job['college_state'] == user_state]

    if filtered_data.empty:
        return None

    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data['specialisation'], filtered_data['salary'])
    plt.xlabel('Specialization')
    plt.ylabel('Salary')
    plt.title(f'Salary vs Specialization in {user_state}')

    # Save the plot as an image file
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(IMAGE_DIR, filename)
    plt.savefig(filepath, format='png')
    plt.close()

    return filename

@app.route('/jobgraph', methods=['POST'])
def jobgraph():
    try:
        data = request.get_json()
        user_state = data['state']
        
        # Generate the graph and get the filename
        filename = generate_graph(user_state)

        if filename:
            # Provide the link to the image file
            image_url = f"/images/{filename}"
            return jsonify({'graph': image_url})
        else:
            return jsonify({'message': f'No data found for the state: {user_state}'})

    except Exception as e:
        return jsonify({'error': f'Error generating graph: {str(e)}'})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        usrip = data['usrip']

        # Make sure usrip is a list
        usrip = [float(usrip)]  # Assuming usrip is a numerical value
        print('Processed input:', usrip)
        # Reshape the input to a 2D array
        user_preddt = model.predict(np.array(usrip).reshape(1, -1))
        print('predicted ',user_preddt)
        # Convert the predicted college code back to college name using clg_code
        predicted_college = college[int(user_preddt[0])]


        return jsonify({'predicted_college': predicted_college})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)