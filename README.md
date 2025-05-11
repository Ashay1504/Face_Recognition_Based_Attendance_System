# Face Recognition Attendance System

A Python-based application that uses facial recognition to mark and manage attendance. It features a Tkinter GUI for user interaction, allowing for easy enrollment of new faces, real-time attendance marking, and viewing of daily attendance logs.

## Features

*   **User Enrollment:** Register new users by capturing 100 face samples via webcam.
*   **Real-time Attendance:** Detects faces via webcam, recognizes registered individuals, and marks their attendance.
*   **Attendance Logging:** Saves attendance records (Name, Timestamp) in CSV files, organized by date in an `Attendance` directory.
*   **Duplicate Prevention:** Prevents marking attendance for the same person multiple times on the same day within a session.
*   **Voice Feedback:** Provides audible confirmation when attendance is taken or if it's already marked.
*   **GUI Interface:** Simple Tkinter-based GUI to:
    *   Add new faces.
    *   Start the attendance process.
    *   View today's attendance log.
*   **Streamlit Viewer (Optional):** An alternative `app.py` script to view today's attendance log using Streamlit in a web browser.

## Project Structure
.
├── Attendance/ # Stores daily attendance CSV files (e.g., Attendance_DD-MM-YYYY.csv)
├── data/ # Stores face data and Haar cascade
│ ├── haarcascade_frontalface_default.xml # Haar cascade for face detection
│ ├── faces_data.pkl # (Generated) Stores encoded face data
│ └── names.pkl # (Generated) Stores names corresponding to face data
├── add_faces.py # Script to enroll new faces and save their data
├── app.py # Streamlit app to view attendance (alternative viewer)
├── gui_app.py # Main Tkinter GUI application (Recommended entry point)
├── main_app.py # Alternative Tkinter GUI (uses some absolute paths, less portable)
├── test.py # Script for real-time attendance marking and saving
└── README.md # This file
## Prerequisites

