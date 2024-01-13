# Formula 1 Statistics

# Formula 1 Statistics App

The Formula 1 Statistics App is a project that aims to provide statistical analysis and insights for Formula 1 racing enthusiasts. It offers a range of features and functionalities to explore and analyze various aspects of Formula 1, including driver performance, team standings, race results, and more.

With this app, users can access a comprehensive database of Formula 1 data and leverage powerful analytics tools to gain valuable insights. Whether you're a casual fan or a dedicated follower of the sport, the Formula 1 Statistics App is designed to enhance your understanding and enjoyment of Formula 1 racing.

Explore the app's intuitive user interface, dive into detailed statistics, and stay up-to-date with the latest race results and championship standings. Whether you're interested in historical data or real-time analysis, the Formula 1 Statistics App has you covered.

Start exploring the world of Formula 1 like never before with the Formula 1 Statistics App!

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

Guidelines on how to contribute to the project:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them with descriptive messages.
- Push your changes to your forked repository.
- Submit a pull request to the main repository.

Please ensure that you follow our [code of conduct](./CODE_OF_CONDUCT.md) when contributing.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Please see the [LICENSE](./LICENSE) file for more details.


## License

### License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). Please see the [LICENSE](./LICENSE) file for more details.
