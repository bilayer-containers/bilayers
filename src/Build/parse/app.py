
import gradio
import skimage
import scipy
import numpy
import os
# Import the function from the script
from Algorithms.threshold.threshold import example_function

# Inputs to be shown in the GUI
inputs = [
    gradio.Files(file_count='multiple', label='Drag and drop all images to be analyzed'),
    gradio.Radio(['Otsu', 'Li'], type='value', value='Otsu', label='Select a Threshold Method'),
    gradio.Number(value=5, interactive=True, label='Object Minimum Diameter Size'),
    gradio.Number(value=20, interactive=True, label='Object Maximum Diameter Size')
]

# Output to be shown in the GUI
output = [
    gradio.File(label='Download Output')
]

demo = gradio.Interface(
    fn=example_function, 
    inputs=inputs, 
    outputs=output,
    title="Simple ID objects"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
