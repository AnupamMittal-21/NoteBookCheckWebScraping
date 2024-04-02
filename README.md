## Web Scraping Project: NotebookCheck Web Scraping

### Overview
This repository contains the code for scraping electronic item details from the NotebookCheck website. The scraping is performed using Python and Selenium WebDriver.

### Installation
1. Install Python on your system if you haven't already.
2. Install Selenium WebDriver using `pip install selenium`.
3. Download the Chrome WebDriver matching your Chrome browser version from [here](https://sites.google.com/chromium.org/driver/).
4. Set the path to the WebDriver in an environment variable named `DRIVER_PATH`.
5. Create a `.env` file and set `DRIVER_PATH` to the path of the Chrome WebDriver.

### Usage
1. Clone this repository to your local machine.
2. Navigate to the directory containing the cloned repository.
3. Make sure you have set up the `.env` file with the `DRIVER_PATH`.
4. Run the Python script to start scraping the NotebookCheck website.

### Additional Configuration (Optional)
- To set the WebDriver as the default browser, add `--user-data-dir=C:\[YourName]\AppData\Local\Google\Chrome\User Data\Default` to the `DRIVER_PATH` in the `.env` file.

### Contributing
Contributions are welcome! If you have any suggestions, bug fixes, or enhancements, feel free to open an issue or create a pull request.

### License
This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for personal or commercial purposes.
