Dependencies:
pip install flask pyhive thrift-sasl pandas JayDeBeApi JPype1
sudo pip install JayDeBeApi JPype1 # if failed to install JayDeBeApi JPype1

Check:
pip show flask pyhive thrift-sasl pandas
pip show JayDeBeApi JPype1
python --version
pip3 --version

if unable to run pip:
sudo yum install python3-pip

Run the app.py:
export FLASK_APP=app.py
python -m flask run

Zip the Python_flask project and Move to the VM server:
ip a  # VM IP
scp -r /d/PROJECTS/PYTHON_FLASK_HIVE/Python_flask.zip knight@192.168.0.17:/home/knight/

In Linux:
cd /home/knight/Applications/Python_flask/python_app
export FLASK_APP=app.py
python3 -m flask run


