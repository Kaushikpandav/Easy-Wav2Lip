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
import tkinter as tk
from tkinter import filedialog, ttk
import configparser
import os

try:
    with open('installed.txt', 'r') as file:
        version = file.read()
except FileNotFoundError:
    print("Easy-Wav2Lip does not appear to have installed correctly.")
    print("Please try to install it again.")
    print("https://github.com/anothermartz/Easy-Wav2Lip/issues")
    input()
    exit()

print("opening GUI")

runfile = 'run.txt'
if os.path.exists(runfile):
    os.remove(runfile)

import webbrowser

def open_github_link(event):
    webbrowser.open("https://github.com/anothermartz/Easy-Wav2Lip?tab=readme-ov-file#advanced-tweaking")

def read_config():
    # Read the config.ini file
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

def save_config(config):
    # Save the updated config back to config.ini
    with open("config.ini", "w") as config_file:
        config.write(config_file)

def open_video_file():
    file_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("All files", "*.*")])
    if file_path:
        video_file_var.set(file_path)
        
def open_vocal_file():
    file_path = filedialog.askopenfilename(title="Select a vocal file", filetypes=[("All files", "*.*")])
    if file_path:
        vocal_file_var.set(file_path)

# feathering
def validate_frame_preview(P):
    if P == "":
        return True  # Allow empty input
    try:
        num = float(P)
        if (num.is_integer()):
            return True
    except ValueError:
        pass
    return False

def start_easy_wav2lip():
    # Start Easy-Wav2Lip processing
    print("Saving config")
    config["OPTIONS"]["video_file"] = str(video_file_var.get())
    config["OPTIONS"]["vocal_file"] = str(vocal_file_var.get())
    config["OPTIONS"]["quality"] = str(quality_var.get())
    config["OPTIONS"]["output_height"] = str(output_height_combobox.get())
    config["OPTIONS"]["wav2lip_version"] = str(wav2lip_version_var.get())
    config["OPTIONS"]["use_previous_tracking_data"] = str(use_previous_tracking_data_var.get())
    config["OPTIONS"]["nosmooth"] = str(nosmooth_var.get())
    config["OPTIONS"]["preview_window"] = str(preview_window_var.get())
    config["PADDING"]["u"] = str(padding_vars["u"].get())
    config["PADDING"]["d"] = str(padding_vars["d"].get())
    config["PADDING"]["l"] = str(padding_vars["l"].get())
    config["PADDING"]["r"] = str(padding_vars["r"].get())
    config["MASK"]["size"] = str(size_var.get())
    config["MASK"]["feathering"] = str(feathering_var.get())
    config["MASK"]["mouth_tracking"] = str(mouth_tracking_var.get())
    config["MASK"]["debug_mask"] = str(debug_mask_var.get())
    config["OTHER"]["batch_process"] = str(batch_process_var.get())
    config["OTHER"]["output_suffix"] = str(output_suffix_var.get())
    config["OTHER"]["include_settings_in_suffix"] = str(include_settings_in_suffix_var.get())
    config["OTHER"]["preview_settings"] = str(preview_settings_var.get())
    config["OTHER"]["frame_to_preview"] = str(frame_to_preview_var.get())
    save_config(config)  # Save the updated config
    with open("run.txt", "w") as f:
        f.write("run")
        exit()
    # Add your logic here

root = tk.Tk()
root.title("Easy-Wav2Lip GUI")
root.geometry("800x720")
root.configure(bg="lightblue")

# Read the existing config.ini
config = read_config()

row=0
tk.Label(root, text=version, bg="lightblue").grid(row=row, column=0, sticky="w")
# Create a label for video file
row+=1
video_label = tk.Label(root, text="Video File Path:", bg="lightblue")
video_label.grid(row=row, column=0, sticky="e")

# Entry widget for video file path
video_file_var = tk.StringVar()
video_entry = tk.Entry(root, textvariable=video_file_var, width=80)
video_entry.grid(row=row, column=1, sticky="w")

# Create a button to open the file dialog
select_button = tk.Button(root, text="...", command=open_video_file)
select_button.grid(row=row, column=1, sticky="w", padx=490)

# Set the default value based on the existing config
video_file_var.set(config["OPTIONS"].get("video_file", ""))

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

# String input for vocal_file
row+=1

# Create a label for the input box
vocal_file_label = tk.Label(root, text="Vocal File Path:", bg="lightblue")
vocal_file_label.grid(row=row, column=0, sticky="e")

# Create an input box for the vocal file path
vocal_file_var = tk.StringVar()
vocal_file_entry = tk.Entry(root, textvariable=vocal_file_var, width=80)
vocal_file_entry.grid(row=row, column=1, sticky="w")

# Create a button to open the file dialog
select_button = tk.Button(root, text="...", command=open_vocal_file)
select_button.grid(row=row, column=1, sticky="w", padx=490)

# Set the initial value from the 'config' dictionary (if available)
vocal_file_var.set(config["OPTIONS"].get("vocal_file", ""))

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

