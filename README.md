<!-- TABLE OF CONTENTS -->

# Ask Mate Forum

<summary><h2 style="display: inline-block">Table of Contents</h2></summary>
<ol>
<li>
    <a href="#about-the-project">About The Project</a>
    <ul>
    <li><a href="#built-with">Built With</a></li>
    </ul>
</li>
<li>
    <a href="#getting-started">Getting Started</a>
    <ul>
    <li><a href="#prerequisites">Prerequisites</a></li>
    </ul>
</li>

</ol>

<!-- ABOUT THE PROJECT -->

## About The Project

Ask Mate is a website that functions like a forum. Users can register and ask a question,
answer a question posted by another user or give their opinion on an already posted answer by leaving a comment. Questions
, answers and comments can be edited or deleted by their respective owners.
The owner of a posted question can moderate the answers and comments so only the accepted answers can be seen by other users.

Application features include:

- Main page where a list of all questions can be found. They can also be sorted by certain criteria or by searching through them<br/><br/>
  <img src="https://raw.githubusercontent.com/CozminM/Ask_Mate/master/public/list-page.png" height="500" width="auto">
  <br/>
  <br/>
  <br/>

- Form page for a user to add a question, answer or comment<br/><br/>
  <img src="https://raw.githubusercontent.com/CozminM/Ask_Mate/master/public/add-form.png" height="500" width="auto">
  <br/><br/><br/>

- Individual question page, where users can see the answers and comments approved by the owner of the question,
add their own, upvote/downvote each post. It is also the page where the question owner can moderate and edit the post<br/><br/>
  <img src="https://raw.githubusercontent.com/CozminM/Ask_Mate/master/public/question-page.png" height="500" width="auto">
  <br/><br/><br/>

- Individual user page where someone can see all the posts that user has made and his reputation,
 gained by the number of upvotes he has on his posts.<br/><br/>
  <img src="https://raw.githubusercontent.com/CozminM/Ask_Mate/master/public/user-page.png" height="500" width="auto">
  <br/><br/><br/>

## Future implementation

- Update overall visuals
- Add admin dashboard
- Add blog page for guides


### Built With

- Python
- Python Flask
- HTML
- CSS
- Postgresql

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. Create these environmental variables for the connection to the database: 
   ```
    PSQL_USER_NAME = yourUsername
    PSQL_PASSWORD = yourPassword
    PSQL_HOST = databaseURL
    PSQL_DB_NAME = databaseName
   ```
   
3. Run the SQL script found in the sample_data folder in your database

4. Create a new virtual environment and install the requirements by running the next commands in the project's root folder:

    ```
   virtualenv -p python3 venv
   source venv/bin/activate
   venv/bin/pip3 install -r requirements.txt
   ```
   
5. Open a new browser page at the next address: http://127.0.0.1:5000

6. Make sure your device can run all the technologies in the build section
