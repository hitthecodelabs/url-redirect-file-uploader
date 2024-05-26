
# URL Redirect File Uploader

This project is a web application that allows users to upload two files: one containing base URLs and another containing redirect URLs. The application processes these files and generates an HTML file that combines the base and redirect URLs. The user can then download the generated HTML file.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Usage](#usage)
- [Deployment](#deployment)
- [License](#license)

## Features

- Upload base URLs file (CSV or TXT)
- Upload redirect URLs file (CSV or TXT)
- Process and distribute base URLs among redirect URLs
- Generate and download an HTML file containing the combined URLs
- Toggle between light and dark themes

## Technologies

- Python 3.10
- Flask 2.1.1
- Gunicorn 20.1.0
- Bootstrap 4.5.2

## Setup

### Prerequisites

- Python 3.10 or higher
- Google Cloud SDK (for deployment)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/hitthecodelabs/url-redirect-file-uploader.git
    cd url-redirect-file-uploader
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1. Create a file named `.env` in the root directory of the project and add the following content:
    ```
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    ```

2. Replace `your_secret_key` with a secure secret key.

## Usage

1. Run the application locally:
    ```sh
    flask run
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Upload the base URLs and redirect URLs files, then click "Upload".

4. Once the files are processed, click "Download Processed File" to download the generated HTML file.

## Deployment

### Google Cloud Platform (GCP)

1. Initialize the GCP project:
    ```sh
    gcloud init
    ```

2. Authenticate with GCP:
    ```sh
    gcloud auth login
    ```

3. Set the project:
    ```sh
    gcloud config set project [PROJECT_ID]
    ```

4. Prepare the `app.yaml` file:
    ```yaml
    runtime: python310
    entrypoint: gunicorn -b :$PORT app:app

    handlers:
    - url: /static
      static_dir: static

    - url: /.*
      script: auto
    ```

5. Deploy the application:
    ```sh
    gcloud app deploy --project=[PROJECT_ID] --quiet
    ```

6. Access the deployed application at the URL provided by GCP:
    ```
    https://[PROJECT_ID].uc.r.appspot.com
    ```

### Managing Versions

1. List all versions:
    ```sh
    gcloud app versions list
    ```

2. Delete specific versions:
    ```sh
    gcloud app versions delete [VERSION_ID]
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Google Cloud Platform](https://cloud.google.com/)