# Dropdown box for quality options
row+=1
quality_label = tk.Label(root, text="Select Quality:", bg="lightblue")
quality_label.grid(row=row, column=0, sticky="e")
quality_options = ["Fast", "Improved", "Enhanced"]
quality_var = tk.StringVar()
quality_var.set(config["OPTIONS"].get("quality", "Improved"))
quality_dropdown = tk.OptionMenu(root, quality_var, *quality_options)
quality_dropdown.grid(row=row, column=1, sticky="w")

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

# Output height
row+=1
output_height_label = tk.Label(root, text="Output height:", bg="lightblue")
output_height_label.grid(row=row, column=0, sticky="e")
output_height_options = ["half resolution", "full resolution"]
output_height_combobox = ttk.Combobox(root, values=output_height_options)
output_height_combobox.set(config["OPTIONS"].get("output_height", "full resolution"))  # Set default value
output_height_combobox.grid(row=row, column=1, sticky="w") 

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

# Dropdown box for wav2lip version options
row+=1
wav2lip_version_label = tk.Label(root, text="Select Wav2Lip version:", bg="lightblue")
wav2lip_version_label.grid(row=row, column=0, sticky="e")
wav2lip_version_options = ["Wav2Lip", "Wav2Lip_GAN"]
wav2lip_version_var = tk.StringVar()
wav2lip_version_var.set(config["OPTIONS"].get("wav2lip_version", "Wav2Lip"))
wav2lip_version_dropdown = tk.OptionMenu(root, wav2lip_version_var, *wav2lip_version_options)
wav2lip_version_dropdown.grid(row=row, column=1, sticky="w")

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")
# output_suffix
row+=1
output_suffix_label = tk.Label(root, text="Output File Suffix:", bg="lightblue")
output_suffix_label.grid(row=row, column=0, sticky="e")
output_suffix_var = tk.StringVar()
output_suffix_var.set(config["OTHER"].get("output_suffix", "_Easy-Wav2Lip"))
output_suffix_entry = output_suffix_entry = tk.Entry(root, textvariable=output_suffix_var, width=20)
output_suffix_entry.grid(row=row, column=1, sticky="w")

include_settings_in_suffix_var = tk.BooleanVar()
include_settings_in_suffix_var.set(config["OTHER"].get("include_settings_in_suffix", True))  # Set default value
include_settings_in_suffix_checkbox = tk.Checkbutton(root, text="Add Settings to Suffix", variable=include_settings_in_suffix_var, bg="lightblue")
include_settings_in_suffix_checkbox.grid(row=row, column=1, sticky="w", padx=130)

# batch_process
row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")
row+=1
batch_process_label = tk.Label(root, text="Batch Process:", bg="lightblue")
batch_process_label.grid(row=row, column=0, sticky="e")
batch_process_var = tk.BooleanVar()
batch_process_var.set(config["OTHER"].get("batch_process", True))  # Set default value
batch_process_checkbox = tk.Checkbutton(root, text="", variable=batch_process_var, bg="lightblue")
batch_process_checkbox.grid(row=row, column=1, sticky="w")

# Dropdown box for preview window options
row+=1
preview_window_label = tk.Label(root, text="Preview Window:", bg="lightblue")
preview_window_label.grid(row=row, column=0, sticky="e")
preview_window_options = ["Face", "Full", "Both", "None"]
preview_window_var = tk.StringVar()
preview_window_var.set(config["OPTIONS"].get("preview_window", "Face"))
preview_window_dropdown = tk.OptionMenu(root, preview_window_var, *preview_window_options)
preview_window_dropdown.grid(row=row, column=1, sticky="w")

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

# Button to start Easy-Wav2Lip
row+=1
start_button = tk.Button(root, text="Start Easy-Wav2Lip", command=start_easy_wav2lip, bg="#5af269", font=("Arial", 16))
start_button.grid(row=row, column=0, sticky="w", padx=290, columnspan=2)

row+=1
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")
tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")

row+=1
tk.Label(root, text="Advanced Tweaking:", bg="lightblue", font=("Arial", 16)).grid(row=row, column=0, sticky="w")
row+=1
# Create a label with a custom cursor
link = tk.Label(root, text="(Click here to see readme)", bg="lightblue", fg="blue", font=("Arial", 10), cursor="hand2")
link.grid(row=row, column=0)

# Bind the click event to the label
link.bind("<Button-1>", open_github_link)

# Process one frame only
preview_settings_var = tk.BooleanVar()
preview_settings_var.set(config["OTHER"].get("preview_settings", True))  # Set default value
preview_settings_checkbox = tk.Checkbutton(root, text="Process one frame only - Frame to process:", variable=preview_settings_var, bg="lightblue")
preview_settings_checkbox.grid(row=row, column=1, sticky="w")

frame_to_preview_var = tk.StringVar()
frame_to_preview_entry = tk.Entry(root, textvariable=frame_to_preview_var, validate="key", width=3, validatecommand=(root.register(validate_frame_preview), "%P"))
frame_to_preview_entry.grid(row=row, column=1, sticky="w", padx=255)
frame_to_preview_var.set(config["OTHER"].get("frame_to_preview", "100"))

