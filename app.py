import pickle
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="CineVerse AI Recommender",
    page_icon="🌌",
    layout="wide"
)

def add_css():
    st.markdown("""
    <style>
    /* Import Google Font 'Poppins' */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Set the imported font */
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main app background: A deep, professional gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right top, #0c0a1e, #1a1a3a, #0c0a1e);
        color: white;
    }
    
    /* Hide Streamlit Header & Footer */
    [data-testid="stHeader"] {
        background: none;
    }
    footer {
        visibility: hidden;
    }
    
    /* Title styling: Gradient text */
    h1 {
        text-align: center;
        font-weight: 700;
        font-size: 3.5rem;
        background: linear-gradient(90deg, #FF4B4B, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 15px rgba(255, 75, 75, 0.3);
    }
    
    /* Frosted glass effect for the select box */
    [data-testid="stSelectbox"] > div {
        background-color: rgba(10, 10, 30, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
    }
    .st-af {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Button styling: Neon/Gradient with shadow */
    .stButton > button {
        color: #FFFFFF;
        background: linear-gradient(90deg, #FF4B4B, #FF0000);
        border: none;
        border-radius: 10px;
        padding: 14px 30px;
        font-size: 18px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.5);
        background: linear-gradient(90deg, #FF6B6B, #FF2020);
        color: #FFFFFF;
    }
    
    /* Separator line style */
    [data-testid="stDivider"] {
        background: linear-gradient(90deg, #FF4B4B, #FFD700);
        height: 2px;
        border: none;
    }

    /* Subheader for "Recommendations" */
    h3 {
        color: #FFFFFF;
        text-align: center;
        font-weight: 600;
    }
    
    /* This styles the container for each movie card */
    [data-testid^="stVerticalBlock"] {
        transition: all 0.3s ease-in-out;
    }

    /* This adds the "lift" and glow effect on hover */
    [data-testid^="stVerticalBlock"]:hover {
        transform: translateY(-10px) scale(1.03);
        z-index: 10;
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.3);
    }
    
    /* Poster Card: Top corners rounded */
    .stImage img {
        border-radius: 10px 10px 0 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
    }
    
    /* Title Card: Glued to the poster, bottom corners rounded */
    .stCaption {
        text-align: center;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 16px;
        margin-top: -10px;
        padding: 15px;
        background-color: rgba(30, 30, 50, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 0 0 10px 10px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)

add_css()


@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies, similarity = load_data()


st.markdown("<h1>CineVerse AI</h1>", unsafe_allow_html=True)
st.write("") 

_, col_centered, _ = st.columns([1.5, 2, 1.5])
with col_centered:
    selected_movie_name = st.selectbox(
        "Select a movie you like:",
        movies['title'].values,
        label_visibility="collapsed",
        placeholder="Type or select a movie to get recommendations..."
    )

st.write("") 

_, col_btn, _ = st.columns([2.5, 1, 2.5])
with col_btn:
    show_recommendations = st.button('Recommend')

if show_recommendations:
    st.divider()
    st.markdown("<h3>Curated For You</h3>", unsafe_allow_html=True)
    st.write("")

    with st.spinner('Generating your cinematic universe...'):
        names, posters = recommend(selected_movie_name)
        
        col1, col2, col3, col4, col5 = st.columns(5, gap="large")
        
        with col1:
            st.image(posters[0])
            st.caption(names[0]) 

        with col2:
            st.image(posters[1])
            st.caption(names[1])

        with col3:
            st.image(posters[2])
            st.caption(names[2])

        with col4:
            st.image(posters[3])
            st.caption(names[3])

        with col5:
            st.image(posters[4])
            st.caption(names[4])