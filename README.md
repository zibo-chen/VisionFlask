# OCR Text Recognition with Flask and macOS Vision Framework

This project is a Flask-based web application that allows users to upload images and perform Optical Character Recognition (OCR) using the macOS Vision framework. The recognized text and its bounding boxes are returned as JSON and also saved as a `.json` file on the server.

## Features

- Upload images in `png`, `jpg`, or `jpeg` formats.
- Perform text recognition using macOS Vision framework.
- Save the uploaded image and recognition results with unique identifiers.
- Return recognition results as JSON.

## Requirements

- macOS with Python and the necessary macOS frameworks (`Cocoa`, `Quartz`, `Vision`).
- Flask for the web server.
- Werkzeug for secure file handling.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/zibo-chen/VisionFlask.git
    cd VisionFlask
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure you have the necessary macOS frameworks:**

    The project uses `Cocoa`, `Quartz`, and `Vision` frameworks which are available on macOS. Ensure you have these installed and accessible in your Python environment.

## Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. **Upload an image:**

    Use a tool like `curl` or Postman to upload an image to the `/ocr` endpoint.

    ```bash
    curl -X POST -F "file=@path_to_your_image.png" http://localhost:5001/ocr
    ```

3. **View the results:**

    The response will be a JSON object containing the recognized text and their bounding boxes. The uploaded image and the recognition results will be saved in the `uploads` directory with unique identifiers.

## Project Structure

- `app.py`: The main Flask application file.
- `utils/text_recognition.py`: Contains the `TextRecognizer` class that uses macOS Vision framework for text recognition.
- `uploads/`: Directory where uploaded images and recognition results are saved.

## Example

Here is an example of the JSON response from the `/ocr` endpoint:

```json
{
    "log_id": "12345678901234567890",
    "words_result_num": 2,
    "words_result": [
        {
            "words": "Hello",
            "location": {
                "top": 0.1,
                "left": 0.2,
                "width": 0.3,
                "height": 0.4
            }
        },
        {
            "words": "World",
            "location": {
                "top": 0.5,
                "left": 0.6,
                "width": 0.7,
                "height": 0.8
            }
        }
    ]
}