*   Python 3.7+
*   A webcam connected to your system.
*   pip (Python package installer)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory-name>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install opencv-python numpy pandas scikit-learn streamlit pywin32
    ```
    *(Note: `pywin32` is for voice feedback on Windows. If on another OS or if you don't need voice, you might need to adapt or remove the speech parts in `test.py`.)*

4.  **Create necessary directories:**
    Make sure you have the following directories in your project's root:
    *   `data/`
    *   `Attendance/`

5.  **Download Haar Cascade File:**
    Download the `haarcascade_frontalface_default.xml` file. You can find it in the OpenCV GitHub repository:
    [https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml)
    Place this file inside the `data/` directory.

## Usage

1.  **Run the main application GUI:**
    It's recommended to use `gui_app.py` as it uses relative paths for subprocesses.
    ```bash
    python gui_app.py
    ```
    Alternatively, you can try `main_app.py`, but be aware it might have hardcoded paths that need adjustment for your system.

2.  **Add New Face (Enrollment):**
    *   In the GUI, enter the name of the person you want to register in the "Enter Name for Registration" field.
    *   Click the "Add New Face" button.
    *   A new window will open showing your webcam feed.
    *   Position your face in front of the camera. The system will capture 100 images of your face. A counter will show the progress.
    *   Once 100 samples are collected (or if you press 'q' to quit early), the window will close. The face data and name will be saved.

3.  **Take Attendance:**
    *   Click the "Take Attendance" button in the GUI.
    *   A new window will open showing your webcam feed.
    *   The system will try to detect and recognize faces. The recognized name will be displayed above the detected face.
    *   To mark the attendance for the currently recognized person, **press the 'O' key** (letter O).
        *   You'll hear "Attendance Taken" if successful.
        *   If attendance for that person was already taken in the current session, you'll hear "Attendance for [Name] is already taken."
    *   To close the attendance window, **press the 'Q' key**.

4.  **View Today's Attendance:**
    *   Click the "View Today’s Attendance" button in the GUI.
    *   If an attendance file exists for the current date (`Attendance/Attendance_DD-MM-YYYY.csv`), a new window will pop up displaying the attendance log.
    *   If no file exists, a message box will inform you.

5.  **Exit Application:**
    *   Click the "Exit" button in the GUI.

### Alternative Attendance Viewing (Streamlit)

You can also view the attendance log for the current day using the Streamlit app:
```bash
streamlit run app.py
Use code with caution.
This will open a web page in your browser displaying the attendance data.
How it Works
Face Enrollment (add_faces.py):
Captures 100 grayscale face crops (50x50 pixels) using OpenCV and a Haar Cascade for face detection.
These face samples are flattened and stored in data/faces_data.pkl.
The corresponding names (repeated 100 times per user) are stored in data/names.pkl.
Attendance Marking (test.py):
Loads the saved face data and names.
Trains a K-Nearest Neighbors (KNN) classifier with the loaded data.
Captures video from the webcam.
For each frame:
Detects faces using the Haar Cascade.
For each detected face, it crops, resizes, flattens the image, and uses the KNN model to predict the name.
Displays the predicted name on the video feed.
If 'O' is pressed, the recognized name and current timestamp are recorded in Attendance/Attendance_DD-MM-YYYY.csv. It checks for duplicates within the current session.
GUI (gui_app.py / main_app.py):
Provides buttons to trigger add_faces.py (passing the name via an environment variable) and test.py as subprocesses.
Includes a function to read and display the daily attendance CSV file.
Important Notes
Lighting and Face Angles: For best results during enrollment and attendance, ensure good, consistent lighting and try to face the camera directly. Varying angles slightly during enrollment can help improve recognition robustness.
Accuracy: The accuracy of the KNN model depends on the quality and variety of the enrolled face samples.
main_app.py vs gui_app.py: main_app.py contains some hardcoded absolute paths for calling add_faces.py and test.py. gui_app.py is generally more portable as it assumes these scripts are in the same directory. It's recommended to use or adapt gui_app.py.
Data Files:
data/faces_data.pkl and data/names.pkl are binary files storing NumPy arrays and lists, respectively. Do not edit them manually.
If you want to reset the registered faces, delete faces_data.pkl and names.pkl from the data directory.
Windows Speech: The win32com.client for speech output is Windows-specific. If running on macOS or Linux, you'll need to replace this with an equivalent (e.g., pyttsx3 or espeak via subprocess) or remove the speech functionality.
Troubleshooting
"No module named cv2": Ensure OpenCV is installed correctly: pip install opencv-python.
Webcam not working:
Make sure your webcam is connected and enabled.
Check if other applications are using the webcam.
The cv2.VideoCapture(0) line might need to be changed if 0 is not your default webcam (e.g., try cv2.VideoCapture(1)).
"Error: Please enter a name.": Make sure to type a name in the input field before clicking "Add New Face".
"No attendance file found for today": This means either no attendance has been taken yet for the current day, or the file path is incorrect. Ensure the Attendance directory exists and the script has write permissions.
pywin32 installation issues: Sometimes pip install pywin32 can be tricky. You might try pip install pypiwin32 as an alternative.
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
License
MIT (or choose another license like Apache 2.0, GPL, etc., as you see fit for your project)
**Before you commit this `README.md`:**

1.  **Replace `<your-repository-url>`** with the actual URL of your GitHub repository.
2.  **Replace `<repository-directory-name>`** with the name of the directory created when cloning.
3.  **Choose a License:** If you don't want MIT, select another one and update the License section. If you're unsure, MIT is a good permissive default.
4.  **Verify Paths:** Double-check that the file paths mentioned in the README match your project structure exactly, especially for `haarcascade_frontalface_default.xml`.
5.  **Test Instructions:** Briefly run through the installation and usage steps yourself to ensure they are clear and correct.
6.  **Hardcoded paths in `main_app.py`**: The README mentions the hardcoded paths in `main_app.py`. If you intend for users to use `main_app.py`, you should fix those paths to be relative (e.g., using `os.path.join(os.path.dirname(__file__), "add_faces.py")`) or clearly instruct users on how to modify them. Since `gui_app.py` is cleaner, I've recommended it.

This README should give users a good starting point to understand, install, and use your project!
