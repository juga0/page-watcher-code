#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FIXME: move this file outside scrapy project?
from page_watcher import read_yaml, commit, create_policy_file_path, \
    CONFIG_PATH, RULES_PATH, POLICIES_DATA_REPO_PATH

import logging

logger = logging.getLogger(__name__)


def main():

    config = read_yaml(CONFIG_PATH)
    # FIXME: obtain last commit?

    rules = read_yaml(RULES_PATH)
    # FIXME: obtain last commit?

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())

    for rule in rules:
        policies_path = create_policy_file_path(rule)
        process.crawl(
            'policies', policies_path=policies_path, url=rule['url'],
            xpath=rule['xpath'])
    logger.debug('starting crawler')
    # the script will block here until the crawling is finished
    process.start()

    commit(POLICIES_DATA_REPO_PATH)
    # FIXME: push to remote repo

if __name__ == "__main__":
    main()
