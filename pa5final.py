import streamlit as st
import openai
import json
import pandas as pd

user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as an Spanish-translator. You will receive a 
            a sentence in English and you should extract all the words in sentence and give an extracted word, translated word from English to Spanish , part of speech and an example sentence of the extracted word in Spanish and do not duplicate sentences with other words.
            List the extracted words in a JSON array, one extracted word per line.
            Each extracted word should have 4 fields:
            - "word" - all the words that were extracted
            - "translation" - the translated word from English to Spanish
            - "part of speech" - the part of speech of the extracted word
            - "example usage" - an example sentence of the extracted word in Spanish and do not duplicate sentences with other words
            
            Don't say anything at first. Wait for the user to say something.
        """    
st.title('Make it Spanish')
st.markdown('Input a sentence in English that you want to change to Spanish. \n\
            The AI will give you some Spanish words.')

user_input = st.text_area("Enter some text to correct:", "Your text here")

if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_so_far
        )
        # Show the response from the AI in a box
        st.markdown('**AI response:**')
        suggestion_dictionary = response.choices[0].message.content
        sd = json.loads(suggestion_dictionary)
        suggestion_df = pd.DataFrame.from_dict(sd)
        st.table(suggestion_df)
    except Exception as e:
        st.error(f"An error occurred: {e}")

