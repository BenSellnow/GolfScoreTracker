# Golf Score Tracking web application using Streamlit

This is a web application for tracking golf scores. The application allows you to enter your scores hole-by-hole and displays your overall score as well as your score relative to par. It also provides a chart of your scores and par per hole.

## Getting Started

### Prerequisites

To run this application, you need to have Python installed on your machine.

### Installing

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the application, run the following command:

```bash
streamlit run <filename.py>
```


## Usage

### Load a Golf Course

First, you need to load a golf course. You can do this by uploading a `.txt` file containing the course information. The file should have the following information:

| Format | Description                   |
|--------|-------------------------------|
| C      | Course Information             |
|        | Course Name                   |
|        | Par                           |
|        | Hole Count                    |
| H      | Hole Information               |
|        | Hole Number                   |
|        | Hole Name                     |
|        | Par                           |

In this format:
```txt
C, Course Name, Par, Hole Count
H, Hole Number, Hole Name, Par
```


### Enter Golfer Information and Scores

After loading a golf course, you can enter the golfer's information and scores. The application will prompt you to enter the golfer's name and then display a form for entering the scores for each hole. The application will calculate the total score and display it, as well as the score relative to par.

### View Score Chart

After entering the scores, the application will display a chart of the golfer's scores and the par per hole.

## Built With

- Streamlit
- Pandas
- Plotly
- Streamlit Lottie
- JSON

## Acknowledgements

The Streamlit Lottie library was used to display the animation of a golf ball being hit in the app's sidebar.

Contact form provided by [FormSubmit](https://formsubmit.co/

