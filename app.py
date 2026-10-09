import streamlit as st
import pickle
import pandas as pd

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore',
    'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur',
    'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
    'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur',
    'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur',
    'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali',
    'Bengaluru'
]

with open('pipe.pkl', 'rb') as file:
    pipe = pickle.load(file)

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox(
        'Select the batting team', sorted(teams)
    )

with col2:
    bowling_team = st.selectbox(
        'Select the bowling team', sorted(teams)
    )

selected_city = st.selectbox(
    'Select host city', sorted(cities)
)

target = st.number_input(
    'Target', min_value=1, max_value=300, value=180
)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input(
        'Score', min_value=0, max_value=300, value=100
    )

with col4:
    overs = st.number_input(
        'Overs completed', min_value=0.0,
        max_value=20.0, value=10.0, step=0.1
    )

with col5:
    wickets = st.number_input(
        'Wickets out', min_value=0, max_value=10, value=3
    )

if st.button('Predict Probability'):

    if batting_team == bowling_team:
        st.error('Please select two different teams.')

    elif score >= target:
        st.success(f'{batting_team} has reached the target!')

    elif overs >= 20 or wickets >= 10:
        st.error('The innings is over.')

    else:
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets

        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)[0]

        lose = result[0]
        win = result[1]

        st.subheader('Match Prediction')

        st.success(
            f'{batting_team} win probability: {win * 100:.1f}%'
        )

        st.info(
            f'{bowling_team} win probability: {lose * 100:.1f}%'
        )
