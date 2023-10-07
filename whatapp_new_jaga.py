import streamlit as st
import pandas as pd
import time



# Set page title and page-wide styling
st.set_page_config(
    page_title="WhatsApp Group Joiner",
    page_icon=":calling:",
    layout="centered"
)

import os, sys



@st.cache_data
def install_chromedriver():
    os.system('sbase install chromedriver')
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

_ = install_chromedriver()

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")




# Custom CSS for styling
st.markdown("""
<style>
body {
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
    padding: 20px;
}
.container {
    max-width: 800px;
    margin: 0 auto;
}
.header {
    text-align: center;
    margin-bottom: 30px;
}
.header h1 {
    color: #075a89;
}
.subheader {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
.instructions {
    margin-bottom: 20px;
}
.instructions p {
    margin: 5px 0;
}
.file-upload {
    margin-top: 20px;
}
.button-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 30px;
}
.download-button {
    background-color: #075a89;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    transition: background-color 0.2s;
}
.download-button:hover {
    background-color: #06486e;
}
.run-again-button {
    background-color: #3caea3;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    transition: background-color 0.2s;
}
.run-again-button:hover {
    background-color: #36a095;
}
.exit-button {
    background-color: #f95d6a;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    text-decoration: none;
    transition: background-color 0.2s;
}
.exit-button:hover {
    background-color: #e95661;
}
.success-message {
    color: green;
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Display system requirements
st.sidebar.title("System Requirements")
st.sidebar.markdown("To run this app, make sure your system meets the following requirements:")
st.sidebar.markdown("- Python 3.x")
st.sidebar.markdown("- Latest version of Chrome installed")
st.sidebar.markdown("- Chrome WebDriver installed and added to your system's PATH")
st.sidebar.markdown("- Required Python packages: Streamlit, pandas, selenium, beautifulsoup4")


st.markdown("<div class='header'><h1>WhatsApp Group Joiner</h1></div>", unsafe_allow_html=True)

st.subheader("Instructions:")
st.markdown("<p class='instructions'>1. Upload a text file in .txt format.</p>", unsafe_allow_html=True)
st.markdown("<p class='instructions'>2. The file should not have blank lines and should contain WhatsApp group links, e.g.,       https://chat.whatsapp.com/xxxxxxxxxxxxx.</p>", unsafe_allow_html=True)
st.markdown("<p class='instructions'>3. The file should not have any other text apart from links.</p>", unsafe_allow_html=True)

# Upload a text file
txt_file = st.file_uploader("Upload a text file", type=["txt"])

if txt_file is not None:
    st.text("Processing... you have 60 seconds to login the WhatApp web  and wait for 60 seconds.")
    st.text("Please do not close the browser window or refresh the page.")
    
    # Start Chrome WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://web.whatsapp.com/')
    
    # Wait for 60 seconds (you can adjust this time if needed)
    time.sleep(60)
    
    # Read the content of the uploaded file as a string
    content = txt_file.read().decode("utf-8")
    group_links = content.split('\n')
    
    # Remove invalid links
    group_links = [link.strip() for link in group_links if link.startswith('https://chat.whatsapp.com/')]
    
    total_groups = len(group_links)
    
    st.text(f"Total number of groups to be added: {total_groups}")
    
    added_groups = []

    for i, group_link in enumerate(group_links, 1):
        st.text(f"Adding group {i}/{total_groups}")
        
        driver.get(group_link)
        
        try:
            join_button = driver.find_element(By.XPATH, '//*[@id="action-button"]')
            join_button.click()
            
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            element = driver.find_element(By.XPATH, '//*[@id="fallback_block"]/div/h4/a')
            link = element.get_attribute("href")
            
            driver.get(link)
            
            time.sleep(5)
            
            try:
                final_join_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]')
                final_join_button.click()
                time.sleep(5)
                added_groups.append(group_link)
            except:
                continue
        except:
            continue
    
    st.success("Groups added successfully.")
    
    # Save added groups to a CSV file
    output_df = pd.DataFrame({'Links': added_groups})
    output_df.to_csv('added_groups.csv', index=False)
    
     # Option to run again or exit
    button_container = st.container()
    with button_container:

        # Provide a download link for the CSV file
        st.subheader("Download Added Groups CSV")
        st.download_button("Download Added Groups CSV", data='added_groups.csv', key='download_button', help="Click to download the CSV file")

        run_again = st.button("Run Again", key='run_again_button')
        st.markdown("<p>or</p>", unsafe_allow_html=True)
        exit_button = st.button("Exit", key='exit_button')
    
    if run_again:
        st.experimental_rerun()
    elif exit_button:
        import webbrowser
        webbrowser.open("https://www.google.com")
        st.balloons()

# Close the WebDriver after processing
if 'driver' in locals():
    driver.quit()



# Display your name in the bottom right corner with a black background
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        right: 0;
        background-color: black;
        color: white;
        padding: 5px 10px;
        font-weight: bold;
    }
    </style>
    <div class="footer">Created By Ramavath Jagadeesh</div>
    """,
    unsafe_allow_html=True
)

