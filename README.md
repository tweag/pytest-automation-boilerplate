Pytest Automation Boilerplate
==================================

About the Project
-----------------
The PyTest Automation Boilerplate contains reusable content, which will enable you to test Web, API, Visual and Mobile native apps on web and mobile platforms.

Usages
-----------------
* UI Web Test Automation with Pytest Selenium & Pytest BDD
* API Test Automation with Pytest & Requests
* Mobile Test Automation with Pytest & Appium
* Cross Browser Testing with BrowserStack
* Test Case Management with TestRail
* Notifications with Slack & MS Teams
* Reporting with Allure & Custom HTML
* Parallel Execution with Pytest-xdist

Getting Started
---------------
### Prerequisites

This document assumes that user has:

* A valid github account & access in github.
* Access to `pytest-automation-boilerplate` repository, and/or additional test repositories.
* Have installed your favourite IDEs (Pycharm or VSCode - it's recommended) and/or set up your terminal for development environment.

#### MacOS

1. <u><strong>Homebrew</strong></u>

   Make sure that `homebrew` is successfully installed. Check if it is already installed by typing `brew --version` in
   your terminal. You should see output similar to below lines, if it is already installed
    ```shell
    Homebrew 4.2.12
    ```
   If not installed, please follow below instructions to install. Detailed Instructions
   here: [HomeBrew Installation](https://brew.sh/)
2. <u><strong>Xcode Command-line Tools</strong></u>

   Ensure to have Xcode CLI tools installed. Check if it is already installed using command `xcode-select --version`. If
   it is successfully installed, you would see output similar to this: `xcode-select version 2384.` If not already
   installed, install by typing command `xcode-select --install` in terminal.

3. <u><strong>Android Studio for Local Android Native App </strong></u>

   Ensure to have Android Studio tool installed. and Install Virtual Device Simulator ("deviceName": "emulator-5554").

4. <u><strong>Git</strong></u>

   Most Mac Machines come with latest version of Git pre-installed. Check if you have git installed in your system by
   typing below command in your terminal
    ```shell
    git --version
    # you should see output similar to below if installed.
    git version 2.44.0
    ```
   If not already installed, execute command `brew install git` to install latest git version. After successful
   installation, check for the git version number using command `git --version`.

5. <u><strong>Python</strong></u>

   *Recommended Version of Python: 3.9.12*

   Though Mac comes pre-installed with Python 2.7 and Python 3 (mostly 3.6+), we would not want to 'disturb' the system
   python versions. Its best to leave it undisturbed. We would use `pyenv` to install latest version of Python by
   following below instructions. Detailed Instructions here: [pyenv](https://github.com/pyenv/pyenv)

   *For any issues faced during installation, please refer pyenv GitHub [here](https://github.com/pyenv/pyenv)*

    ```shell
    brew update
    brew install openssl readline sqlite3 xz zlib

    # Any issues encountered during execution of above command, please refer here: `https://github.com/pyenv/pyenv/wiki/Common-build-problems` for possible solutions/workarounds

    # pyenv-installer
    curl https://pyenv.run | bash

    # Restart Shell
    exec $SHELL

    # Verify pyenv is installed successfully
    pyenv --version


    # If you get issues with running above command, ensure the paths are properly set. Run below commands
    # Note: If you source bashrc in profile, then first two lines should come before the line which sources, `source ~/.bashrc` and last line should be at the bottom of the file.
    # If you are using `zsh`, replace .profile with .zprofile, and .bashrc with .zshrc

    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo 'eval "$(pyenv init --path)"' >> ~/.profile
    echo 'eval "$(pyenv virtualenv-init --path)"' >> ~/.profile

    # Also add following lines to .zshrc (if your shell is zsh)
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    # Close the file and source it
    source ~/.zshrc

    # Verify Installation
    username@hostname ~ % exec $SHELL
    username@hostname ~ % pyenv --version

    # Install latest available version of python
    username@hostname ~ % pyenv install 3.9.12
    username@hostname ~ % pyenv global 3.9.12
    ```
   
   *Manual Python 3.9.12 installer: [here](https://www.python.org/downloads/release/python-3912/)*
<p align="right">(<a href="#about-the-project">back to top</a>)</p>

### Installation

1. <u><strong>Clone Boilerplate Project</strong></u>
   Clone the Boilerplate `master` branch from Github to your local machine by following below instructions.

    ```shell
    mkdir workspaces && cd workspaces
    git clone https://github.com/modus/pytest-automation-boilerplate.git
    # alternatively, you could use ssh link if you have setup ssh in your work machine.
    ```

2. <u><strong>source setup_install.sh</strong></u>
   After successful cloning, execute below commands to install BoilerPlate.

    ```shell
    cd pytest-automation-boilerplate/
    source setup_install.sh

3. <u><strong>Activate your Virtual Environment</strong></u>
   In the above step using source setup_install.sh automatically activates the virtual environment.
   For eg: After installation you will see the following.Yet another Important Note: Please activate virtual environment
   using command ". /Users/username/.bp-venv/bin/activate" while running test cases from new shell. Need not activate
   now, since it is already activated.

   (.bp-venv) username@hostname python-test-automation-boilerplate %

   If Virtual Environment has to be activated without the installation step i.e once initial installation is completed
   then following command is used
    ```shell
    #Command Line for MAC
    source /Users/username/.bp-venv/bin/activate

    #Command Line for Windows
    source /Users/username/.bp-venv/Scripts/activate
    ``` 


4. <u><strong>Setup Environment Variables in `.local.env` & `pytest.ini` files</strong></u>
   After successful installation, check and update `env_configs/.local.env` and `pytest.ini` files with relevant details.


5. <u><strong>Appium setup for Mobile apps</strong></u>
    If you are planning to run mobile tests, you need to install Appium server and start it before running the tests.
   Detailed instructions can be found [here](https://appium.io/docs/en/latest/quickstart/)

6. <u><strong>Local Setup for BrowserStack</strong></u>
    If you are planning to run tests on BrowserStack, you need to install BrowserStack Local binary and start it before running the tests.
    Detailed instructions can be found [here](https://www.browserstack.com/local-testing/automate#test-localhost-websites)

7. <u><strong>Local Setup for Docker</strong></u>
    you need to install Docker desktop before running the docker-compose.yml file.
    Detailed instructions can be found [here](https://docs.docker.com/desktop/install/mac-install/)

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

### Executing Test Cases in Local Machine

Users can invoke **`pytest`** command to run test cases locally, with required arguments, as appropriate. Applicable
command line arguments to be passed to `pytest` command:

1. **`--driver=<test-browser-name>`**
   This should be passed **mandatorily** while running UI/selenium test cases. Test Browser name would be`chrome`,
   `firefox` or `edge` or `safari` as per the test needs for local testing. Use `Remote` for testing using Docker/BrowserStack and `Appium` for mobile tests.
2. **`--language=<en|fr|etc.>`**
   Application Language, used in context of UI testing (selenium)
3. **`--capability <individual-capability-value>`**
   Additional individual capabilities can be set using the --capability command line arguments. 
   As an example, for setting the run in a headless mode you will have '--capability headless True'
4. **`--variables <capabilities.json>`**
   To specify multiple capabilities, you can provide a JSON file on the command line using the pytest-variables plugin.
5. **`--tags=<tag name>`**
   This is the gherkin tag name mentioned in the feature file, to filter the tests. Some of the pre-defined sample tags
   that can be used for testing are:
    * `web-tests`
    * `visual-tests`
    * `api-tests`
    * `android-tests`
    * `iOS-tests`
8. **`--gherkin-terminal-reporter`**
   To be used to override the default pytest terminal report, and display in gherkin format (from `pytest-bdd` plugin).
   (Please note, we can't use -n with this argument (* `--gherkin-terminal-reporter`) due to a restriction. so just remove this console printing
   before parallel execution)
9. **`--html=<path-to-html-output> --self-contained-html`**
    To generate html report (from `pytest-html` plugin). To see full log output in the html report avoid `-s` argument in the same time.
10. **`-n <number-of-threads>`**
    To run tests with multiple number of threads in parallel (from `pytest-xdist` plugin).

Sample `pytest` invocation to run all sample ui tests in Chrome browser with 3 threads in parallel:

```shell
pytest -v --driver=Chrome --capability headless True --tags=web-tests -n=1
```

Boilerplate framework is using built-in driver manager to handle the driver binaries for each browser.
There is no need to provide `--driver-path` argument anymore. Selenium lib. will automatically detect the browser version and download required binary driver.
All the drivers will be stored in the `$HOME/.cache/selenium/` folder.
More info: [here](https://www.selenium.dev/blog/2022/introducing-selenium-manager)

### Project Structure

```bash
.
├── /                                         # root directory with project-wide env_configs and folders
├── /app files                                # directory with all android and ios app files/builds
├── /webdriver                                # directory contains all the driver binaries / Browserstack local binary
├── /main                                     # directory contains all the base code (utils, plugins, common steps...) for the framework
├── /env_configs/                             # Configurations related to framework & browser specific
├── /frontend/                                # Project specific files (locators, page objects, step definitions, feature files... etc)
├── /frontend/features/*                      # Test cases written in Gherkin language
├── /frontend/locators/*                      # Web locators for the project
├── /output/                                  # Reports, downloads.... etc)
├── /test_data/                               # All project test data for API, WEB, Mobile tests)
│   ├── /conftest.py                          # Step up and tear down for the tests
│   ├── /setup_install.sh                     # Local Setup script
│   ├── /**.sh                                # Shell scripts for local/CI runs
│   ├── /pytest.ini                           # Project init file
│   ├── /docker-compose.yml                   # To build the docker image
│   ├── /README.md                            # Instructions for the project
│   ├── /requirements.txt                     # Dependencies

```


### Testrail Interaction

Ensure to set/update following details in `env_configs/.local.env` file before interacting with testrail.

> **_IMPORTANT_NOTE:_** If you are updating to project v3.10 or newer make sure to store your TestRail related
> env_configs in '.local.env' file.
> The reason for that is BoilerPlate releases up to v3.8, all TestRail related env_configs were stored in 'pytest.ini' file.
> With current release all TestRail data are stored in the file mentioned below:
>
>.local.env

```
TESTRAIL_EMAIL=[email of user to be used for communication]
TESTRAIL_KEY=[key of user to be used for communication]
TESTRAIL_URL=[URL of TestRail instance]
TESTRAIL_PROJECT_ID=[project id to which the data is sent]
JIRA_PROJECT_KEY=[Jira project key for integration with Jira]
```

1. <strong><u>Export Test Cases</u></strong>

   **To import/update test Scenarios for ALL feature files**
    ```shell
    python -m pytest -v --pytest-testrail-export-test-cases --pytest-testrail-feature-files-relative-path "[path-to-features-dir]"
    ```
   **To import/update test Scenarios for INDIVIDUAL .feature file**
    ```shell
    python -m pytest -v --pytest-testrail-export-test-cases --pytest-testrail-feature-files-relative-path "[DIR_NAME]/[FILE_NAME].feature"
    ``` 

2. <strong><u>Export Test Results</u></strong>

#### For TestRail type 3:
#### Create Test Plan in TestRail

- You have to manually create the test plan in TestRail
    - Naming convention: [JIRA_PROJECT_NAME]_[SPRINT_NAME]_[MARKET] - MARKET only if applied
        - eg: *JIRA_Sprint-1_us* or *JIRA_Regression_us*
- Then add the Test Suite to the test plan (While exporting tests, it automatically creates a testsuite)
- Add a configuration to the test suite and then run below command
    ```shell
    # Mandatory Parameters
    # pytest-testrail-test-plan-id : Testrail Plan ID
    # pytest-testrail-test-configuration-name: Testrail Configuration Name

### Browserstack Interaction

#### Browserstack execution through command line params

Run tests on different browsers using the below command:
```shell
# Usage example for Windows 11 - Chrome
username@hostname python-test-automation-boilerplate % python -m pytest -v --reruns 1 --reruns-delay 1 --gherkin-terminal-reporter --driver Remote --selenium-host '[BS_USERNAME]:[BS_KEY]@hub-cloud.browserstack.com' --capability browserName 'Chrome' --capability os 'Windows' --capability osVersion '11' --capability build 'eucrisahcpcom-qa' --capability browserstack 'True' --tags="p1"
```

For more details on usage, please read through these pages:

* [BS - Test Local Host Websites](https://www.browserstack.com/local-testing/automate#test-localhost-websites)
* [BS - Test Websites Hosted on Private Internal Servers](https://www.browserstack.com/local-testing/automate#test-websites-hosted-private-internal-servers)
* [BS usage with Python](https://www.browserstack.com/automate/python)

Please read BS documentation for more details on configurations:

* https://www.browserstack.com/automate/python
* https://www.browserstack.com/app-automate/appium-python

3. For running parallel test from local in the browserstack you can add **-n [parallel threads value] -> e.g.: "-n '2'"]** to your command.
   -n represents the number of processes to execute the test cases in parallel mode.
   We can also pass "**auto**" to use as many processes as your computer has CPU cores. This can lead to considerable
   speed ups, especially if your test suite takes a noticeable amount of time.

Reference Link - https://pypi.org/project/pytest-xdist/

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

#### Browserstack Mobile

* Upload your Android app (.apk or .aab file) or iOS app (.ipa file) to BrowserStack servers using our REST API. Here is
  an example cURL request to upload the app :

```shell
 curl -u "YOUR_USERNAME:YOUR_ACCESS_KEY" \
-X POST "https://api-cloud.browserstack.com/app-automate/upload" \
-F "file=@/path/to/app/file/Application-debug.apk"
```

* We will receive below sample response which we need to add it in the env_configs/ios_mobile_BS.json and
  env_configs/android_mobile_BS.json file

```shell
{
    "app":"bs://j3c874f21852ba57957a3fdc33f47514288c4ba4"
}
```

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

Command for local run on chrome (also ./local_run_web.sh)
```shell
-v -s  --gherkin-terminal-reporter --driver=Chrome  --html="./output/reports/" --self-contained-html --capability headless True --tags="web_tests" --reruns 1 --reruns-delay 2 -n=2
```
Command for local run on firefox
```shell
-v -s  --gherkin-terminal-reporter --driver=Firefox --capability headless True --html="./output/reports/" --tags="web_tests" --self-contained-html --reruns 1 --reruns-delay 2 -n=1
```
Command for local run on BS with Chrome:
```shell
-v -s  --gherkin-terminal-reporter --driver=Remote --selenium-host '[BS_USERNAME]:[BS_KEY]@hub-cloud.browserstack.com' --variables="env_configs/mac_chrome.json" --html="./output/reports/" --tags="web_tests" --reruns 1 --reruns-delay 2 --self-contained-html
```
Command for local run on local appium server:
```shell
-v -s  --gherkin-terminal-reporter --driver=Appium --html="./output/reports/" --tags="mobile_test and android" --variables="env_configs/android_mobile_local.json" --self-contained-html --reruns 1 --reruns-delay 2
```
Command for local run on BS with IOS:
```shell
-v -s --gherkin-terminal-reporter --disable-warnings --driver=Appium --html="./output/reports/" --selenium-host '[BS_USERNAME]:[BS_KEY]@hub-cloud.browserstack.com' --variables="env_configs/ios_mobile_BS.json" --self-contained-html --tags="mobile_test and ios" --reruns 1 --reruns-delay 2
```

### Html Test Reports
To generate a html report please add following arguments to your command:
```shell
--html=<path_to_report> and --self-contained-html
```
`<path_to_report>` - Project path where the html report will be created.
</br>
For example:
</br>
`--html=./output/reports/`

Example of full command to generate html reports:
```shell
python -m pytest -v --tags="sample-ui-tests" -n=3 --variables=./env_configs/web_local.json --driver=chrome --html=./output/reports/ --self-contained-html
```
Please avoid adding `-s` in the CLI since it will not include any logs in the html report.
</br>
</br>

For GitHub actions please update .yaml including .html file and ./assets folder as in this example.

```
- name: Upload pytest test results
  uses: actions/upload-artifact@v2ł
  with:
    name: pytest-results
    path: |
      ./*.html
      ./assets/
      ./output/
  if: ${{ always() }}
```   
### Allure Reports
by default allure report generates at output/allure/reports at the end of test execution, results are inside /output/allure/results folder. 

### Github Workflows
A list of workflows are added in the .github/workflows folder. e.g
Docker execution, Browserstack execution, Local execution, Mobile execution, Testrail execution, etc.
** about billing of github actions, please check the github documentation. (https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)

Best Practices
---------------------
**Use proper wait predefined step to handle the time needed between action steps**

Avoid using static wait between steps and use instead the predefined step to wait for a specific web element.
In this way we do not hardcode the amount of time needed for an element to appear, we are specifically waiting for it to be displayed.

Therefore, instead of having:

    When I click on 'login > sign-in'
    And I pause for 5 seconds
    And I set text 'username' to field 'login > email'

The right approach is:

    When I click on 'login > sign-in'
    And The element 'login > email' is displayed
    And I set text 'username' to field 'login > email'
Always use these common points:

+ Write clear & concise features using Gherkin, to define behaviour of the system. 
Scenario Structure

+ Organize scenarios into meaningful groups. 
+ Use scenarios to describe test cases / user stories, keeping them focused & atomic
Reusable Steps

+ Identify common steps that can be reused across multiple scenarios & abstract them into reusable step definitions.
Test Data Management
+ Manage test data effectively.
+ Ensure each scenario has necessary data inputs to execute successfully.


Notifications
---------------------
**Slack and MS Teams notifications support is available, we can set webhooks in pytest.ini file**

# Slack Notification arguments
    --slack-webhook-url=https://hooks.slack.com/services/....
    --slack-channel=pytest-test-automation
    --slack-results-url=http://localhost:63342/pytest-automation-boilerplate/output/allure/reports/index.html
# Teams Notification arguments
    --teams-webhook-url=https://moduscreate.webhook.office.com/...
    --teams-results-url=http://localhost:63342/pytest-automation-boilerplate/output/allure/reports/index.html

** Local web driver warnings (if any) resolution for Safari browser on mac**
```shell
/usr/bin/safaridriver --enable
```
For chrome webdriver warning (if any):
```shell
xattr -d com.apple.quarantine $(which chromedriver)
```


Boilerplate update
---------------------
<b>To be decided soon...</b>

<p align="right">(<a href="#about-the-project">back to top</a>)</p>

------------
