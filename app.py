from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def contact_form():
    return render_template('contact_form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    subject = request.form.get('subject')
    other_subject = request.form.get('other_subject')
    preferred_methods = request.form.getlist('preferred')
    agreement = request.form.get('agreement')

    errors = []

    if not name or not email or not phone or not message:
        errors.append("All fields are required.")
    if not phone.isdigit():
        errors.append("Phone number must be numeric.")
    if subject == "Other" and not other_subject:
        errors.append("Please specify the subject.")
    if agreement != "on":
        errors.append("You must agree to the terms.")

    if errors:
        return render_template('contact_form.html', errors=errors, form=request.form)

    final_subject = other_subject if subject == "Other" else subject

    return render_template('confirmation.html',
                           name=name,
                           email=email,
                           phone=phone,
                           message=message,
                           subject=final_subject,
                           preferred=preferred_methods,
                           agreement="Yes" if agreement == "on" else "No")

if __name__ == '__main__':
    app.run(debug=True)