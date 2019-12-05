import sys
import logging

import ccapi

logger = logging.getLogger("ccapi")
logger.setLevel(logging.DEBUG)

def main():
    client = ccapi.Client()
    client.auth(email = "test@cellcollective.org", password = "test")

    me     = client.me()

    models = client.get("model", filters = { "user": me }, size = sys.maxsize)
    for model in models:
        model.delete()

if __name__ == "__main__":
    main()