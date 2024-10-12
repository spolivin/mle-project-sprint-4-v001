"""Launches a service of a recommendations application."""
import argparse

import uvicorn

from service.constants import (
    MAIN_APP_PORT,
    RECS_OFFLINE_SERVICE_PORT,
    EVENTS_SERVICE_PORT,
    FEATURES_SERVICE_PORT,
)

# Enumerating services
MAIN_APP = "service.recommendations_service:app"
RECS_APP = "service.recs_offline_service:app"
EVENTS_APP = "service.events_service:app"
FEATURES_APP = "service.features_service:app"

# Enumerating options to launch a specific service
OPTION_MAIN = "main_app"
OPTION_RECS = "recs_store"
OPTION_EVENTS = "events_store"
OPTION_FEATURES = "features_store"

# Help message for options
HELP_MSG = f"Available options: ['{OPTION_MAIN}', '{OPTION_RECS}', '{OPTION_EVENTS}', '{OPTION_FEATURES}']"

# Adding an argument for launching a specific service
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--service-name",
    help="Service name to run. " + HELP_MSG,
)
args = parser.parse_args()

if __name__ == "__main__":
    # Launching main application
    if args.service_name == OPTION_MAIN:
        uvicorn.run(
            app=MAIN_APP,
            port=MAIN_APP_PORT,
        )
    # Launching offline recommendations service
    elif args.service_name == OPTION_RECS:
        uvicorn.run(
            app=RECS_APP,
            port=RECS_OFFLINE_SERVICE_PORT,
        )
    # Launching service for storing events
    elif args.service_name == OPTION_EVENTS:
        uvicorn.run(
            app=EVENTS_APP,
            port=EVENTS_SERVICE_PORT,
        )
    # Launching a service for online recommendations
    elif args.service_name == OPTION_FEATURES:
        uvicorn.run(
            app=FEATURES_APP,
            port=FEATURES_SERVICE_PORT,
        )
    # Processing 'no arguments' / 'invalid arguments' cases
    else:
        if args.service_name is None:
            print("No service specified" + f"\n{HELP_MSG}")
        else:
            print(f"Service name '{args.service_name}' is invalid" + f"\n{HELP_MSG}")
