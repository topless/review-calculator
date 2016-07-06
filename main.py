#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import sys
import json
import urllib2
from datetime import datetime

# NOTE: The key should be stored in the database and not in the code.
APIKEY = 'tiNFg9zDKRWXaIpI8pPyWbXd4ACa9ZDt'

# MAX_RESULTS: Limit is the number of total reviews we will use.
MAX_RESULTS = 300

# PER_PAGE: How many results we will fetch on each request
PER_PAGE = 100


def lambda_handler(event, context):
    if 'domain' not in event:
        return {'error': 'Provide a domain in your request'}

    business_unit = get_business_unit(event['domain'])
    if 'id' not in business_unit:
        return business_unit

    business_reviews = get_business_reviews(business_unit['id'])
    if not len(business_reviews):
        return {'error': 'No business reviews found'}

    result = {
        'domain': event['domain'],
        'result': calculate_mean(business_reviews)
    }
    print("Result {}".format(result))
    return result


def get_business_unit(domain):
    api_find_url = 'https://api.trustpilot.com/v1/business-units/find'
    url = "{}?&name={}&apikey={}".format(api_find_url, domain, APIKEY)
    print("Fetching {}".format(url))
    try:
        response = urllib2.urlopen(url)
        return json.load(response)
    except urllib2.HTTPError as e:
        print(e.code)
        return json.loads(e.read())


def get_business_reviews(business_id):
    """We are using the provided next-page urls to get results up to MAX_RESULTS
    orderBy param is set default to createdat.desc, nothing to do there.
    """
    reviews = []
    api_reviews_url = "https://api.trustpilot.com/v1/business-units"
    url = "{}/{}/reviews?apikey={}&perPage={}&orderBy=createdat.asc".format(
        api_reviews_url, business_id, APIKEY, PER_PAGE
    )

    while len(reviews) < MAX_RESULTS:
        try:
            print("Fetching {}".format(url))
            response = urllib2.urlopen(url)
            data = json.load(response)
            reviews += list(data['reviews'])
            next_url = get_next_url(data)
            url = "{}&apikey={}".format(next_url, APIKEY)
            # Break if we have in total less than MAX_RESULTS
            if not next_url:
                break
        except urllib2.HTTPError as e:
            print(e.code)
            return json.loads(e.read())
    return reviews


def calculate_mean(reviews):
    weight = 1
    weights_sum = 0
    stars_sum = 0

    iter_reviews = iter(reviews)
    oldest = next(iter_reviews)
    oldest_date = datetime.strptime(oldest['createdAt'][:10], "%Y-%m-%d")
    stars_sum = weight * int(oldest['stars'])

    for review in iter_reviews:
        review_date = datetime.strptime(review['createdAt'][:10], "%Y-%m-%d")
        weight = abs((oldest_date - review_date).days) + 1
        weights_sum += weight
        stars_sum += weight * int(review['stars'])

    mean_stars = stars_sum / float(weights_sum)
    return mean_stars


def get_next_url(data):
    for link in data['links']:
        if link['rel'] != 'next-page':
            continue
        return link['href']


if __name__ == '__main__':
    # Cheating for local debug :)
    args = {'domain': sys.argv[1]}
    lambda_handler(args, None)
