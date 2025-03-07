import streamlit as st
import pickle

movies1=pickle.load(open('movies.pkl','rb'))
movies_list=pickle.load(open('movies_list.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
        movie_index= movies1[movies1['title']==movie].index[0]
        distances=similarity[movie_index]  
        movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
        recommended_movies=[]
        for i in movies_list:
            recommended_movies.append(movies1.iloc[i[0]].title)
        return recommended_movies

st.title("Movie Recomender")
selected_movie=st.selectbox("Enter your last seen movie:",
movies_list)
   
if st.button("Recommend"):
    r=recommend(selected_movie)
    for i in r:
        st.write(i)