# Checkbox for nosmooth option
row+=1
nosmooth_var = tk.BooleanVar()
nosmooth_var.set(config["OPTIONS"].get("nosmooth", True))  # Set default value
nosmooth_checkbox = tk.Checkbutton(root, text="nosmooth - unticking will smooth face detection between 5 frames", variable=nosmooth_var, bg="lightblue")
nosmooth_checkbox.grid(row=row, column=1, sticky="w")

# Checkbox for use_previous_tracking_data option
row+=1
use_previous_tracking_data_var = tk.BooleanVar()
use_previous_tracking_data_var.set(config["OPTIONS"].get("use_previous_tracking_data", True))  # Set default value
use_previous_tracking_data_checkbox = tk.Checkbutton(root, text="Keep previous face tracking data if using same video", variable=use_previous_tracking_data_var, bg="lightblue")
use_previous_tracking_data_checkbox.grid(row=row, column=1, sticky="w")

# padding
row+=1
tk.Label(root, text="Padding:", bg="lightblue", font=("Arial", 12)).grid(row=row, column=1, sticky="sw", pady=10)
row+=1
tk.Label(root, text="(Up, Down, Left, Right)", bg="lightblue").grid(row=row, column=1, rowspan=4, sticky="w", padx=100)
padding_vars = {}

# Create a list of padding labels and their corresponding keys
padding_labels = [("U:", "u"), ("D:", "d"), ("L:", "l"), ("R:", "r")]

# Validation function to allow only integers
def validate_integer(P):
    if P == "" or P == "-" or P.lstrip("-").isdigit():
        return True
    return False

# Create the padding labels and entry widgets using a loop
for label_text, key in padding_labels:
    label = tk.Label(root, text=label_text, bg="lightblue")
    label.grid(row=row, column=1, sticky="w", padx=50)

    # Create a StringVar for the current key
    padding_var = tk.StringVar()

    # Set validation to allow positive and negative integers
    entry = tk.Entry(root, textvariable=padding_var, width=3, validate="key", validatecommand=(root.register(validate_integer), "%P"))
    entry.grid(row=row, column=1, sticky="w", padx=70)

    # Set the default value from the 'config' dictionary
    padding_var.set(config["PADDING"].get(key, ""))

    # Store the StringVar in the dictionary
    padding_vars[key] = padding_var

    # Increment the row
    row += 1


tk.Label(root, text="", bg="lightblue").grid(row=row, column=0, sticky="w")
row+=1
# mask size
def validate_custom_number(P):
    if P == "":
        return True  # Allow empty input
    try:
        num = float(P)
        if 0 <= num <= 6 and (num.is_integer() or (num * 10) % 1 == 0):
            return True
    except ValueError:
        pass
    return False

row+=1
tk.Label(root, text="Mask settings:", bg="lightblue", font=("Arial", 12)).grid(row=row, column=1, sticky="sw")
row+=1
size_label = tk.Label(root, text="Mask size:", bg="lightblue", padx=50)
size_label.grid(row=row, column=1, sticky="w")
size_var = tk.StringVar()
size_entry = tk.Entry(root, textvariable=size_var, validate="key", width=3, validatecommand=(root.register(validate_custom_number), "%P"))
size_entry.grid(row=row, column=1, sticky="w", padx=120)
size_var.set(config["MASK"].get("size", "2.5"))

# feathering
def validate_feather(P):
    if P == "":
        return True  # Allow empty input
    try:
        num = float(P)
        if 0 <= num <= 3 and (num.is_integer()):
            return True
    except ValueError:
        pass
    return False
    
row+=1
feathering_label = tk.Label(root, text="Feathering:", bg="lightblue", padx=50)
feathering_label.grid(row=row, column=1, sticky="w")
feathering_var = tk.StringVar()
feathering_entry = tk.Entry(root, textvariable=feathering_var, validate="key", width=3, validatecommand=(root.register(validate_feather), "%P"))
feathering_entry.grid(row=row, column=1, sticky="w", padx=120)
feathering_var.set(config["MASK"].get("feathering", "2.5"))

# mouth_tracking
row+=1
mouth_tracking_var = tk.BooleanVar()
mouth_tracking_var.set(config["MASK"].get("mouth_tracking", True))  # Set default value
mouth_tracking_checkbox = tk.Checkbutton(root, text="track mouth for mask on every frame", variable=mouth_tracking_var, bg="lightblue", padx=50)
mouth_tracking_checkbox.grid(row=row, column=1, sticky="w")

# debug_mask
row+=1
debug_mask_var = tk.BooleanVar()
debug_mask_var.set(config["MASK"].get("debug_mask", True))  # Set default value
debug_mask_checkbox = tk.Checkbutton(root, text="highlight mask for debugging", variable=debug_mask_var, bg="lightblue", padx=50)
debug_mask_checkbox.grid(row=row, column=1, sticky="w")

# Increase spacing between all rows (uniformly)
for row in range(row):
    root.rowconfigure(row, weight=1)


root.mainloop()
