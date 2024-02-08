from BUS_LIB.Analytics.speed_analytics import count_passed
from BUS_LIB.Analytics.speeding_map import show_speed_map
import argparse

parser = argparse.ArgumentParser(description='Analyzing speed data and optionally displaying the result.')
parser.add_argument('timeframe_name', type=str,
                    help='Common name of all file to analyze. '
                         'All names of files should be the same except the last symbol. '
                         'The last symbol of all files should be a number. '
                         'The number of the first file should be 1. All next files '
                         'should have numbers greater by one from the previous one.')
parser.add_argument('directory_name', type=str,
                    help='Path to a directory where "timeframe" files are being stored.')
parser.add_argument('--number_of_timeframes', type=int, default=60,
                    help='Number of "timeframe_name" files to analyze. Default value: 60.')
parser.add_argument('--to_file', type=bool, default=False,
                    help='Allows to save result of analyzing to file. Default value: False.')
parser.add_argument('--file_directory', type=str, default='DATA/BUS_SPEEDING',
                    help='Path to a file where the result is going to be saved, if "to_file" is True.'
                         'Default value: "DATA/BUS_SPEEDING"')
parser.add_argument('--display_map', type=bool, default=False,
                    help='If the result was saved to "file_directory" file, displays a map based on the result.')

args = parser.parse_args()

if args.display_map is True and args.to_file is False:
    parser.error('The "Display_map" argument requires "to_file" to be equal to True.')

print("The number of buses that exceeded the speed limit is " +
      str(count_passed(tag=args.timeframe_name, storage=args.directory_name, length=args.number_of_timeframes,
                       to_file=args.to_file, file_name=args.file_directory)) + ".")

if args.display_map:
    show_speed_map(name_file=args.file_directory)
