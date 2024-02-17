from flask import Flask, render_template_string
app = Flask(__name__)

@app.route("/api/python", methods=['GET'])
def submit_form():
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