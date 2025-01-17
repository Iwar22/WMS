import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import base64
import io
import os

# ---- ASSETS
# Function to construct relative paths
def get_relative_path(file_name):
    return os.path.join('logos', "Logo's", file_name)

# Construct paths to the images
bayards_logo_path = get_relative_path("bayards logo.png")
aluminium_logo_path = get_relative_path("bayards aluminium solutions logo.png")
helideck_logo_path = get_relative_path("helideck.png")
yacht_logo_path = get_relative_path("yacht.png")
up_logo_path = get_relative_path("up.jpg")

# Function to load images with error handling
def load_image(path):
    try:
        return Image.open(path)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return None
    except IOError:
        st.error(f"Error opening file: {path}")
        return None

bayards_logo = load_image(bayards_logo_path)
aluminium_logo = load_image(aluminium_logo_path)
helideck_logo = load_image(helideck_logo_path)
yacht_logo = load_image(yacht_logo_path)
up_logo = load_image(up_logo_path)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        st.error(f"Error loading animation: {url}")
        return None
    return r.json()

warehouse_animation = load_lottieurl("https://lottie.host/924cb93d-aad7-483a-9bbf-ab3dec5fffb7/hTqo40JjAI.json")

#--- config
st.set_page_config(page_title="Bayards WMS", page_icon=":tada:", layout="wide")

# Resize images to the desired height while maintaining aspect ratio
def resize_image(image, height):
    aspect_ratio = image.width / image.height
    new_width = int(height * aspect_ratio)
    return image.resize((new_width, height))

logo_height = 175  # Adjust the height as needed
logo_width = 350  # Adjust the width as needed

if aluminium_logo:
    aluminium_logo = resize_image(aluminium_logo, logo_height)
if helideck_logo:
    helideck_logo = resize_image(helideck_logo, logo_height)
if yacht_logo:
    yacht_logo = resize_image(yacht_logo, logo_height)
if up_logo:
    up_logo = resize_image(up_logo, logo_height)

# Encode image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

aluminium_logo_base64 = image_to_base64(aluminium_logo) if aluminium_logo else None
helideck_logo_base64 = image_to_base64(helideck_logo) if helideck_logo else None
yacht_logo_base64 = image_to_base64(yacht_logo) if yacht_logo else None
up_logo_base64 = image_to_base64(up_logo) if up_logo else None

# URLs for the login pages of the respective business units
aluminium_login_url = "http://aluminium-login-page.com"
helideck_login_url = "http://helideck-login-page.com"
yacht_login_url = "http://yacht-login-page.com"
up_login_url = "http://up-login-page.com"

# Define CSS for hover effect
hover_css = """
<style>
    .hover-effect {
        transition: transform 0.4s, opacity 0.3s;
    }
    .hover-effect:hover {
        opacity: 0.7;
        transform: scale(1.35);
    }
</style>
"""
st.markdown(hover_css, unsafe_allow_html=True)

# Define a function to create clickable images with margin
def clickable_image_with_margin(image_base64, width, margin, url):
    if image_base64:
        return f'<a href="{url}" target="_blank"><img src="data:image/png;base64,{image_base64}" width="{width}" style="margin-left: {margin}px;" class="hover-effect"></a>'
    return ""

#-- LANDING PAGE --------------
with st.container():
    if bayards_logo:
        st.image(bayards_logo, width=450)  # Adjust use_column_width for responsive sizing
    st.title("Warehouse management system")
    st.markdown("<br><br>", unsafe_allow_html=True)  # Add space beneath the title

    # Layout with logos on the left and animation on the right
    left_column, right_column = st.columns([1, 2])  # Adjust the ratio as needed

    with left_column:
        st.markdown(clickable_image_with_margin(aluminium_logo_base64, logo_width, 20, aluminium_login_url), unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add space between images
        st.markdown(clickable_image_with_margin(helideck_logo_base64, logo_width, 20, helideck_login_url), unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)  # Add space between images
        st.markdown(clickable_image_with_margin(yacht_logo_base64, logo_width, 20, yacht_login_url), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)  # Add space between images
        st.markdown(clickable_image_with_margin(up_logo_base64, logo_width, 20, up_login_url), unsafe_allow_html=True)

    with right_column:
        if warehouse_animation:
            st_lottie(warehouse_animation, height=450, key="coding")
