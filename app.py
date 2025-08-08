import streamlit as st
from typing import List, Dict
import json, os
from datetime import datetime

st.set_page_config(page_title="EduLite Enhanced", page_icon="🎓", layout="wide")

# --- Data (courses, with images, videos, resources, and quizzes) ---
COURSES = [
    {
        "id": "py-basics",
        "title": "Python Basics",
        "level": "Beginner",
        "duration": "2 hours",
        "desc": "Learn variables, loops, functions and basic scripting.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
        "video": "https://www.youtube.com/watch?v=rfscVS0vtbw",
        "resources": [{"name": "Python Cheat Sheet", "url": "https://assets.ubuntu.com/v1/7792a6a0-python3-quickref"}],
        "quiz": [
            {"q": "What keyword creates a function in Python?", "options": ["func","def","function","lambda"], "answer": "def"},
            {"q": "How do you write a single-line comment in Python?", "options": ["//","#","<!--","/* */"], "answer": "#"},
            {"q": "Which data type is immutable?", "options": ["list","dict","set","tuple"], "answer": "tuple"}
        ]
    },
    {
        "id": "ml-intro",
        "title": "Intro to Machine Learning",
        "level": "Intermediate",
        "duration": "3 hours",
        "desc": "Overview of supervised learning, models, and evaluation.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/44/Scikit_learn_logo_small.svg",
        "video": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
        "resources": [],
        "quiz": [
            {"q": "Which is a supervised learning task?", "options": ["Clustering","Regression","Dimensionality Reduction","PCA"], "answer": "Regression"},
            {"q": "What metric is used for classification?", "options": ["MSE","Accuracy","RMSE","AIC"], "answer": "Accuracy"}
        ]
    },
    {
        "id": "ds-fundamentals",
        "title": "Data Science Fundamentals",
        "level": "Beginner",
        "duration": "4 hours",
        "desc": "Statistics, EDA and visualization basics.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Statistics.svg",
        "video": "https://www.youtube.com/watch?v=ua-CiDNNj30",
        "resources": [],
        "quiz": [
            {"q": "What is the mean of [1,2,3]?", "options": ["1","2","3","6"], "answer": "2"}
        ]
    },
    {
        "id": "html-css",
        "title": "HTML & CSS Basics",
        "level": "Beginner",
        "duration": "3 hours",
        "desc": "Structure web pages and style them.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg",
        "video": "https://www.youtube.com/watch?v=mU6anWqZJcc",
        "resources": [],
        "quiz": [
            {"q": "Which tag is for a paragraph?", "options": ["<p>","<div>","<span>","<body>"], "answer": "<p>"}
        ]
    },
    {
        "id": "javascript",
        "title": "JavaScript Essentials",
        "level": "Beginner",
        "duration": "3 hours",
        "desc": "Language of the web: DOM, events, basics.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png",
        "video": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
        "resources": [],
        "quiz": [
            {"q": "Which is NOT a JS data type?", "options": ["Number","String","Boolean","Character"], "answer": "Character"}
        ]
    },
    {
        "id": "react",
        "title": "React for Beginners",
        "level": "Intermediate",
        "duration": "5 hours",
        "desc": "Build modern web apps with components and hooks.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
        "video": "https://www.youtube.com/watch?v=w7ejDZ8SWv8",
        "resources": [],
        "quiz": [
            {"q": "React components start with which letter convention?", "options": ["lowercase","UPPERCASE","Capitalized","camelCase"], "answer": "Capitalized"}
        ]
    },
    {
        "id": "sql-basics",
        "title": "SQL Basics",
        "level": "Beginner",
        "duration": "2 hours",
        "desc": "Query relational databases using SQL.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/87/Sql_data_base_with_logo.png",
        "video": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "resources": [],
        "quiz": [
            {"q": "Which SQL statement retrieves rows?", "options": ["GET","SELECT","FETCH","OPEN"], "answer": "SELECT"}
        ]
    },
    {
        "id": "git-github",
        "title": "Git & GitHub",
        "level": "Beginner",
        "duration": "2 hours",
        "desc": "Version control and collaboration basics.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg",
        "video": "https://www.youtube.com/watch?v=RGOj5yH7evk",
        "resources": [],
        "quiz": [
            {"q": "What command creates a new branch locally?", "options": ["git branch name","git new name","git create name","git checkout -b name"], "answer": "git checkout -b name"}
        ]
    },
    {
        "id": "ai-overview",
        "title": "AI Overview",
        "level": "Beginner",
        "duration": "1.5 hours",
        "desc": "Intro to concepts and real-world use-cases.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/17/Artificial_Intelligence_logo.svg",
        "video": "https://www.youtube.com/watch?v=2ePf9rue1Ao",
        "resources": [],
        "quiz": [
            {"q": "AI stands for?", "options": ["Automatic Intelligence","Artificial Intelligence","Actual Intelligence","Augmented Interface"], "answer": "Artificial Intelligence"}
        ]
    },
    {
        "id": "pandas",
        "title": "Data Analysis with Pandas",
        "level": "Intermediate",
        "duration": "4 hours",
        "desc": "Work with tabular data using Pandas.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg",
        "video": "https://www.youtube.com/watch?v=vmEHCJofslg",
        "resources": [],
        "quiz": [
            {"q": "Which object is core to pandas?", "options": ["DataFrame","Matrix","Array","Table"], "answer": "DataFrame"}
        ]
    }
]

PROGRESS_FILE = "progress_store.json"

