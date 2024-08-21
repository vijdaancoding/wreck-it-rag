# **Wreck-it-RAG**

<img src="Other/file.png" width="150" height="auto" alt="Wreck-it-RAG Logo">


The repo is an attempt to create an automated pipleine for extracting infromation from different documents and converting them into JSON

## **To-Do List**
📝 Add OpenAI API Key Support<br>
📝 ~~Make streamlit editable to choose between OCR or LLM summaries~~<br>
📝 Concatenate JSON blocks for page-by-page chunking<br>
📝 Replace pip with poetry<br>
📝 ~~Convert Tables from HTML to JSON~~<br>
📝 Integrate SQL database to store JSON<br>
📝 Look into Apache Spark or Hadoop<br>

## **Downloading UNSTRUCTURED.IO Dependancies**

Follow [UNSTRUCTURED.IO's](https://docs.unstructured.io/open-source/installation/full-installation) own installation guide to download all dependancies

## Quick Summary of Installation Guide

## **Windows**

### 1. libmagic-dev

Use WSL to enter the following commands
```
sudo apt update
sudo apt install libmagic-dev
```

### 2. Poppler

Check out the [pdf2image docs](https://pdf2image.readthedocs.io/en/latest/installation.html) on how to install Poppler on various devices

### 3. libreoffice

Check out the official page of [libreoffice](https://www.libreoffice.org/download/download-libreoffice/) for download guides.

Once the `.msi` or `.exe` file is downloaded follow the on-screen instructions

### 4. Tesseract

The latest installer for Tesseract on windows can be found [here](https://github.com/UB-Mannheim/tesseract/wiki)

Make sure to add the `C:\Program Files\Tesseract-OCR` to your Path.

## **2. Installing pip Requirements**

Enter the following code to install all python libraries
```
pip install -r requirements.txt
```

## **3. Create .env File**

Create an .env file with the following variable
```
GEMINI_API_KEY = your-gemini-api-key-here
```

