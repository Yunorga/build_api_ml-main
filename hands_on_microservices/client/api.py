# Create a canvas component
# canvas_result = st_canvas(
#     b_width, b_color, bg_color,width=50, height=50, drawing_mode=drawing_mode, key="canvas"
# )

# st.sidebar.header("Configuration")

# canvas_result = st_canvas(
#             fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
#             stroke_width=1,
#             stroke_color="rgba(0, 0, 0, 1)",
#             background_color=bg_color,
#             update_streamlit=True,
#             height=150,
#             drawing_mode=drawing_mode,
#             point_display_radius=1 if drawing_mode == "point" else 0,
#             display_toolbar=st.sidebar.checkbox("Display toolbar", True),
#             key="full_app",
#         )

# # Do something interesting with the image data
# if canvas_result.image_data is not None:
#     st.image(canvas_result.image_data)

# if st.button("Submit"): # send image to server 
#     img = canvas_result.image_data
#     response = requests.put(API_IMG_UPLOAD_URL, data=img)
#     st.write(response)

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import requests
from io import BytesIO
from PIL import Image

# from streamlit_extras.switch_page_button import switch_page

API_IMG_URL = "http://serveur:8000/img"
API_IMG_UPLOAD_URL = "http://serveur:8000/img_upload"

st.set_page_config(page_title="Application PostgreSQL", layout="centered")

st.title("Bienvenue sur l'Application")

if st.button("Utilisateur"):
    st.switch_page("pages/utilisateur.py")

if st.button("Admin"):
    st.switch_page("pages/admin.py")

if st.button("Image"):
    response = requests.put(API_IMG_URL)
    image = Image.open(BytesIO(response.content))
    st.image(image)

    # st.switch_page("pages/admin.py")


# Specify brush parameters and drawing mode
b_width = st.slider("Brush width: ", 1, 100, 10)
b_color = "#53b646" #st.beta_color_picker("Enter brush color hex: ")
bg_color = "#cccccc" #st.beta_color_picker("Enter background color hex: ", "#eee")
drawing_mode = True #st.checkbox("Drawing mode ?", True)


# Specify canvas parameters in application
stroke_width = st.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.color_picker("Stroke color hex: ")
bg_color = st.color_picker("Background color hex: ", "#FFFFFF")

width = 100 # st.slider("Canvas width: ", 100, 1000, 400)
height = 100 # st.slider("Canvas height: ", 100, 1000, 400)
bg_image_pil = None

drawing_mode = st.selectbox(
    "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform", "polygon")
)

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=bg_image_pil,
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode=drawing_mode,
    key="canvas",
)

if st.button("Submit"): # send image to server 
    # Convert NumPy array to PIL Image
    img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')

    # Convert PIL Image to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")  # Or JPEG, etc.
    img_bytes = img_bytes.getvalue()

    # Send image data via POST request
    response = requests.post(API_IMG_UPLOAD_URL, files={"file": ("image.png", img_bytes, "image/png")})





    # response = requests.put(API_IMG_UPLOAD_URL, data=img)
    # st.write(response)




# # Do something interesting with the image data and paths
# if canvas_result.image_data is not None:
#     st.write("## Drawn Image")
#     img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
#     st.image(img)

# if canvas_result.json_data is not None:
#     st.write("## Canvas Data")
#     st.json(canvas_result.json_data)

    # img = canvas_result.image_data
    # save image to BytesIO object
    # img = BytesIO()
    # img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
    # img = img.save(img, format='PNG')
    # img = img.getvalue()

    
    # response = requests.put(API_IMG_UPLOAD_URL, data=img)
    # response = requests.put(API_IMG_UPLOAD_URL, data=img
    # send image to server over http put request
    # img_byte_arr = BytesIO()
    # img.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()
    
    # img_byte_arr = BytesIO()
    





# import streamlit as st
# import numpy as np
# from PIL import Image
# from streamlit_drawable_canvas import st_canvas

# def main():
#     st.title("Drawable Canvas")

#     # Specify canvas parameters in application
#     stroke_width = st.slider("Stroke width: ", 1, 25, 3)
#     stroke_color = st.color_picker("Stroke color hex: ")
#     bg_color = st.color_picker("Background color hex: ", "#FFFFFF")
#     bg_image = st.file_uploader("Background image:", type=["png", "jpg"])

#     if bg_image:
#         bg_image_pil = Image.open(bg_image)
#         width, height = bg_image_pil.size
#     else:
#         width = st.slider("Canvas width: ", 100, 1000, 400)
#         height = st.slider("Canvas height: ", 100, 1000, 400)
#         bg_image_pil = None

#     drawing_mode = st.selectbox(
#         "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform", "polygon")
#     )

#     # Create a canvas component
#     canvas_result = st_canvas(
#         fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
#         stroke_width=stroke_width,
#         stroke_color=stroke_color,
#         background_color=bg_color,
#         background_image=bg_image_pil,
#         update_streamlit=True,
#         height=height,
#         width=width,
#         drawing_mode=drawing_mode,
#         key="canvas",
#     )

#     # Do something interesting with the image data and paths
#     if canvas_result.image_data is not None:
#         st.write("## Drawn Image")
#         img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
#         st.image(img)

#     if canvas_result.json_data is not None:
#         st.write("## Canvas Data")
#         st.json(canvas_result.json_data)

# if __name__ == "__main__":
#     main()