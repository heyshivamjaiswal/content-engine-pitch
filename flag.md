"""
sandbox.py
 
Small proof of concept showing we can call DataForSEO's API directly,
without going through OpenSEO at all. Hits their free Sandbox
environment, no real credit card needed, just a free DataForSEO
account.
 
Note from testing: DataForSEO gates real data behind account
verification, phone verification or a minimum $50 deposit, even for
sandbox calls. Requests below are correctly authenticated and formed,
verify that from the raw response printed, but data is blocked at
that account gate. Two ways around this if we move forward on this
integration: use DataForSEO's official Python SDK (dataforseo_client
on pip) instead of raw requests, same account gate applies but worth
knowing it exists as an alternative to hand-rolled requests, or their
Cloudflare-hosted deployment path for OpenSEO itself, which may route
around some of this depending on how billing is set up there. Neither
was tested here, just flagging as next options if we hit this wall
again with a production account.
 
To run: pip install requests, set DFS_LOGIN and DFS_PASSWORD below or
as environment variables, then python sandbox.py
"""
