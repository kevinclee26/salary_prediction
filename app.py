from flask import Flask, request, jsonify
import json
import pickle

# load the previously persisted ML assets
with open('assets/model/final_model.sav', 'rb') as f: 
	rfr=pickle.load(f)
with open('assets/model/input_columns.sav', 'rb') as f: 
	input_columns=pickle.load(f)
with open('assets/model/input_scaler.sav', 'rb') as f: 
	scaler=pickle.load(f)
with open('assets/model/input_dictionary.json', 'r') as f: 
    input_dictionary=json.load(f)
    column_dict={}
    for key in input_dictionary.keys(): 
    	if input_dictionary[key]['type']=='categorical': 
    		column_dict.update(input_dictionary[key]['options'])

app=Flask(__name__)

@app.route('/')
def index(): 
	welcome_message='<h1>Welcome to Salary Predictor</h1><h3>Use the /salary route. Below are the query parameters:</h3>'
	query_params='<img src="static/image/sample.png" alt="sample"><hr>'
	for each_key in input_dictionary.keys(): 
		query_params+=f'<p><b>{each_key}</b> - {input_dictionary[each_key]["definition"]}</p>'
		if input_dictionary[each_key]['type']=='categorical': 
			for input_str, feature in input_dictionary[each_key]['options'].items(): 
				query_params+=f'<li><b>{input_str}</b> - {feature}</li>'
	# return welcome_message
	return welcome_message+query_params

@app.route('/sample/')
@app.route('/sample')
def sample(): 
	inputs={'YearsCodePro': 10, 
			'Bachelor’s degree (B.A., B.S., B.Eng., etc.)': 1,
			'Data scientist or machine learning specialist': 1, 
			'MacOS': 1}
	input_ary=[inputs[each_feature] if (each_feature in inputs) else 0 for each_feature in input_columns]
	input_scaled=scaler.transform([input_ary])
	# prediction=rfr.predict(input_scaled)
	return jsonify({'input(s)': inputs, 'output': round(rfr.predict(input_scaled)[0], 2)})

# this method takes + as literal
# this method handles &
# @app.route('/predict/')
# @app.route('/predict/<query_string>')
# # def predict(query_string=''): 
# def predict(query_string): 
# 	output='machine_learning_model_output'
# 	return jsonify({'Inputs': query_string, 'Results': output})

# this method takes + as space
# this method separates with &
# this path doesn't handle & symbol well
# @app.route('/predict')
# @app.route('/predict/')
# def predict(): 
# 	output='machine_learning_model_output'
# 	# use flat=False to return as list - enables multiple values to same param
# 	query_params=request.args.to_dict()
# 	return_dict={
# 		# 'Inputs': request.args.get('input', ''), 
# 		'Result': output
# 	}
# 	query_params['results']=output
# 	return jsonify(return_dict)

@app.route('/predict/')
@app.route('/predict')
def predict(): 
	inputs={'YearsCodePro': request.args.get('YearsCodePro', 0)}
	cat_inputs={'OpSys': request.args.get('OpSys'), 
			'EdLevel': request.args.get('EdLevel'), 
			'DevType': request.args.get('DevType')}
	inputs.update({column_dict[name]: 1 for name in cat_inputs.values() if name in column_dict.keys()})
	input_ary=[inputs[each_feature] if (each_feature in inputs) else 0 for each_feature in input_columns]
	input_scaled=scaler.transform([input_ary])
	# prediction=rfr.predict(input_scaled)
	return jsonify({'input(s)': inputs, 'output': round(rfr.predict(input_scaled)[0], 2)})

if __name__=='__main__': 
	app.run()