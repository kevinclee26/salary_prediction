from flask import Flask, jsonify
from flask import request
import pickle

# app=Flask(__name__)
app=Flask(__name__)

# load trained classifier
clf_path='lib/models/SentimentClassifier.pkl'
with open(clf_path, 'rb') as f:
    model=pickle.load(f)

@app.route('/')
def index(): 
	return 'Welcome'


@app.route('/sample/')
def sample():
    return jsonify({'title': 'data scientist', 'city': 'san francisco'})

# this method takes + as literal
# this method handles &
# @app.route('/predict/')
# @app.route('/predict/<query_string>')
# # def predict(query_string=''): 
# def predict(query_string): 
# 	output='machine_learning_model_output'
# 	return jsonify({'Inputs': query_string, 'Results': output})
# 	# return jsonify(output)

# this method takes + as space
# this method separates with &
# this path doesn't handle & symbol well
@app.route('/predict')
@app.route('/predict/')
def predict(): 
	output='machine_learning_model_output'
	# use flat=False to return as list - enables multiple values to same param
	query_params=request.args.to_dict()
	# return_dict={
	# 	# 'Inputs': request.args.get('input', ''), 
	# 	'Result': output
	# }
	query_params['results']=output
	# return jsonify({'Inputs': query_string, 'Results': output})
	# return jsonify(request.args.get('input'))
	# return jsonify(return_dict)
	return jsonify(query_params)


if __name__=='__main__': 
	app.run()