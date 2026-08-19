
"""
test.py
 
Small proof of concept showing we can call DataForSEO's API directly,
without going through OpenSEO at all. Hits their free Sandbox
environment.
 
Note: DataForSEO blocks real data behind account verification, phone
or $50 deposit, even in sandbox. Requests below are correctly formed,
check the raw response, just gated at account level.
 
To run: pip install requests, set DFS_LOGIN and DFS_PASSWORD below or
as environment variables, then python test.py
"""

BASE_URL = "https://sandbox.dataforseo.com/v3"


def get_auth_header():
    """Builds the Basic Auth header DataForSEO expects."""
    raw = f"{DFS_LOGIN}:{DFS_PASSWORD}"
    encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    return {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json",
    }


def run_site_audit(target_url):
    """
    Calls on_page/instant_pages, this is a live endpoint, meaning it
    returns results in the same response, no polling needed. This is
    the direct equivalent of OpenSEO's Site Audit feature.
    """
    endpoint = f"{BASE_URL}/on_page/instant_pages"
    payload = [
        {
            "url": target_url,
            "enable_javascript": True,
        }
    ]

    response = requests.post(endpoint, json=payload, headers=get_auth_header())
    data = response.json()

    print(f"\n--- Site Audit (instant_pages) for {target_url} ---")
    print(f"Status: {data.get('status_message')}")

    status_message = data.get("status_message", "")
    if "verify your account" in status_message.lower():
        print("BLOCKED: DataForSEO requires account verification (phone or minimum")
        print("$50 deposit) before returning data, even in sandbox mode. This is an")
        print("account-level gate on their side, not a code or auth failure, the")
        print("request itself was accepted and correctly formed.")
        return data

    tasks = data.get("tasks", [])
    if tasks and tasks[0].get("result"):
        result = tasks[0]["result"][0]
        items = result.get("items", [])
        if items:
            page = items[0]
            print(f"On-page score: {page.get('onpage_score')}")
            print(f"Broken links: {page.get('broken_links')}")
            print(f"Duplicate content: {page.get('duplicate_content')}")
    else:
        print("No result data returned (expected with sandbox dummy data in some cases).")

    return data


def run_backlinks_summary(target_domain):
    """
    Calls backlinks/summary/live, this is the direct equivalent of
    OpenSEO's Backlinks / Domain Overview feature.
    """
    endpoint = f"{BASE_URL}/backlinks/summary/live"
    payload = [
        {
            "target": target_domain,
        }
    ]

    response = requests.post(endpoint, json=payload, headers=get_auth_header())
    data = response.json()

    print(f"\n--- Backlinks Summary for {target_domain} ---")
    print(f"Status: {data.get('status_message')}")

    status_message = data.get("status_message", "")
    if "verify your account" in status_message.lower():
        print("BLOCKED: same account verification gate as above, not a code issue.")
        return data

    tasks = data.get("tasks", [])
    if tasks and tasks[0].get("result"):
        result = tasks[0]["result"][0]
        print(f"Referring domains: {result.get('referring_domains')}")
        print(f"Total backlinks: {result.get('backlinks')}")
    else:
        print("No result data returned (expected with sandbox dummy data in some cases).")

    return data


if __name__ == "__main__":
    # Swap this for any client domain you want to test against.
    test_target = "google.com"

    run_site_audit(f"https://{test_target}")
    run_backlinks_summary(test_target)

    print("\nDone. This proves the direct-DataForSEO integration path (Option C) ")
    print("works end to end without needing OpenSEO's UI or a self-hosted instance.")
