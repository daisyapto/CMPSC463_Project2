"""
References:
https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/
https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application
https://www.w3schools.com/html/html_forms.asp
https://www.w3schools.com/html/tryit.asp?filename=tryhtml_form_submit
Chat GPT-- Flask explanation
"""

from App.route import app
import webbrowser, os
from threading import Timer


# Automatically open browser
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Prevent opening browser in debug mode
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, open_browser).start()
    app.run(debug=True)

