# Project Name

A brief description of the project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and set up the project in a virtual environment, follow these steps:

1. Create a virtual environment:
        ```shell
        python -m venv .venv
        ```

2. Activate the virtual environment:
        - On Windows:
            ```shell
            .venv\Scripts\activate
            ```
        - On macOS and Linux:
            ```shell
            source .venv/bin/activate
            ```

3. Install the project package using pip:
        ```shell
        pip install -e .
        ```

4. Install a formula1 analytics package from another path:
        ```shell
        pip install path-to-formula1_analytics-package
        ```

     If you don't have the formula1 analytics package, you can download it from [here](https://github.com/Dewciu/formula1_analytics).

5. Set up the database from another package using Docker Compose:
    - Download the database package from [here](https://github.com/Dewciu/formula1_dockers).
    - Navigate to the downloaded package directory:
        ```shell
        cd /path/to/database_package
        ```
    - Start the database containers:
        ```shell
        docker-compose up -d
        ```



## Usage

Instructions on how to use the project or any relevant examples.

To run the Python Flask app, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the project directory:
    ```shell
    cd /path/to/project
    ```

3. Run the Flask app:
    ```shell
    python run.py
    ```

4. Access the app in your web browser at `http://localhost:5000`.

## Contributing

Guidelines on how to contribute to the project.

## License

Information about the project's license.
