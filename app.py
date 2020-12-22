from flask import Flask, jsonify
from flask import request
import pickle
from sklearn.ensemble import RandomForestRegressor

# load the previously persisted ML assets
with open('model/final_model.sav', 'rb') as f: 
	rfr=pickle.load(f)
with open('model/input_columns.sav', 'rb') as f: 
	input_columns=pickle.load(f)
with open('model/input_scaler.sav', 'rb') as f: 
	scaler=pickle.load(f)

# app=Flask(__name__)
app=Flask(__name__)

@app.route('/')
def index(): 
	welcome_message='<h3>Welcome to Salary Prediction</h3><h4>Please use the /predict route</h4><h4>Below are some query parameters:</h4>'
	query_parameters='''
					'YearsCodePro': 

					'''
	print(input_columns)
	# return welcome_message
	return jsonify(list(input_columns))

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

@app.route('/test/')
def test(): 
	# inputs={'YearsCodePro': 10, 'Data scientist or machine learning specialist': 1, 'Windows': 1}
	# inputs={'YearsCodePro': 10, 
	#        'Data scientist or machine learning specialist': 1, 
	#        'MacOS': 1, 
	#        'Other doctoral degree (Ph.D., Ed.D., etc.)': 1}
	inputs={'YearsCodePro': request.args.get('YearsCodePro', 0), 
			'Windows': request.args.get('Windows', 0), 
			'Data scientist or machine learning specialist': request.args.get('Data_Scientist', 0), 
			'Other doctoral degree (Ph.D., Ed.D., etc.)': request.args.get('Doctoral', 0)}
	input_ary=[inputs[each_feature] if (each_feature in inputs) else 0 for each_feature in input_columns]
	input_scaled=scaler.transform([input_ary])
	# prediction=rfr.predict(input_scaled)
	# return jsonify(rfr.predict(input_scaled)[0])
	return jsonify({'inputs': inputs, 'output': rfr.predict(input_scaled)[0]})
	# return jsonify(input_ary)

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


	# 'Data scientist or machine learning specialist': request.args.get('Data scientist or machine learning specialist', ''), 
			# 'Other doctoral degree (Ph.D., Ed.D., etc.)': request.args.get('Other doctoral degree (Ph.D., Ed.D., etc.)', '')}
			# input_ary=[inputs[each_feature] if (each_feature in inputs) else 0 for each_feature in input_columns]
			# input_scaled=scaler.transform([input_ary])
			# # prediction=rfr.predict(input_scaled)
			# return jsonify(rfr.predict(input_scaled)[0])