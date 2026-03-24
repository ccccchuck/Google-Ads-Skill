#!/usr/bin/env python3
"""Fetch search term report from Google Ads API."""
import argparse
import json
import sys
import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "google ads", "google-ads.yaml")
CUSTOMER_ID = "6646561021"

VALID_DATE_RANGES = [
    "TODAY", "YESTERDAY", "LAST_7_DAYS", "LAST_14_DAYS",
    "LAST_30_DAYS", "LAST_90_DAYS", "THIS_MONTH", "LAST_MONTH"
]


def main(date_range="LAST_7_DAYS", limit=30, output_format="text"):
    client = GoogleAdsClient.load_from_storage(os.path.abspath(CONFIG_PATH))
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            search_term_view.search_term,
            campaign.name,
            ad_group.name,
            search_term_view.status,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.conversions,
            metrics.cost_micros
        FROM search_term_view
        WHERE segments.date DURING {date_range}
        ORDER BY metrics.clicks DESC
        LIMIT {limit}"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = CUSTOMER_ID
    search_request.query = query

    results = ga_service.search(request=search_request)

    rows = []
    for row in results:
        entry = {
            "search_term": row.search_term_view.search_term,
            "campaign": row.campaign.name,
            "ad_group": row.ad_group.name,
            "status": row.search_term_view.status.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": round(row.metrics.ctr * 100, 2),
            "conversions": row.metrics.conversions,
            "cost": round(row.metrics.cost_micros / 1_000_000, 2),
        }
        rows.append(entry)

    if output_format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(f"--- 搜索词报告 ({date_range}) ---")
        print(f"{'Search Term':<50} {'Campaign':<35} {'Clicks':>6} {'Impr':>6} {'CTR':>7} {'Conv':>6} {'Cost':>8}")
        print("-" * 128)
        for r in rows:
            print(f"{r['search_term']:<50} {r['campaign']:<35} {r['clicks']:>6} {r['impressions']:>6} {r['ctr']:>6.2f}% {r['conversions']:>6.1f} ${r['cost']:>7.2f}")
        print(f"\nTotal: {len(rows)} search terms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch search term report from Google Ads API.")
    parser.add_argument("--date_range", default="LAST_7_DAYS", choices=VALID_DATE_RANGES, help="Date range")
    parser.add_argument("--limit", type=int, default=30, help="Max results")
    parser.add_argument("--format", dest="output_format", default="text", choices=["text", "json"], help="Output format")
    args = parser.parse_args()

    try:
        main(date_range=args.date_range, limit=args.limit, output_format=args.output_format)
    except GoogleAdsException as ex:
        print(f'Request failed with status "{ex.error.code().name}":', file=sys.stderr)
        for error in ex.failure.errors:
            print(f'  Error: {error.message}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
