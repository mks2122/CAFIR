from flask import Flask,render_template,request,redirect,url_for,jsonify

from blockchain import store_case, update_case_status, close_case, get_case_details, detailsGetter

import random

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


@app.route('/firIntermediate', methods=['GET','POST'])
def fir_intermediate():
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Parse and extract individual fields from the JSON
        name = data.get('name')
        father_or_husband_name = data.get('fatherOrHusbandName')
        address = data.get('address')
        phone_number = data.get('phoneNumber')
        email = data.get('email')
        
        # Place of occurrence
        distance_from_police_station = data.get('distanceFromPoliceStation')
        direction_from_police_station = data.get('directionFromPoliceStation')
        date_and_hour_of_occurrence = data.get('dateAndHourOfOccurrence')

        # Offence details
        nature_of_offence = data.get('natureOfOffence')

        # Arrays (optional)
        stolen_property_descriptions = data.get('stolenPropertyDescriptions')
        accused_names = data.get('accusedNames')
        witness_names = data.get('witnessNames')

        # Complaint text
        complaint = data.get('complaint')
        id=data.get('id')

        # For testing purposes, we just print or return the data.
        # In actual use, you might want to save it to a database or process it further.
        print({
            "name": name,
            "father_or_husband_name": father_or_husband_name,
            "address": address,
            "phone_number": phone_number,
            "email": email,
            "distance_from_police_station": distance_from_police_station,
            "direction_from_police_station": direction_from_police_station,
            "date_and_hour_of_occurrence": date_and_hour_of_occurrence,
            "nature_of_offence": nature_of_offence,
            "stolen_property_descriptions": stolen_property_descriptions,
            "accused_names": accused_names,
            "witness_names": witness_names,
            "complaint": complaint
        })

        fir_number = str(random.randint(100000, 999999)) if id == None else id
        print(f"--------------------------- {id} ---------------------------")
        print(f"--------------------------- {fir_number} ---------------------------")
        store_case(fir_number, name, father_or_husband_name, address, phone_number, email, 
               distance_from_police_station, direction_from_police_station, date_and_hour_of_occurrence, 
               nature_of_offence, stolen_property_descriptions, accused_names, witness_names, "Pending")

        # Return a response to the client
        return jsonify({"message": "FIR details received successfully!", id:fir_number})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Something went wrong!"})

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
    stolen_property_description = request.form.get('stolenPropertyDescription[]')
    accused_names = request.form.get('accusedName[]')
    witness_names = request.form.get('witnessName[]')
    complaint = request.form.get('complaint')
    id=request.form.get('id')

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
    # for desc in stolen_property_description:
    print(f"Description: {stolen_property_description}")
    print("\nAccused Details:")
    # for name in accused_names:
    print(f"Accused Name: {accused_names}")
    print("\nWitness Details:")
    # for name in witness_names:
    print(f"Witness Name: {witness_names}")
    print(f"\nComplaint Description: {complaint}")

    # Store the FIR on the blockchain and SQL database
    fir_number = str(random.randint(100000, 999999)) if id == None else id
    store_case(fir_number, name, father_or_husband_name, address, phone_number, email, 
               distance_from_police_station, direction_from_police_station, date_and_hour_of_occurrence, 
               nature_of_offence, stolen_property_description, accused_names, witness_names, "Not Investigated")

    return redirect('/success')  # Redirect back to the form or render a success page


@app.route('/details')
def details():

    tables,dic=detailsGetter()
    # print(tables)
    
    
    return render_template('Display.html',fir_data=dic)

@app.route('/success')
def success():
    return render_template('successPage.html')  


if __name__ == '__main__':    
    app.run(debug=True)