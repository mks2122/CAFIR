from flask import Flask,render_template,request,redirect,url_for

isSignedIn = False
app = Flask(__name__,template_folder='template',static_folder='static')

@app.route('/')
def home():
    # print("signed in the page??????",isSignedIn)
    if isSignedIn:
        return 'done'
    # print('donw')
    return render_template('login.html')


users=['admin','harry','ron','hermione']
passwords=['admin','potter','weasley','granger']

@app.route('/login',methods=['GET','POST'])
def login():
    print(request.form)
    if request.method == 'POST':
        usr, pwd = request.form['Username'], request.form['password']

    if usr in users:
        if pwd == passwords[users.index(usr)]:
            isSignedIn = True  
            print('Logged in')
            return redirect('/fir')
    return render_template('login.html',message='Invalid Username or Password')


@app.route('/logout')
def logout():
    isSignedIn = False
    return redirect('/')


@app.route('/fir')
def fir():
    return render_template('fIR.html')

@app.route('/firDetails', methods=['GET','POST'])
def fir_details():
    # Extracting form data
    name = request.form.get('name')
    father_or_husband_name = request.form.get('fatherOrHusbandName')
    address = request.form.get('address')
    phone_number = request.form.get('phoneNumber')
    email = request.form.get('email')
    distance_from_police_station = request.form.get('distanceFromPoliceStation')
    direction_from_police_station = request.form.get('directionFromPoliceStation')
    date_and_hour_of_occurrence = request.form.get('dateAndHourOfOccurrence')
    nature_of_offence = request.form.get('natureOfOffence')
    stolen_property_description = request.form.getlist('stolenPropertyDescription[]')
    accused_names = request.form.getlist('accusedName[]')
    witness_names = request.form.getlist('witnessName[]')
    complaint = request.form.get('complaint')

    # You can process or save this data in a database or use it as needed
    # For this example, let's just print it
    print("Complainant Details:")
    print(f"Name: {name}")
    print(f"Father's/Husband's Name: {father_or_husband_name}")
    print(f"Address: {address}")
    print(f"Phone Number: {phone_number}")
    print(f"Email: {email}")
    print("\nPlace of Occurrence:")
    print(f"Distance from Police Station: {distance_from_police_station}")
    print(f"Direction from Police Station: {direction_from_police_station}")
    print(f"Date and Hour of Occurrence: {date_and_hour_of_occurrence}")
    print("\nOffence Details:")
    print(f"Nature of Offence: {nature_of_offence}")
    print("\nStolen Property (if applicable):")
    for desc in stolen_property_description:
        print(f"Description: {desc}")
    print("\nAccused Details:")
    for name in accused_names:
        print(f"Accused Name: {name}")
    print("\nWitness Details:")
    for name in witness_names:
        print(f"Witness Name: {name}")
    print(f"\nComplaint Description: {complaint}")

    return redirect('/fir')  # Redirect back to the form or render a success page






if __name__ == '__main__':    
    app.run(debug=True)