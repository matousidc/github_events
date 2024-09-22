# Assignment

### How to run:

- git clone https://github.com/matousidc/github_events.git
- (create and activate venv)
- input YOUR GitHub token into prepared '.env_example' file and rename it to '.env'.

  Contents of the file should look something like this:
- ``````
  GITHUB_TOKEN=ghp_sdfsdfsdf62646sdf56mnmBJ1QQluasffghFdES
- pip install -r requirements.txt
- fastapi dev

### Endpoints:

- /pulls-delay/{owner}/{repo} - returns the average time between pull requests for a given repository
- /events/{offset} - returns number of events grouped by the event type for a given offset( last x minutes)
- /repo-stats/{owner}/{repo} - returns most frequent event and most frequent user for a given repository

### Comments:

- used python 3.11
- GitHub api is paginated, so functions are making requests in loops until last page is reached or a condition is met
- from GitHub docs "Only events created within the past 90 days will be included", so some repositories may show no
  events

### Context diagram:

![Diagram](c4model.png)