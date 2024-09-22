from fastapi import FastAPI, HTTPException
from functions import calculate_difference, events_count, repo_info

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Welcome to the API. Here are the available endpoints:",
        "endpoints": {
            "Endpoint 1": "/pulls-delay/{owner}/{repo}",
            "Endpoint 2": "/events/{offset}",
            "Endpoint 3": "/repo-stats/{owner}/{repo}"
        }
    }


@app.get("/pulls-delay/{owner}/{repo}", status_code=200)
def pulls_delay(owner: str, repo: str):
    """average time between pull requests for a given repository"""
    res = calculate_difference(owner, repo)
    if not res:
        raise HTTPException(status_code=404, detail="No pull requests for this repository")
    return res


@app.get("/events/{offset}", status_code=200)
def events(offset: int):
    """total number of events grouped by the event type for a given offset. only WatchEvent, PullRequestEvent and
    IssuesEvent"""
    return events_count(offset)


@app.get("/repo-stats/{owner}/{repo}", status_code=200)
def repo_stats(owner: str, repo: str):
    """most frequent event and most frequent user for a given repository"""
    res = repo_info(owner, repo)
    if not res:
        raise HTTPException(status_code=404, detail="No events for this repository")
    return res
