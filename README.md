# Mailto Link Shortener

This project is a simple Flask application that allows users to generate `mailto:` links and shorten them using the TinyURL API. Users can also update existing TinyURL links with new `mailto:` details.

## Features

- Generate a `mailto:` link with email address, subject, body, CC, and BCC.
- Shorten the generated `mailto:` link using the TinyURL API.
- Update an existing TinyURL alias with a new `mailto:` link.
- Preserve form data after submission for user convenience.

## Prerequisites

- Python 3.x
- Flask
- Requests

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/mailto-link-shortener.git
    cd mailto-link-shortener
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install Flask requests
    ```

## Usage

1. Run the Flask application:

    ```sh
    python app.py
    ```

2. Open a web browser and navigate to `http://127.0.0.1:5000`.

3. Fill in the form with the email details and TinyURL API authorization key.
   - You can choose to either shorten a new link or update an existing alias.
   - If you select "Update URL," make sure to provide the existing alias.

4. Submit the form to generate or update the TinyURL link.

## Project Structure
```
/flask_mailto_shortener
|-- app.py
|-- templates
| |-- index.html
|-- static
| |-- style.css (optional for styling)
```

### `app.py`

This is the main Flask application file containing the route definitions and functions for generating, shortening, and updating `mailto:` links.

### `templates/index.html`

This is the HTML template file rendered by Flask. It contains the form for user input and displays the resulting shortened link.

### `static/style.css`

This optional CSS file is used for styling the HTML template.

## Example

After filling in the form and submitting it, the user will see a shortened `mailto:` link like this: `Shortened Mailto Link: http://tinyurl.com/xyz123`


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
