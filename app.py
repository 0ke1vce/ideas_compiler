import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import json

# Import your custom compiler modules
from error_handler import ErrorHandler
from symbol_table import SymbolTable
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ir_gen import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator

# Import the Database Manager we just built!
import db_manager 
import os
import setup_db

# Cloud deployment fix: Auto-build the database if it's missing!
if not os.path.exists("ideas_saas.db"):
    setup_db.initialize_database()

st.set_page_config(page_title="IDEAS Project Manager", layout="wide")

# --- INITIALIZE SESSION STATE ---
# This acts as our app's short-term memory to track logins
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ""
if 'loaded_code' not in st.session_state:
    st.session_state.loaded_code = "TASK Database DURATION 5 ASSIGNED Ujjwal\nTASK API DURATION 4 REQUIRES Database ASSIGNED Mayank\nTASK Frontend DURATION 3 ASSIGNED Ujjwal"
if 'loaded_name' not in st.session_state:
    st.session_state.loaded_name = "My First Project"

def run_ideas_compiler(source_code):
    """Runs the compiler and returns the JSON file path."""
    error_handler = ErrorHandler()
    symbol_table = SymbolTable()
    
    tokens = Lexer(error_handler).tokenize(source_code)
    if error_handler.has_error: return False, "Syntax/Spelling Error! Check your code."
    
    Parser(tokens, symbol_table, error_handler).parse()
    if error_handler.has_error: return False, "Grammar Error! Check your code."
        
    if not SemanticAnalyzer(symbol_table, error_handler).analyze() or error_handler.has_error: 
        return False, "Logic Error! You might have an infinite loop or a missing task."
    
    graph = IRGenerator(symbol_table).generate()
    optimizer = Optimizer(graph)
    schedule = optimizer.optimize()
    
    codegen = CodeGenerator(schedule, optimizer.total_duration)
    output_file = "ui_schedule.json"
    codegen.generate_json(output_file)
    
    return True, output_file

# --- THE LOGIN GATEWAY ---
def login_page():
    st.title("🔐 Welcome to IDEAS")
    st.markdown("Log in or create an account to manage your project timelines.")
    
    # Create clean tabs for the UI
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        log_user = st.text_input("Username", key="log_user")
        log_pass = st.text_input("Password", type="password", key="log_pass")
        if st.button("Login", type="primary"):
            success, user_id = db_manager.verify_user(log_user, log_pass)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = log_user
                st.rerun() # Refresh the page to show the dashboard!
            else:
                st.error("Invalid username or password.")
                
    with tab2:
        st.subheader("Create Account")
        new_user = st.text_input("New Username", key="new_user")
        new_pass = st.text_input("New Password", type="password", key="new_pass")
        if st.button("Sign Up"):
            if new_user and new_pass:
                success, msg = db_manager.create_user(new_user, new_pass)
                if success:
                    st.success(f"{msg} You can now log in using the Login tab.")
                else:
                    st.error(msg)
            else:
                st.warning("Please fill out both fields.")

# --- THE MAIN SAAS DASHBOARD ---
def main_dashboard():
    # 1. The Sidebar Navigation
    with st.sidebar:
        st.write(f"👤 Logged in as: **{st.session_state.username}**")
        if st.button("Logout"):
            # Clear the memory if they log out
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = ""
            st.rerun()
            
        st.divider()
        st.subheader("📂 Your Saved Projects")
        
        # Fetch their history from SQLite!
        projects = db_manager.get_user_projects(st.session_state.user_id)
        
        if not projects:
            st.info("No saved projects yet.")
        else:
            # Create a button for every past project they have
            for p in projects:
                if st.button(f"📄 {p['name']}", key=f"btn_{p['name']}"):
                    st.session_state.loaded_code = p['script']
                    st.session_state.loaded_name = p['name']
                    st.rerun()

    # 2. The Compiler UI
    st.title("🚀 IDEAS Project Manager")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Code Editor")
        # Added a text box to name the project before saving it
        project_name = st.text_input("Project Name:", value=st.session_state.loaded_name)
        user_code = st.text_area("Enter your IDEAS script:", value=st.session_state.loaded_code, height=300)
        
        # Updated button text to reflect the new database functionality
        compile_btn = st.button("Compile & Save to Database", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 Interactive Gantt Chart")
        
        if compile_btn:
            if not project_name.strip():
                st.error("Please provide a project name so we can save it.")
            else:
                with st.spinner("Compiling script & saving to cloud..."):
                    success, result = run_ideas_compiler(user_code)
                    
                    if success:
                        # THE MAGIC HAPPENS HERE: Save to SQLite
                        db_manager.save_project(st.session_state.user_id, project_name, user_code, result)
                        
                        st.success("Compilation Successful! Project Saved.")
                        
                        with open(result, 'r') as f:
                            data = json.load(f)
                        
                        st.metric(label="Total Project Duration", value=f"{data['total_project_days']} Days")
                        
                        # --- RENDER CHART ---
                        base_date = datetime.date.today()
                        chart_data = []
                        
                        for task in data["tasks"]:
                            start_date = base_date + datetime.timedelta(days=task["start_day"] - 1)
                            end_date = base_date + datetime.timedelta(days=task["end_day"])
                            
                            status = "Critical (Bottleneck)" if task["is_critical"] else f"Flexible ({task['slack_days']} Days Slack)"
                            
                            chart_data.append({
                                "Task": task["task_name"],
                                "Start": start_date,
                                "Finish": end_date,
                                "Duration": f"{task['duration']} Days",
                                "Assigned": task["assigned"],
                                "Status": status
                            })
                        
                        df = pd.DataFrame(chart_data)
                        color_map = {"Critical (Bottleneck)": "#ef4444"}
                        
                        fig = px.timeline(
                            df, x_start="Start", x_end="Finish", y="Task", 
                            color="Status", 
                            color_discrete_map=color_map,
                            hover_data=["Duration", "Assigned"]
                        )
                        fig.update_yaxes(autorange="reversed") 
                        fig.layout.xaxis.type = 'date'
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"❌ Compilation Failed: {result}")

# --- APP ROUTING ---
# This decides which page to show the user!
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()