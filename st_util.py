import streamlit as st
from Game import Game
import pandas as pd
import plotly.express as px

@st.cache_resource
def get_global_game():
    """Returns the shared instance of the game."""
    return Game()

@st.cache_data
def get_choice_histogram(choice_dict: dict):
    if not choice_dict:
        return None

    df = pd.DataFrame(list(choice_dict.values()), columns=["Production"])
    fig = px.histogram(
        df, 
        x="Production", 
        nbins=5, 
        range_x=[0.5, 5.5],
        title="Distribution of Factory Decisions",
        labels={"Production": "Tons Produced"}
    )
    fig.update_layout(bargap=0.2)
    return fig

    
