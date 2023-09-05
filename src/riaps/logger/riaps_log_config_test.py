#!/usr/bin/python3
'''
Script to test app log config file

Created on Oct 20, 2022

Arguments
-f (or --file) FILE : Path to the file that will be used to construct the loggers
@author: riaps
'''

import argparse
import logging.config
import time
import riaps.utils.spdlog_setup as spdlog_setup


def test_loggers(loggers, msg):
    for logger in loggers:
        # level = loggers[logger].getEffectiveLevel()
        # level_name = logging.getLevelName(level)
        # print(f"logger: {logger} level: {level_name}")
        loggers[logger].info(msg)
    print("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file", default="riaps-log.conf")
    parser.add_argument("-s", "--spd", action='store_true')
    args = parser.parse_args()

    if args.spd:
        loggers = spdlog_setup.from_file(args.file)
    else:
        logging.config.fileConfig(args.file)
        loggers = logging.root.manager.loggerDict
        root_logger = logging.getLogger()  # get the root logger
        for logger in loggers:
            loggers[logger] = logging.getLogger(logger)
        loggers["root"] = root_logger

    for i in range(10):
        test_loggers(loggers, f"message: {i}")
        time.sleep(1)

if __name__ == '__main__':
    main()


