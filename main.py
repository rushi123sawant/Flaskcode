import streamlit as st
import urllib.parse
import http.client
import json
 
# ANALYZE IMAGE
st.set_page_config(
    page_title="Image Analysis App",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;background-color: #778899;color: white;border-radius: 20px; width: 100%;margin: 0 auto;'>Image Analysis (Azure cognitive service)</h1>",unsafe_allow_html=True)
st.markdown("-----")


def analyze_image(image_url):
    subscription_key = '0e1b79e513bc4626b47552f29a3c66b6'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
 
    body = {
        'url': image_url
    }
 
    params = urllib.parse.urlencode({
        'visualFeatures': 'description',
    })
 
    try:
        conn = http.client.HTTPSConnection("southcentralus.api.cognitive.microsoft.com")
        conn.request("POST", "/vision/v2.0/analyze?%s" % params, str(body), headers)
        response = conn.getresponse()
        jsonData = response.read()
        data = json.loads(jsonData)
 
        # Extract relevant information
        description = data['description']['captions'][0]['text']
        tags = data['description']['tags']
 
        conn.close()
 
        return description, tags
 
    except Exception as ex:
        return str(ex)
 
# Initialize the Streamlit app

 
# st.title("Image Analysis (Azure cognitive service)")
 
# Bot icon URL
bot_icon_url = "https://i.ibb.co/YQp70fp/chatbot-new.png"
 
# Get or initialize the image history list in session_state
if "image_history" not in st.session_state:
    st.session_state.image_history = []
 
# Directly input an image URL for analysis
image_url = st.text_input("Enter an image URL:")
 
if st.button("Analyze Image"):
    if image_url:
        # Analyze the image
        description, tags = analyze_image(image_url)
 
        # Add image data to the history list
        st.session_state.image_history.append({
            "image_url": image_url,
            "description": description,
            "tags": tags
        })
 
# Display the image history
for entry in st.session_state.image_history:
    # Display uploaded image
    st.image(entry["image_url"], caption='Uploaded Image', use_column_width=True)
 
    # Display description and tags in a grey container with black text and bot icon
    # st.markdown(
    #     f'<img src="{bot_icon_url}" width="40" height="40" style="border-radius: 50%; margin-right: 10px;">'
    #     f'<div style="background-color: #C6CCD0; padding: 10px; border-radius: 10px;">'
    #     f'<span style="color: black;">'
    #     f'Description: {entry["description"]}<br>'
    #     f'Tags: {", ".join(entry["tags"])}'
    #     f'</span>'
    #     f'</div>',
    #     unsafe_allow_html=True
    # )
    st.markdown(
        f'<div style="display: flex; align-items: center;">'
        f'<img src="{bot_icon_url}" width="40" height="40" style="border-radius: 50%; margin-right: 10px;">'
        f'<div style="background-color: #C6CCD0;background: linear-gradient(90deg, rgba(158,163,166,1) 0%, rgba(216,222,227,1) 100%); padding: 10px; border-radius: 10px; color: black;">'
        f'<span>'
        f'Description: {entry["description"]}<br>'
        f'Tags: {", ".join(entry["tags"])}'
        f'</span>'
        f'</div>'
        f'</div>',
    unsafe_allow_html=True
    )
    st.write("---")  # Separator