# Utility functions for local persistence (writes to working directory)
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_course" not in st.session_state:
    st.session_state.selected_course = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

# Sidebar - navigation and search
with st.sidebar:
    st.title("EduLite")
    st.markdown("Free learning demo — interactive")
    page = st.radio("Navigate", ["Home", "Courses", "My Progress", "Contact"])
    st.session_state.page = page.lower().replace(" ", "-")
    st.markdown("---")
    st.write("Search courses")
    q = st.text_input("Search")
    if q:
        st.session_state.search = q
    else:
        st.session_state.search = ""

# Page components
def render_course_card(course):
    cols = st.columns([1,3,1])
    with cols[0]:
        try:
            st.image(course.get("image"), width=90)
        except Exception:
            st.write("")
    with cols[1]:
        st.subheader(course["title"])
        st.write(course["desc"])
        st.caption(f"Level: {course['level']} • Duration: {course['duration']}")
        btn_col1, btn_col2, btn_col3 = st.columns([1,1,1])
        with btn_col1:
            if st.button("Open Lesson", key=f"open-{course['id']}"):
                st.session_state.selected_course = course["id"]
                st.session_state.page = "courses"
        with btn_col2:
            if st.button("Preview Video", key=f"vid-{course['id']}"):
                st.session_state.preview = course["video"]
        with btn_col3:
            if st.button("Start Quiz", key=f"start-{course['id']}"):
                st.session_state.page = f"quiz-{course['id']}"

def page_home():
    st.header("Welcome to EduLite — Enhanced 🎓")
    st.write("Interactive courses, quizzes and progress saving (local).")
    st.markdown("### Featured courses")
    cols = st.columns(3)
    for i, course in enumerate(COURSES[:3]):
        with cols[i]:
            st.image(course.get("image"), width=120)
            st.subheader(course["title"])
            st.write(course["desc"])
            if st.button("Open", key=f"feat-{course['id']}"):
                st.session_state.selected_course = course["id"]
                st.session_state.page = "courses"

def page_courses():
    st.header("All Courses")
    search = st.session_state.get("search", "").strip().lower()
    filtered = [c for c in COURSES if search in c["title"].lower() or search in c["desc"].lower()]
    if not filtered:
        st.info("No courses match your search.")
    for course in filtered:
        with st.expander(course["title"]):
            render_course_card(course)

    # preview video if set
    if st.session_state.get("preview"):
        st.markdown("---")
        st.subheader("Video Preview")
        st.video(st.session_state.preview)

    # selected course detailed view
    if st.session_state.selected_course:
        course = next((c for c in COURSES if c["id"] == st.session_state.selected_course), None)
        if course:
            st.markdown("---")
            st.image(course.get("image"), width=220)
            st.header(course["title"])
            st.write(course["desc"])
            st.video(course["video"])
            if course["resources"]:
                st.markdown("**Resources**")
                for r in course["resources"]:
                    st.write(f"- [{r['name']}]({r['url']})")
            if course["quiz"]:
                if st.button("Take Quiz", key=f"take-{course['id']}"):
                    st.session_state.page = f"quiz-{course['id']}"

def page_progress():
    st.header("My Progress")
    progress = st.session_state.progress or {}
    if not progress:
        st.info("No progress yet. Complete quizzes to record progress.")
    else:
        for cid, info in progress.items():
            course = next((c for c in COURSES if c["id"]==cid), None)
            if course:
                st.write(f"**{course['title']}** — Score: {info.get('score')}% • Completed: {info.get('completed')} • On: {info.get('timestamp')}")

    if st.button("Save Progress to disk"):
        save_progress(st.session_state.progress or {})
        st.success("Progress saved locally to progress_store.json")

def page_contact():
    st.header("Contact / Feedback")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Send"):
        st.success("Thanks — message recorded locally (not emailed).")

def page_quiz(course_id: str):
    course = next((c for c in COURSES if c["id"]==course_id), None)
    if not course:
        st.error("Course not found.")
        return
    st.header(f"Quiz — {course['title']}")
    questions = course.get("quiz", [])
    if not questions:
        st.info("No quiz available for this course.")
        return

    # prepare answers
    if course_id not in st.session_state.quiz_answers:
        st.session_state.quiz_answers[course_id] = [None]*len(questions)

    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}. {q['q']}**")
        choice = st.radio("", q["options"], key=f"{course_id}-q-{i}")
        st.session_state.quiz_answers[course_id][i] = choice

    if st.button("Submit Quiz"):
        user_answers = st.session_state.quiz_answers[course_id]
        correct = 0
        for ua, q in zip(user_answers, questions):
            if ua == q["answer"]:
                correct += 1
        score = int((correct/len(questions))*100)
        st.success(f"You scored {score}% — {correct}/{len(questions)} correct.")
        # update progress in session state
        st.session_state.progress[course_id] = {"score": score, "completed": True, "timestamp": datetime.utcnow().isoformat()}
        # auto-save
        save_progress(st.session_state.progress)

# Router
page = st.session_state.page
if page == "home" or page.startswith("home"):
    page_home()
elif page == "courses" or page.startswith("courses"):
    page_courses()
elif page.startswith("quiz-"):
    cid = page.split("quiz-")[-1]
    page_quiz(cid)
elif page == "my-progress" or page.startswith("my-progress"):
    page_progress()
elif page == "contact":
    page_contact()
else:
    page_home()

st.markdown('---')
st.caption("EduLite Built with Pratik☺️")