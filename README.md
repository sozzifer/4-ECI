# 4-ECI
Confidence intervals

Python version 3.10

To run, create a Python virtual environment and install the packages as specified in requirements.txt using pip install -r requirements.txt

To deploy on Docker, replace app.run(debug=True) in eci_controller.py with the following:
app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)