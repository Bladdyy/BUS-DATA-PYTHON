from BUS_LIB.Analytics.stop_analytics import bus_late
import argparse

parser = argparse.ArgumentParser(description='Analyzing stop arrival data and optionally displaying the result.')
parser.add_argument('--bus_schedule', type=str, default="../DATA/BUS_STOP_TIMETABLE",
                    help='Path to a global bus schedule. Default value "../DATA/BUS_STOP_TIMETABLE".')
parser.add_argument('timeframe_name', type=str,
                    help='Common name of all files to analyze. '
                         'All names of files should be the same except the last symbol. '
                         'The last symbol of all files should be a number. '
                         'The number of the first file should be 1. All next files '
                         'should have numbers greater by one from the previous one.')
parser.add_argument('directory_name', type=str,
                    help='Path to a directory where "timeframe" files are being stored.')
parser.add_argument('--number_of_timeframes', type=int, default=60,
                    help='Number of "timeframe_name" files to analyze. Default value: 60.')
parser.add_argument('--visualization', type=bool, default=False,
                    help='Allows to visualize percentage of late arrivals for each bus line on a scatter plot. '
                         'Default value: False.')

args = parser.parse_args()


result = bus_late(table=args.bus_schedule, tag=args.timeframe_name, storage=args.directory_name,
                  length=args.number_of_timeframes, visualize=args.visualization)
print("Buses were on time on", result[0], "stops out of", result[1], "stops.")
