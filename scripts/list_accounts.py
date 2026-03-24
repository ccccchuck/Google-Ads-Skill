#!/usr/bin/env python3
"""List accessible Google Ads customer accounts."""
import sys
import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "google ads", "google-ads.yaml")


def main():
    client = GoogleAdsClient.load_from_storage(os.path.abspath(CONFIG_PATH))
    customer_service = client.get_service("CustomerService")

    try:
        accessible_customers = customer_service.list_accessible_customers()
        print("Accessible Customer Resource Names:")
        for name in accessible_customers.resource_names:
            print(f"  {name}")
    except GoogleAdsException as ex:
        print(f"Request failed with status {ex.error.code().name}", file=sys.stderr)
        for error in ex.failure.errors:
            print(f"  Error: {error.message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
