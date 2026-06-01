import streamlit as st
import requests

st.title("Web scraper")

url=st.text_input("Enter URL to scrape")

if st.button("Scrape"):
    response=requests.post(
        "http://localhost:8000/api/scrape",
        json={"url":url}
    )
    data=response.json()
    st.write(data)

if st.button("Get"):
    response=requests.get("http://localhost:8000/api/")
    data=response.json()
    st.write(data) 