import streamlit as st
from typing import List
import pandas as pd
from streamlit_lottie import st_lottie
import json
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os

class GolfCourse:
    def __init__(self, name: str, hole_count: int, par: int, holes: List["Hole"]):
        self.name = name
        self.hole_count = hole_count
        self.par = par
        self.holes = holes


class Golfer:
    def __init__(self, name: str, scores: List[int]):
        self.name = name
        self.scores = scores


class Hole:
    def __init__(self, number, name, par):
        self.number = number
        self.name = name
        self.par = par


def load_course(filepath):
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            name, par, hole_count = None, None, None
            holes = []
            for line in lines:
                tokens = line.strip().split(",")
                if tokens[0] == "C":
                    try:
                        name = tokens[1]
                        par = int(tokens[2])
                        hole_count = int(tokens[3])
                    except IndexError:
                        st.error("Invalid file format. Please upload a valid golf course file.")
                        return None
                elif tokens[0] == "H":
                    try:
                        if len(tokens) != 4:  # Validate the number of tokens
                            st.error("Invalid file format. Please upload a valid golf course file.")
                            return None
                        hole_number = int(tokens[1])
                        hole_name = tokens[2]
                        hole_par = int(tokens[3])
                        holes.append(Hole(hole_number, hole_name, hole_par))
                    except IndexError:
                        st.error("Invalid file format. Please upload a valid golf course file.")
                        return None
            if name is None or par is None or hole_count is None:
                st.error("Invalid file format. Please upload a valid golf course file.")
                return None
            return GolfCourse(name, hole_count, par, holes)
    except FileNotFoundError:
        st.error("File not found. Please choose a valid course file.")
        return None

    


def get_golfer_scores(holes: List[Hole]) -> Golfer:
    # Split the holes list into front nine and back nine
    front_nine = holes[:9]
    back_nine = holes[9:]

    # Create two columns
    col1, col2 = st.columns(2)

    # Get golfer information in first column
    st.sidebar.subheader("Enter the golfer's information:")
    name = st.sidebar.text_input("Name:")

    # Get front nine scores in second column
    with col1:
        st.subheader("Enter the golfer's scores - ↪️9️⃣Front Nine:")
        front_scores = []
        for i, hole in enumerate(front_nine):
            score = st.number_input(f"Hole {i+1} - {hole.name} (Par {hole.par}):", min_value=1, value=hole.par)
            front_scores.append(score)
    # Add a line between the two columns
    st.markdown("---")

    # Get back nine scores in second column
    with col2:
        st.subheader("Enter the golfer's scores - ↩️9️⃣Back Nine:")
        back_scores = []
        for i, hole in enumerate(back_nine):
            score = st.number_input(f"Hole {i+10} - {hole.name} (Par {hole.par}):", min_value=1, value=hole.par)
            back_scores.append(score)

    # Combine front nine and back nine scores into a single list
    scores = front_scores + back_scores

    # Return Golfer object with name and scores
    return Golfer(name, scores)




def get_shot_category(score, par):
    diff = score - par
    if score == 1:
        return "Ace"
    elif diff == -3:
        return "Albatross"
    elif diff == -2:
        return "Eagle"
    elif diff == -1:
        return "Birdie"
    elif diff == 0:
        return "Par"
    elif diff == 1:
        return "Bogey"
    elif diff == 2:
        return "Double Bogey"
    else:
        return "Triple or Worse"

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def create_score_chart(golfer: Golfer, par: int, course: GolfCourse) -> go.Figure:
    # Create a list of x-axis labels
    labels = [f"Hole {i+1}" for i in range(course.hole_count)]

    # Create a trace for the golfer's net score
    golfer_scores = [score for score in golfer.scores]
    trace1 = go.Scatter(x=labels, y=golfer_scores, mode="lines+markers", name="Score", line=dict(color="#C8DBBE"))

    # Create a trace for the par
    par_scores = [hole.par for hole in course.holes]
    trace2 = go.Scatter(x=labels, y=par_scores, mode="lines+markers", name="Par", line=dict(dash="dash", color="#4A0404"))

    # Create the layout for the chart
    layout = go.Layout(title=f"{golfer.name}'s Score vs. Par", xaxis_title="Hole", yaxis_title="Score")


    # Create the figure and add the traces to it
    fig = go.Figure(layout=layout)
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    # Show the chart
    return fig

