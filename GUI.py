import gradio as gr
import configparser
import subprocess
import os
import sys

# Function to read the existing config.ini
def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

# Function to save the config
def save_config(config):
    with open("config.ini", "w") as config_file:
        config.write(config_file)

# Function to start Easy-Wav2Lip with user inputs
def start_easy_wav2lip(video_file, vocal_file, quality, output_height, wav2lip_version, output_suffix,
                       include_settings, batch_process, preview_window, nosmooth,
                       use_previous_tracking_data, preview_settings, frame_to_preview):
    # Read existing config
    config = read_config()
    
    # Update config values
    config["OPTIONS"]["video_file"] = str(video_file)
    config["OPTIONS"]["vocal_file"] = str(vocal_file)
    config["OPTIONS"]["quality"] = str(quality)
    config["OPTIONS"]["output_height"] = str(output_height)
    config["OPTIONS"]["wav2lip_version"] = str(wav2lip_version)
    config["OPTIONS"]["use_previous_tracking_data"] = str(use_previous_tracking_data)
    config["OPTIONS"]["nosmooth"] = str(nosmooth)
    config["OPTIONS"]["preview_window"] = str(preview_window)
    
    # Update other settings
    config["OTHER"]["batch_process"] = str(batch_process)
    config["OTHER"]["output_suffix"] = str(output_suffix)
    config["OTHER"]["include_settings_in_suffix"] = str(include_settings)
    config["OTHER"]["preview_settings"] = str(preview_settings)
    config["OTHER"]["frame_to_preview"] = str(frame_to_preview)
    
    # Save updated config
    save_config(config)
    
    # Define the path to the run.py script and Python executable in venv
    script_path = r"C:/Lips_snyc/wav2lipnew/Easy-Wav2Lip/run.py"
    python_executable = sys.executable

    # Check if the run.py script exists before running it
    if not os.path.exists(script_path):
        return "The script run.py was not found. Please check the path."
    
    # Check if the input video and vocal files exist
    if not os.path.exists(video_file):
        return f"Input video file not found: {video_file}"
    if not os.path.exists(vocal_file):
        return f"Input vocal file not found: {vocal_file}"
    
    # Prepare output directory
    output_dir = os.path.join(os.getcwd(), "temp")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_video_path = os.path.join(output_dir, "output.mp4")

    # Run the Easy-Wav2Lip script
    try:
        subprocess.run([python_executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        return f"Error occurred while running the script: {str(e)}"

    # Check if output video exists and return it for display and download
    if os.path.exists(output_video_path):
        return output_video_path
    else:
        return "Output video not found. Please check the script execution."

# Function to create the Gradio interface
def create_interface():
    config = read_config()
    
    # CSS for the orange and black theme
    orange_black_css = """
    body, .gradio-container {
        background-color: #000000; /* Black background */
        color: #ffffff; /* White text for readability */
        font-family: 'Roboto', sans-serif;
    }
    .gradio-title {
        font-size: 1.8em;
        font-weight: bold;
        color: #ffa500; /* Orange title */
        margin-left: 10px; /* Space between logo and title */
    }
    .gradio-description {
        margin-bottom: 20px;
        font-size: 1em;
        color: #b0b0b0;
    }
    .gradio-container {
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(255, 165, 0, 0.5); /* Orange glow */
        padding: 20px;
    }
    h1, h2, p {
        color: #ffffff; /* White font for headings and paragraphs */
    }
    .gradio-block, .gradio-input, .gradio-output, input, textarea, select, button {
        background-color: #1e1e1e; /* Dark grey for inputs */
        color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ffa500; /* Orange border */
    }
    button {
        background-color: #ffa500; /* Orange button */
        color: #000000; /* Black text */
        padding: 8px 15px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 1em;
    }
    button:hover {
        background-color: #ff8c00; /* Darker orange on hover */
    }
    .output-file-download, .output-file-preview {
        color: #ffa500; /* Orange download link */
    }
    img.logo {
        max-height: 40px; /* Responsive height */
        margin-right: 10px; /* Space between logo and title */
        vertical-align: middle; /* Align with text */
        object-fit: contain; /* Maintain aspect ratio */
    }
    .header-container {
        display: flex; /* Flex layout for logo and title */
        align-items: center; /* Center vertically */
        justify-content: center; /* Center horizontally */
    }
"""

   # HTML for title with logo
    title_with_logo = """
    <div class="header-container">
        <h2>Antriksh.AI</h2>
        <img src="https://i.ibb.co/jbMHNkY/Antriksh.jpg" class="logo" alt="Logo" />
    </div>
    """
    interface = gr.Interface(
        fn=start_easy_wav2lip,
        inputs=[
            gr.File(label="Select Video File", file_count="single"),
            gr.File(label="Select Vocal File", file_count="single"),
            gr.Radio(choices=["Fast", "Improved", "Enhanced"], label="Select Quality",
                     value=config.get("OPTIONS", "quality", fallback="Improved")),
            gr.Dropdown(choices=["half resolution", "full resolution"], label="Output Height",
                        value=config.get("OPTIONS", "output_height", fallback="full resolution")),
            gr.Radio(choices=["Wav2Lip", "Wav2Lip_GAN"], label="Select Wav2Lip Version",
                     value=config.get("OPTIONS", "wav2lip_version", fallback="Wav2Lip")),
            gr.Textbox(label="Output Suffix", value=config.get("OTHER", "output_suffix", fallback="_Easy-Wav2Lip")),
            gr.Checkbox(label="Include Settings in Suffix", 
                        value=config.getboolean("OTHER", "include_settings_in_suffix", fallback=True)),
            gr.Checkbox(label="Batch Process", 
                        value=config.getboolean("OTHER", "batch_process", fallback=True)),
            gr.Radio(choices=["Face", "Full", "Both", "None"], label="Preview Window", 
                     value=config.get("OPTIONS", "preview_window", fallback="Face")),
            gr.Checkbox(label="Nosmooth", 
                        value=config.getboolean("OPTIONS", "nosmooth", fallback=True)),
            gr.Checkbox(label="Use Previous Tracking Data", 
                        value=config.getboolean("OPTIONS", "use_previous_tracking_data", fallback=True)),
            gr.Checkbox(label="Preview Settings", 
                        value=config.getboolean("OTHER", "preview_settings", fallback=True)),
            gr.Number(label="Frame to Preview", 
                      value=config.getint("OTHER", "frame_to_preview", fallback=100), precision=0)
        ],
        outputs=gr.File(label="Download Output Video"),
        # title="Antriksh.AI",
        title=title_with_logo,
        description="Configure and run Easy-Wav2Lip with an intuitive interface.",
        css=orange_black_css
    )
    return interface

# Launch the Gradio interface
interface = create_interface()
interface.launch(share=True)
