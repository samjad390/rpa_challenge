# RPA Challenge

In this repository [rpaframework](https://rpaframework.org/releasenotes.html) with python is used to automate process of scraping.
### Features

1. **Scrap data from** [ITDashboard Website](https://itdashboard.gov/)
2. It will make excel of agencies and there investment from [itdashboard.gov](https://itdashboard.gov/) home page.
3. It will open specific agency home page and scrap data from its Unique Investment Identifier(**UII**) table.
4. It will download the pdf it there is any linked with **UII** and match the name and UII in table with pdf section A name and UII.  
5. This repository can be tested at [robocorp](https://cloud.robocorp.com/).
6. All downloaded **PDFs** and generated **EXCEL** Files are stored in **output** folder.

## Installation Requirements

1. [rpaframework](https://rpaframework.org/releasenotes.html)

### Instructions to setup

1. Sign up at [robocorp](https://cloud.robocorp.com/taskoeneg/task/robots) create a bot and add link of this repository to bot.
2. **ALTERNATIVE**: you can upload .zip folder of this repository to the bot.
3. Add Assistant and link it to the bot from [robocorp assistants](https://cloud.robocorp.com/taskoeneg/task/assistants). 
4. Download Assistant app by clicking on **Download Robocorp Assistant App**
5. Link your workspace in assistant app and install bot assistant.
6. Bot will perform the task and store the output in output folder.


## Bot Structure
###challenge.py
challenge.py contains class ItDashboard in which functions to scrap the agencies from [IT-Dashboard](https://itdashboard.gov/) home page store them in excel named **Agencies.xlsx** in to output folder and scrap **UII** table of specific agency store its pdfs and whole table in output folder.


### conda.yaml
environment configuration to set up bot [rpaframework]() dependencies.

### robot.yaml
Configuration for robocorp to open the challenge.py and perform tasks in it. [conda.yaml]().

