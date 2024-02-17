from helper_code.find_predicates import predicates
from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/api/python", methods=['GET'])
def view_form():
    form_html = '''
    <form action="/api/handle-form" method="post">
        <label for="device-description">Device Description:</label><br>
        <input type="text" id="device-description" name="device-description" required><br>
        <label for="indication-for-use">Indication for Use:</label><br>
        <input type="text" id="indication-for-use" name="indication-for-use" required><br><br>
        <input type="submit" value="Submit">
    </form> 
    '''
    return render_template_string(form_html)

@app.route("/api/handle-form", methods=['POST'])
def handle_form():
    # Retrieve form data
    device_description = request.form['device-description']
    indication_for_use = request.form['indication-for-use']
    
    # Process the form data (for demonstration, print it to console)
    print(f"Device Description: {device_description}")
    print(f"Indication for Use: {indication_for_use}")
    
    # Generate the response page with the submitted data
    response_page_html = f'''
    <p>Device Description {device_description} </p>
    <p>Indication for Use: {indication_for_use}<p>
    <a href="/api/python">Submit another response</a>
    '''

    device_data = {
        "Device Description": device_description,
        "Indication for Use": indication_for_use
    }
    
    top_k_numbers = predicates(device_data)

    return render_template_string(response_page_html)