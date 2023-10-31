from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("C:/Users/User/Desktop/Hotel_stats6.csv")
hotel_data = df

@app.route('/')
def index():
    # Get unique values for 'Country', 'Room_Type', and 'Trip_Type' from the DataFrame    
    # Filter out non-string values and apply str.strip()
    unique_countries = [str(country).strip() for country in df['Country'].unique() if isinstance(country, str)]
    unique_metro_types = [str(metro).strip() for metro in df['metro'].unique() if isinstance(metro, str)]
    unique_pool_types = [str(pool).strip() for pool in df['Pool'].unique() if isinstance(pool, str)]
    return render_template('index.html', unique_countries=unique_countries, unique_metro_types=unique_metro_types, unique_pool_types=unique_pool_types)


@app.route('/search', methods=['POST'])
def search():
    pool = request.form['pool']
    country = request.form['country']
    metro = request.form['metro']

    min_score = float(request.form['min_score'])  # Add this line to get the minimum score from the form 
    #min_score = round(float(request.form['min_score']), 2)
    # Filter the DataFrame based on user input
    filtered_df = df[(df['Pool'] == pool) & (df['Country'] == country) & (df['metro'] == metro) & (df['Average_Score'] >= min_score)]
    filtered_df['Average_Score'] = filtered_df['Average_Score'].round(1)
    filtered_df['Average_review_score'] = filtered_df['Average_review_score'].round(1)  # Round the Average_review_score to 2 decimal places

    # Sort the filtered DataFrame by average rating
    sorted_df = filtered_df.sort_values(by='Average_review_score', ascending=False)

    return render_template('search_results.html', sorted_df=sorted_df)

if __name__ == '__main__':
    app.run(debug=True)
