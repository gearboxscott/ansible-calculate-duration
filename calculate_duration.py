#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: calculate_duration

short_description: This module to add time on end of the passed in date and time.

version_added: "1.0.0"

description: This module to add time on end of the passed in date and time.

options:
    calculate_duration:
      date: This is date and time to start appending duration (fmt: %Y-%m-%d %H:%M:%S )
      duration: Number of units to add. (int)
      units: Number of some unit to add to the passed in date and time (string).
             Choices: days, seconds, microseconds, milliseconds, minutes, hours, weeks  
             sample: 'units: hours'

author:
    - Scott Parker (@gearboxscott)
'''

EXAMPLE = r'''
# Calculate the End of the Patching Window
- name: Calculate the End of the Patching Window
  calculate_duration:
    date: '2021-02-19 07:00'
    duration: 20
    units: hours
  register: patch_window_close

Output Produced:

{
    "changed": true,
    "date_out": "2021-02-20",
    "time_out": "03:00",
    "full_out": "2021-02-20 03:00",
    "invocation": {
        "module_args": {
            "date": "2021-02-19 07:00:00",
            "duration": 20,
            "units": "hours"
        }
    },
    "_ansible_no_log": false
}

'''

RETURN = r'''
date_out:
    description: Incremented Date
    type: string
    returned: %Y-%m-%d
    sample: '2021-02-19'
time_out:
    description: Incremented Time associated with date_out date
    type: string
    returned: %H:%M
    sample: '13:00'
full_out:
    description: Incremented Date and Time together
    type: string
    returned: %Y-%m-%d %H:%M
    sample: '2021-02-19 13:00'
'''

from ansible.module_utils.basic import *
from datetime import date, datetime, timedelta, time
from sys import argv

def main():

    fields = {
        "date": { "required": True, "type": "str" },
        "duration": { "required": True, "type": "int" },
        "units": {
            "type": "str",
            "choices": [ 'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks' ],
            "default": "hours"
        },
    }

    module = AnsibleModule( argument_spec=fields )

    format_date_in = "%Y-%m-%d %H:%M:%S"
    formatted_date = datetime.strptime( module.params[ 'date' ], format_date_in )

    if module.params[ 'units' ] == 'days':
        end_time = formatted_date + timedelta( days=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'seconds':
        end_time = formatted_date + timedelta( seconds=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'microseconds':
        end_time = formatted_date + timedelta( microseconds=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'milliseconds':
        end_time = formatted_date + timedelta( milliseconds=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'minutes':
        end_time = formatted_date + timedelta( minutes=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'hours':
        end_time = formatted_date + timedelta( hours=module.params[ 'duration' ] )
    elif module.params[ 'units' ] == 'weeks':
        end_time = formatted_date + timedelta( weeks=module.params[ 'duration' ] )
    else:
        module.fail_exit( msg="Units of " + module.params[ 'units' ] + " is Invalid!" ) 

    format_full_out = "%Y-%m-%d %H:%M" 
    format_date_out = "%Y-%m-%d"
    format_time_out = "%H:%M"

    date_out = end_time.strftime( format_date_out )
    time_out = end_time.strftime( format_time_out )
    full_out = end_time.strftime( format_full_out )

    module.exit_json( changed=True, date_out=date_out, time_out=time_out, full_out=full_out ) 

if __name__ == '__main__':
    main()
