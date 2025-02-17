# Real-time Stock Price Visualization with Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Dockerized](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://www.docker.com/)
[![DevContainers](https://img.shields.io/badge/DevContainers-ready-brightgreen?logo=visualstudiocode)](https://code.visualstudio.com/docs/devcontainers/containers)

This project demonstrates a simple real-time stock price visualization application built using Streamlit, yfinance, and Matplotlib. It allows users to enter a stock ticker symbol, select a time period and data interval, and see a live-updating chart of the stock's closing price.

## Features

*   **Real-time Updates:** The stock price chart updates automatically at a user-defined interval.
*   **User-configurable Ticker:**  Enter any valid stock ticker symbol (e.g., AAPL, MSFT, GOOG).
*   **Adjustable Update Interval:** Control how often the data is fetched and the chart is updated using a slider.
*   **Selectable Time Period and Interval:** Choose from various time periods (e.g., 1 day, 5 days, 1 month) and data intervals (e.g., 1 minute, 5 minutes, 1 hour) to customize the chart.
*   **Error Handling:** Handles invalid ticker symbols and data fetching errors gracefully.
*   **Caching:** Uses Streamlit's caching mechanism (`@st.cache_data`) to improve performance and reduce API calls.
*   **Stop/Start Updates:**  A button allows you to pause and resume the real-time updates without stopping the entire script.
*   **Dockerized:** Includes a `Dockerfile` for easy deployment and reproducibility.
*   **Dev Container Support:**  Includes a `.devcontainer` configuration for a consistent development environment using VS Code and Docker.

## Prerequisites

You have several options for running this project:

**Option 1: Local Python Environment (Recommended for Development):**

*   **Python 3.7+:** Make sure you have Python 3.7 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
*   **pip:**  You'll need `pip`, the Python package installer. It usually comes with Python.

**Option 2: Docker (Recommended for Deployment):**

*   **Docker Desktop:** Install Docker Desktop (or another Docker engine) from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).

**Option 3: VS Code Dev Container (Recommended for Consistent Development):**

*   **Visual Studio Code:** Install VS Code from [https://code.visualstudio.com/](https://code.visualstudio.com/).
*   **Docker Desktop:**  (See above).
*   **Dev Containers Extension:** Install the "Dev Containers" extension in VS Code. You can find it in the VS Code Extensions Marketplace.

## Getting Started

### Option 1: Local Python Environment

1.  **Clone the Repository:**

    ```bash
    git clone <your_repository_url>  # Replace with the URL of your Git repository
    cd <your_repository_name>
    ```

2.  **Create a Virtual Environment (Highly Recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    .venv\Scripts\activate.bat  # On Windows (Command Prompt)
    .venv\Scripts\Activate.ps1  # On Windows (PowerShell)
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**

    ```bash
    streamlit run app.py
    ```

    This will open the app in your default web browser (usually at `http://localhost:8501`).

5.  **Stop the App:** Press Ctrl+C in the terminal where the app is running.  Deactivate the virtual environment when you're done: `deactivate`.

### Option 2: Docker

1.  **Clone the Repository:** (Same as above).
2.  **Build the Docker Image:**

    ```bash
    docker build -t stock-app .
    ```

3.  **Run the Docker Container:**

    ```bash
    docker run -p 8501:8501 stock-app
    ```

    This will start the app, and you can access it in your browser at `http://localhost:8501`.

4.  **Stop the Container:** Find the container ID using `docker ps`, then run `docker stop <container_id>`.  Or, press Ctrl+C in the terminal where the container is running.

### Option 3: VS Code Dev Container

1.  **Clone the Repository:** (Same as above).
2.  **Open in VS Code:** Open the project folder in VS Code.
3.  **Reopen in Container:**
    *   VS Code should automatically detect the `.devcontainer` folder and prompt you to "Reopen in Container". Click this.
    *   If not, open the Command Palette (View > Command Palette, or Ctrl+Shift+P / Cmd+Shift+P) and type "Dev Containers: Reopen in Container".

4.  **Run the App (Inside the Container):**
    *   Open a terminal within VS Code (Terminal > New Terminal).  This terminal is *inside* the container.
    *   Run: `streamlit run app.py`
    *   The app will be available at `http://localhost:8501` in your host machine's browser.

5.  **Stop the Container:** Close the VS Code window connected to the container, or use "Dev Containers: Stop Container" from the Command Palette.

## Project Structure

*   **`app.py`:** The main Python script containing the Streamlit application logic.
*   **`requirements.txt`:** Lists the required Python packages.
*   **`Dockerfile`:**  Defines how to build the Docker image.
*   **`.devcontainer/devcontainer.json`:**  Configuration file for VS Code Dev Containers.
*   **`README.md`:** This file, providing instructions and information about the project.

## Notes

*   **yfinance and Real-time Data:**  `yfinance` provides delayed data, not truly real-time data.  The delay is typically a few minutes.
*   **API Rate Limits:** Be mindful of Yahoo Finance's API rate limits.  Excessive requests might result in temporary blocking. The caching and update interval features help to mitigate this.
*   **Stopping the Script:**  The "Stop Updates" button in the Streamlit app *pauses* the data fetching and plotting, but it doesn't completely terminate the Python script.  To fully stop the script, you need to press Ctrl+C in the terminal where it's running (or stop the Docker container).
* **Virtual Environment:** Always work within a virtual environment.
* **Docker Images:** If you make changes to the requirements or the app, rebuild the image.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or new features.

## License
This project is open source, you can use it as you please.