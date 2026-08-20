import streamlit as st

st.header("Model Structure")

st.mermaid_chart("""graph TD
                A[Raw Market and Financial Data] -->|Data Cleaning and Preprocessing| B[Preprocessed Data]
                
                subgraph Preprocessing and Feature Engineering
                B -->|Feature Engineering| C[Model Training]
                B --> D[Fundamental Calculations]
                end
                
                subgraph -
                D -->|Fundamental Ratios| E{Language Model}
                C -->|Best Performing Model| E
                
                D --> G[Streamlit Webapp]
                E -->|Thesis Output| G
                C -->|Classification Report and Results| G
                
                end
                
                
                """,width  ="stretch")
st.page_link("Confidence_Scope.py", label = "**Confidence Scope**", icon ="🔍", icon_position="right")

