#!/usr/bin/env python3
"""Obtain a refresh token for the Google Ads API via OAuth2."""
import argparse
import sys

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]


def main(client_secrets_path):
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, scopes=SCOPES)
    credentials = flow.run_local_server(port=0)

    print(f"Access token: {credentials.token}")
    print(f"Refresh token: {credentials.refresh_token}")
    print(f"Client ID: {credentials.client_id}")
    print(f"Client Secret: {credentials.client_secret}")
    print("\n请将上方的 Refresh token 更新到 google ads/google-ads.yaml 文件的 refresh_token 字段中。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Obtain a refresh token for Google Ads API.")
    parser.add_argument("--client_secrets_path", required=True, help="Path to client_secret.json")
    args = parser.parse_args()
    main(args.client_secrets_path)
