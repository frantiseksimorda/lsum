# coding: utf8

from user_agents import parse

def stringList(list_of_tuples_containig_one_string):

    returning = []

    for tup in list_of_tuples_containig_one_string:
        returning.append(tup[0])

    return returning


def activeBrowser(meta_info):

    meta = parse(meta_info.META['HTTP_USER_AGENT'])
    return (meta.browser.family).lower()

