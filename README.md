# Simple File Server

This repository contains a simple file server upload application built using Streamlit, Apache, and Docker. The application allows users to easily upload and manage files through a web interface.

## Getting Started

To use this application, follow the steps below:

### Prerequisites

- Python 3.x
- Docker

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/streamlit-apache-docker-file-server.git
   cd streamlit-apache-docker-file-server
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Create a `secrets.toml` file in the `.streamlit` folder:

   ```bash
   mkdir .streamlit
   touch .streamlit/secrets.toml
   ```

   Add any necessary secrets or configuration to `secrets.toml`.

### Running the Application

Run the application using Docker Compose:

```bash
docker-compose up -d
```

This command will start the application in detached mode, allowing you to use the file server without tying up your terminal.

Visit [http://localhost:8501](http://localhost:8501) in your web browser to access the file server.

### Stopping the Application

To stop the application, use the following command:

```bash
docker-compose down
```

## Configuration

Customize the application by modifying the `secrets.toml` and `config.toml` files in the `.streamlit` folder. Adjust any required parameters, such as file upload limits or authentication details.

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues. Your feedback and contributions are highly appreciated.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
