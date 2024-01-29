<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
</p>
<p align="center">
    <h1 align="center">TRAVEL-GUIDE</h1>
</p>
<p align="center">
    <em>Discover the world with your personal guide!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/younghch/travel-guide?style=default&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/younghch/travel-guide?style=default&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/younghch/travel-guide?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/younghch/travel-guide?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running travel-guide](#-running-travel-guide)
> - [ License](#-license)

---

##  Overview

The travel-guide project is a Telegram bot that provides users with a personalized audio guide for tourist spots based on their current location. The bot utilizes the Google Places API to retrieve nearby places and offers two modes of guidance: Guide Right Infront and Guide Nearby Places. In the Guide Right Infront mode, the bot gives detailed descriptions of cultural and historical sites, including interesting stories or legends. In the Guide Nearby Places mode, it displays a list of nearby places and allows users to select a specific place to receive a comprehensive guide. The bot also supports selecting different versions of the GPT language model for generating the guide. Overall, the project provides users with convenient and informative guidance for exploring tourist attractions.

---

##  Features


---

##  Repository Structure

```sh
└── travel-guide/
    ├── Dockerfile
    ├── bot.py
    ├── core
    │   ├── gpt.py
    │   └── places.py
    └── requirements.txt
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [requirements.txt](https://github.com/younghch/travel-guide/blob/master/requirements.txt) | This code snippet indicates the list of dependencies needed for the repository, essentially a Travel Guide which likely functions as a chatbot providing travel recommendations. These dependencies include OpenAI for generating responses, python-telegram-bot for communication over Telegram, and Requests for making HTTP requests; all vital for the bot's operation.                                                                                                                  |
| [Dockerfile](https://github.com/younghch/travel-guide/blob/master/Dockerfile)             | This Dockerfile allows for the containerization of the travel-guide app. It sets up the Python environment, installs dependencies from the requirements file, copies the source code into the container, and starts the bot upon container launch.                                                                                                                                                                                                                                           |
| [bot.py](https://github.com/younghch/travel-guide/blob/master/bot.py)                     | The `bot.py` file powers a location-based Telegram bot. The bot provides interactive travel guide services to users, suggesting nearby places and giving detailed guides based on user's location data. It offers options to choose the guide mode (places right infront or nearby places) and the generation model version (GPT-3.5 or GPT-4) for customized responses. It utilizes core functionalities defined in other modules for place recommendations and generation of guided texts. |

</details>

<details closed><summary>core</summary>

| File                                                                             | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---                                                                              | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| [places.py](https://github.com/younghch/travel-guide/blob/master/core/places.py) | The code in core/places.py serves as a critical component for the travel-guide bot. It uses Google Places API to fetch details of popular or historical points of interest near a user-provided location. It defines a list of tourist and historical place types, creates and sends a query to Google via a POST request, and retrieves place names and addresses in response. This module significantly contributes to the bot's ability to recommend travel destinations.                                              |
| [gpt.py](https://github.com/younghch/travel-guide/blob/master/core/gpt.py)       | The core/gpt.py module is an integral part of the travel-guide repository. Its key functions are to generate content for a travel guide application by leveraging the capabilities of the GPT-3 and GPT-4 models from OpenAI. The code creates guided tours in Korean, presenting detailed narratives about various places. It has two different narration-types: a general overview of multiple places and a detailed guide for a specific location. The module utilizes structured prompts to guide the AI's responses. |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version x.y.z`

###  Installation

1. Clone the travel-guide repository:

```sh
git clone https://github.com/younghch/travel-guide
```

2. Change to the project directory:

```sh
cd travel-guide
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

###  Running travel-guide

Use the following command to run travel-guide:

```sh
python main.py
```

###  Tests

To execute tests, run:

```sh
pytest
```

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

[**Return**](#-quick-links)

---
