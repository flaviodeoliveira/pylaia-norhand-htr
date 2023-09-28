import gradio as gr
import subprocess
from PIL import Image
import tempfile
import os
import yaml
import base64
import evaluate

def resize_image(image, base_height):

    if image.size[1] == base_height:
        return image

    # Calculate aspect ratio
    w_percent = base_height / float(image.size[1])
    w_size = int(float(image.size[0]) * float(w_percent))

    # Resize the image
    return image.resize((w_size, base_height), Image.Resampling.LANCZOS)

# Get images and respective transcriptions from the examples directory
def get_example_data(folder_path="./examples/"):
    
    example_data = []
    
    # Get list of all files in the folder
    all_files = os.listdir(folder_path)
    
    # Loop through the file list
    for file_name in all_files:
        
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is an image (.png)
        if file_name.endswith(".jpg"):
            
            # Construct the corresponding .txt filename (same name)
            corresponding_text_file_name = file_name.replace(".jpg", ".txt")
            corresponding_text_file_path = os.path.join(folder_path, corresponding_text_file_name)
            
            # Initialize to a default value
            transcription = "Transcription not found."
            
            # Try to read the content from the .txt file
            try:
                with open(corresponding_text_file_path, "r") as f:
                    transcription = f.read().strip()
            except FileNotFoundError:
                pass  # If the corresponding .txt file is not found, leave the default value
            
            example_data.append([file_path, transcription])
            
    return example_data

def predict(input_image: Image.Image, ground_truth):

    cer = None

    try:

        # Try to resize the image to a fixed height of 128 pixels
        try:
            input_image = resize_image(input_image, 128)
        except Exception as e:
            print(f"Image resizing failed: {e}")
            return f"Image resizing failed: {e}"

        # Used as a context manager. Takes care of cleaning up the directory.
        # Even if an error is raised within the with block, the directory is removed.
        # No finally block needed
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_image_path = os.path.join(temp_dir, 'temp_image.jpg')
            temp_list_path = os.path.join(temp_dir, 'temp_img_list.txt')
            temp_config_path = os.path.join(temp_dir, 'temp_config.yaml')

            input_image.save(temp_image_path)

            # Create a temporary img_list file
            with open(temp_list_path, 'w') as f:
                f.write(temp_image_path)

            # Read the original config file and create a temporary one
            with open('my_decode_config.yaml', 'r') as f:
                config_data = yaml.safe_load(f)
            
            config_data['img_list'] = temp_list_path

            with open(temp_config_path, 'w') as f:
                yaml.dump(config_data, f)

            try:
                subprocess.run(f"pylaia-htr-decode-ctc --config {temp_config_path} | tee predict.txt", shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Command failed with error {e.returncode}, output:\n{e.output}")

            # # Write the output to predict.txt
            # with open('predict.txt', 'wb') as f:
            #     f.write(output)

            # Read the output from predict.txt
            if os.path.exists('predict.txt'):
                with open('predict.txt', 'r') as f:
                    output_line = f.read().strip().split('\n')[-1]   # Last line
                    _, prediction = output_line.split(' ', 1)  # split only at the first space
            else:
                print('predict.txt does not exist')

            if ground_truth is not None and ground_truth.strip() != "":

                # Debug: Print lengths before computing metric
                print("Number of predictions:", len(prediction))
                print("Number of references:", len(ground_truth))

                # Check if lengths match
                if len(prediction) != len(ground_truth):

                    print("Mismatch in number of predictions and references.")
                    print("Predictions:", prediction)
                    print("References:", ground_truth)
                    print("\n")

                cer = cer_metric.compute(predictions=[prediction], references=[ground_truth])
                # cer = f"{cer:.3f}"

            else:

                cer = "Ground truth not provided"

        return prediction, cer

    except subprocess.CalledProcessError as e:
        return f"Command failed with error {e.returncode}"

# Encode images
with open("assets/header.png", "rb") as img_file:
    logo_html = base64.b64encode(img_file.read()).decode('utf-8')

with open("assets/teklia_logo.png", "rb") as img_file:
    footer_html = base64.b64encode(img_file.read()).decode('utf-8')

title = """
    <h1 style='text-align: center'> Hugging Face x Teklia: PyLaia HTR demo</p>
"""

description = """
    [PyLaia](https://github.com/jpuigcerver/PyLaia) is a device agnostic, PyTorch-based, deep learning toolkit \
    for handwritten document analysis.
    This model was trained using PyLaia library on Norwegian historical documents ([NorHand Dataset](https://zenodo.org/record/6542056)) \
    during the [HUGIN-MUNIN project](https://hugin-munin-project.github.io) for handwritten text recognition (HTR).
    * HF `model card`: [Teklia/pylaia-huginmunin](https://huggingface.co/Teklia/pylaia-huginmunin) | \
    [A Comprehensive Comparison of Open-Source Libraries for Handwritten Text Recognition in Norwegian](https://doi.org/10.1007/978-3-031-06555-2_27)
"""

examples = get_example_data()

# pip install evaluate
# pip install jiwer
cer_metric = evaluate.load("cer")

with gr.Blocks(
    theme=gr.themes.Soft(),
    title="PyLaia HTR",
) as demo:

    gr.HTML(
        f"""
        <div style='display: flex; justify-content: center; width: 100%;'>
            <img src='data:image/png;base64,{logo_html}' class='img-fluid' width='350px'>
        </div>
        """
    )

    #174x60

    title = gr.HTML(title)
    description = gr.Markdown(description)

    with gr.Row():

        with gr.Column(variant="panel"):

            input = gr.components.Image(type="pil", label="Input image:")

            with gr.Row():

                btn_clear = gr.Button(value="Clear")
                button = gr.Button(value="Submit")

        with gr.Column(variant="panel"):

            output = gr.components.Textbox(label="Generated text:")
            ground_truth = gr.components.Textbox(value="", placeholder="Provide the ground truth, if available.", label="Ground truth:")
            cer_output = gr.components.Textbox(label="CER:")

    with gr.Row():

        with gr.Accordion(label="Choose an example from test set:", open=False):
            
            gr.Examples(
                examples=examples,
                inputs = [input, ground_truth],
                label=None,
            )

    with gr.Row():

        gr.HTML(
            f"""
            <div style="display: flex; align-items: center; justify-content: center">
                <a href="https://teklia.com/" target="_blank">
                    <img src="data:image/png;base64,{footer_html}" style="width: 100px; height: 80px; object-fit: contain; margin-right: 5px; margin-bottom: 5px">
                </a>
                <p style="font-size: 13px">
                    |    <a href="https://huggingface.co/Teklia">Teklia models on Hugging Face</a>
                </p>
            </div>
            """
        )

    button.click(predict, inputs=[input, ground_truth], outputs=[output, cer_output])
    btn_clear.click(lambda: [None, "", "", ""], outputs=[input, output, ground_truth, cer_output])

    # # Try to force light mode
    # js = """
    #     function () {
    #         gradioURL = window.location.href
    #         if (!gradioURL.endsWith('?__theme=light')) {
    #             window.location.replace(gradioURL + '?__theme=light');
    #     }
    # }"""

    # demo.load(_js=js)

if __name__ == "__main__":

    demo.launch(favicon_path="teklia_icon_grey.png")
