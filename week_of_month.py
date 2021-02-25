#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import *
from math import ceil
from datetime import date, datetime, timedelta, time

def main():
    """ Returns the week of the month for the specified date.
    """

    fields = {}

    module = AnsibleModule( argument_spec=fields )

    changed = False
    dt = datetime.today()
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    module.exit_json( changed=True, week_of_month=int(ceil(adjusted_dom/7.0)) )

if __name__ == '__main__':
    main()