def download_text_file():
    text = '''C,Whistling Straits,72,18
H,1,Outward Bound,4
H,2,Cross Country,5
H,3,O'Man,3
H,4,Glory,4
H,5,Snake,5
H,6,Gremlin's Ear,4
H,7,Shipwreck,3
H,8,On the Rocks,4
H,9,Down and Dirty,4
H,10,Voyageur,4
H,11,Sand Box,5
H,12,Pop up,3
H,13,Cliff Hanger,4
H,14,Widow's Watch,4
H,15,Grand Stand,4
H,16,Endless Bite,5
H,17,Pinched Nerve,3
H,18,Dyeabolical,4'''

    # Convert text to bytes
    text_bytes = text.replace('\n', '\r\n').encode('utf-8')

    
    # Set up download button
    st.download_button(
        label='🧪 Download Test File',
        data=text_bytes,
        file_name='GolfCourse.txt',
        mime='text/plain'
    )

def main():
    st.set_page_config(page_title="Golf Score Tracker", page_icon=":golf:", layout="wide")

    # Display the app title and description
    st.title("⛳Golf Score Tracker")
    st.success("_Welcome to the Golf Score Tracker app! Use this app to keep track of your golf scores and view your shot categories for each hole._")
    course_file = st.file_uploader("Upload a golf course file:", type="txt", help=f"🗃️ Golf course files should be formatted-Course: C,Whistling Straits,72,18 Holes: H,1,Outward Bound,4")
    show_expander = True
    course = None

    if course_file is not None:
        try:
            file_path = os.path.join(os.getcwd(), course_file.name)
            with open(file_path, "wb") as file:
                file.write(course_file.getvalue())
            course = load_course(file_path)
            if course is not None:
                st.subheader(f"⛳Loaded course: {course.name} ({course.hole_count} holes, par {course.par})")
            os.remove(file_path)
            show_expander = False
        except ValueError:
            st.error("Invalid file type. Please upload a valid text file.")
            return
        except AttributeError:
            return

    if show_expander:
        with st.expander("👇 Download an example file"):
            download_text_file()
    else:
        st.divider()

    if course is not None:    
        golfer = get_golfer_scores(course.holes)
        
    
        # Create a container for golfer information
        golfer_container = st.container()
        with golfer_container:
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.subheader(f"🏌️Golfer: {golfer.name}")
            total_score = sum(golfer.scores)
            col2.subheader(f"🏁Total score: {total_score}")
            par_diff = total_score - course.par
            if par_diff < 0:
                col3.subheader(f"-{abs(par_diff)} under par")
            elif par_diff > 0:
                col3.subheader(f"+{par_diff} over par")
            else:
                col3.subheader("= Even par")
        # Add a line between the two columns
        st.divider()
        tab1, tab2 = st.tabs(["📇Scorecard", "📧Get in Touch"])
        with tab1:
            st.subheader("📇Scorecard:")
            shot_data = []
            for i, hole in enumerate(course.holes):
                category = get_shot_category(golfer.scores[i], hole.par)
                shot_data.append([i+1, hole.par, golfer.scores[i], category])
            shot_columns = ["Hole", "Par", "Score", "Category"]
            st.table(pd.DataFrame(data=shot_data, columns=shot_columns))

            # Display the score chart
            st.plotly_chart(create_score_chart(golfer, course.par, course), use_container_width=True)
        with tab2:
            st.subheader("📧 Get in Touch With Me!")

            url = f"https://formsubmit.co/el/vitesu?next=https://formsubmit.co/el/vitesu"

            # Define the height of the iframe
            height = 750

            # Use the IFrame component to embed the webpage
            components.iframe(url, height=height, width=750)

 
        


    golfer = load_lottiefile("Golfer.json")
    with st.sidebar:
        st_lottie(
        golfer,
        speed=1,
        height=300,
        width=300,
        
        )



if __name__ == "__main__":
    main()
