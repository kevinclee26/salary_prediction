import pickle

model_path='ml_model.pkl'
with open(model_path, 'rb') as f: 
	pickle.load(f)

def make_prediction(user_inputs): 
	model_input=transform_inputs(user_input)
	if model_input: 
		prediction=model.predict(model_input)
		return prediction
	else: 
		return 'Bad Inputs'

def transform_inputs(input_string): 
	return input_array