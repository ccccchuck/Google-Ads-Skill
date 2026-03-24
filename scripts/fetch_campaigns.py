#!/usr/bin/env python3
"""Fetch campaign performance data from Google Ads API."""
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


def main(date_range="LAST_7_DAYS", output_format="text"):
    client = GoogleAdsClient.load_from_storage(os.path.abspath(CONFIG_PATH))
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.ctr,
            metrics.conversions,
            metrics.cost_micros,
            metrics.average_cpc
        FROM campaign
        WHERE segments.date DURING {date_range}
            AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = CUSTOMER_ID
    search_request.query = query

    results = ga_service.search(request=search_request)

    rows = []
    for row in results:
        entry = {
            "campaign": row.campaign.name,
            "status": row.campaign.status.name,
            "channel": row.campaign.advertising_channel_type.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "ctr": round(row.metrics.ctr * 100, 2),
            "conversions": row.metrics.conversions,
            "cost": round(row.metrics.cost_micros / 1_000_000, 2),
            "avg_cpc": round(row.metrics.average_cpc / 1_000_000, 2),
        }
        rows.append(entry)

    if output_format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(f"--- 广告系列表现 ({date_range}) ---")
        print(f"{'Campaign':<45} {'Status':<10} {'Clicks':>6} {'Impr':>6} {'CTR':>7} {'Conv':>6} {'Cost':>8} {'CPC':>7}")
        print("-" * 105)
        total_cost = 0
        total_clicks = 0
        total_conv = 0
        for r in rows:
            print(f"{r['campaign']:<45} {r['status']:<10} {r['clicks']:>6} {r['impressions']:>6} {r['ctr']:>6.2f}% {r['conversions']:>6.1f} ${r['cost']:>7.2f} ${r['avg_cpc']:>6.2f}")
            total_cost += r['cost']
            total_clicks += r['clicks']
            total_conv += r['conversions']
        print("-" * 105)
        print(f"{'Total':<45} {'':>10} {total_clicks:>6} {'':>6} {'':>7} {total_conv:>6.1f} ${total_cost:>7.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch campaign performance from Google Ads API.")
    parser.add_argument("--date_range", default="LAST_7_DAYS", choices=VALID_DATE_RANGES, help="Date range")
    parser.add_argument("--format", dest="output_format", default="text", choices=["text", "json"], help="Output format")
    args = parser.parse_args()

    try:
        main(date_range=args.date_range, output_format=args.output_format)
    except GoogleAdsException as ex:
        print(f'Request failed with status "{ex.error.code().name}":', file=sys.stderr)
        for error in ex.failure.errors:
            print(f'  Error: {error.message}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
