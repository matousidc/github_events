import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException

load_dotenv()


def api_call(path: str) -> requests.Response:
    """Calling the GitHub API"""
    url = f"https://api.github.com/{path}"
    token = os.getenv('GITHUB_TOKEN')
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Bad request, probably wrong owner or repository name")
    return response


def calculate_difference(owner: str, repo: str) -> dict | None:
    """Iterates over all available events for a given repository and calculates average time between pull requests"""
    pulls_times = []
    i = 1
    while True:
        resp = api_call(f"/repos/{owner}/{repo}/events?per_page=100&page={i}")
        pulls_times += [datetime.fromisoformat(x['created_at']) for x in resp.json() if x['type'] == 'PullRequestEvent']
        if 'next' not in resp.links.keys():
            break
        i += 1
    if not pulls_times:
        return None
    time_differences = [(pulls_times[i] - pulls_times[i - 1]).total_seconds() for i in range(1, len(pulls_times))]
    average_time_difference = sum(time_differences) / len(time_differences)
    return {"average_time_difference_seconds": abs(round(average_time_difference))}


def events_count(offset: int) -> dict:
    """Iterates the events, counting the number of specified events, stops when reaches offset minutes ago"""
    i = 1
    counts = {x: 0 for x in ['WatchEvent', 'PullRequestEvent', 'IssuesEvent']}
    while True:
        resp = api_call(f"events?per_page=100&page={i}")
        for x in resp.json():
            if datetime.fromisoformat(x['created_at']).timestamp() < (
                    datetime.utcnow() - timedelta(minutes=offset)).timestamp():
                return counts
            if x['type'] in counts.keys():
                counts[x['type']] += 1
        if 'next' not in resp.links.keys():
            break
        i += 1
    return counts


def repo_info(owner: str, repo: str) -> dict | None:
    """Calculates the most frequent event and most frequent user for a given repository"""
    stats = {'events': {}, 'users': {}}
    i = 1
    while True:
        resp = api_call(f"/repos/{owner}/{repo}/events?per_page=100&page={i}")
        for x in resp.json():
            if x['type'] in stats['events'].keys():
                stats['events'][x['type']] += 1
            else:
                stats['events'][x['type']] = 1
            if x['actor']['login'] in stats['users'].keys():
                stats['users'][x['actor']['login']] += 1
            else:
                stats['users'][x['actor']['login']] = 1
        if 'next' not in resp.links.keys():
            break
        i += 1
    if not stats['events'] or not stats['users']:
        return None
    return {"most_frequent_event": max(stats['events'], key=stats['events'].get),
            "most_frequent_user": max(stats['users'], key=stats['users'].get)}
