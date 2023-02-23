from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__, static_folder='static' )


# Load the saved model from file
model = joblib.load('movie_success_model.joblib')

# Set up the list of genres
genres_list = ['Action', 'Romance', 'Thriller', 'Comedy', 'Drama']
language_list = ['en', 'es', 'fr']

@app.route('/')
def home():
    return render_template('index.html', results = '')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the form
    budget = int(request.form['budget'])
    popularity = float(request.form['popularity'])
    runtime = int(request.form['runtime'])
    vote_average = float(request.form['vote_average'])
    revenue = int(request.form['revenue'])
    selected_genres = request.form['genres']
    original_language = request.form['original_language']

      # Create a dictionary to hold the input data
    input_data = {
        'budget': budget,
        'popularity': popularity,
        'runtime': runtime,
        'vote_average': vote_average,
        'revenue': revenue
    }

      # Set the values of the non-selected genres to 0 in the input data
    for genre in genres_list:
        input_data[f'genres_{genre}'] = 0

        # Set the values of the selected genres to 1 in the input data
    input_data[f'genres_{selected_genres}'] = 1
    
    # Set the values of the non-selected genres to 0 in the input data
    for lan in language_list:
        input_data[f'original_language_{lan}'] = 0

    input_data[f'original_language_{original_language}'] = 1
  
    # Convert the input data to a dataframe
    input_df = pd.DataFrame([input_data])

    input_df = input_df[['budget', 'popularity', 'revenue', 'runtime', 'vote_average',
       'original_language_en', 'original_language_es', 'original_language_fr',
       'genres_Action', 'genres_Comedy', 'genres_Drama', 'genres_Romance',
       'genres_Thriller']]

    print(input_df)
    # Use the model to make predictions on the input data
    predictions = model.predict(input_df)
    print(predictions)
    # Return the prediction to the user
    if predictions[0] == 1:
        result = 'Your curated movie would be successful'
    else:
        result = 'Your curated movie would be unsuccessful'
    print(result)
    return render_template("index.html", result = result)

@app.route('/visualizations.html')
def visualizations():
    return render_template('visualizations.html')

@app.route('/index.html')
def movie():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
