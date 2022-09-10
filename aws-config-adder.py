import configparser
import argparse
import os
from os.path import expanduser

DEFAULT_SOURCE_PROFILE = "<name_of_source_profile>"
DEFAULT_ROLE_ARN = "arn:aws:iam::{}:role/<name_of_the_role>"
DEFAULT_REGION = "us-east-1"

"""
Typical AWS Config section looks like this
[profile <name_of_config>]
region = <region_name>
role_arn = arn:aws:iam::<000000000000>:role/<name_of_the_role>
source_profile = <source_profile>
"""


def main(command_line_args):
    # get the path to the user's home directory
    user_home = expanduser("~")

    # load their .aws/config file
    config = configparser.ConfigParser()
    config.read([str(user_home + "/.aws/config")])

    if not command_line_args.name:
        config_name = input("What is the name of the aws config you want to create?")
    else:
        config_name = command_line_args.name

    if not command_line_args.region:
        region_name = input("What is the region for the config?")
    else:
        region_name = command_line_args.region

    if not command_line_args.account:
        account_number = input("What is the account number?")
    else:
        account_number = command_line_args.account

    config["profile {}".format(config_name)] = {
        "region": region_name,
        "role_arn": DEFAULT_ROLE_ARN.format(account_number),
        "source_profile": DEFAULT_SOURCE_PROFILE
    }

    # Make a quick backup of the config file before we overwrite it.
    os.popen('cp {} {}'.format(str(user_home + "/.aws/config"), str(user_home + "/.aws/config.bak")))

    with open(str(user_home + "/.aws/config"), 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    """
    Main kick off of the script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default=None)
    parser.add_argument('-r', '--region', default=os.environ.get('AWS_REGION', DEFAULT_REGION))
    parser.add_argument('-a', '--account', default=None)
    args = parser.parse_args()

    main(command_line_args=args)
