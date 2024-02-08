from BUS_LIB.Data_gathering.data_getter import get_pos_data
import argparse


parser = argparse.ArgumentParser(description='Downloading data about bus locations during specific timeframe.')
parser.add_argument('--batch', type=int, default=60,
                    help='The amount of timeframes to download. Default value: 60.')
parser.add_argument('timeframe_name', type=str,
                    help='Common name of all files to analyze. '
                         'All timeframes are going to be saved with the same file name,'
                         'except the last symbol. The last symbol is going to be a number (file index).'
                         'Indexes are being numbered from 1 to "batch".')
parser.add_argument('directory_name', type=str,
                    help='Path to a directory where "timeframe" files are going to be stored.')
parser.add_argument('--consistency', type=int, default=60,
                    help='Length between two consecutive timeframe downloads measured in seconds. Default value: 60.')

args = parser.parse_args()

get_pos_data(batches=args.batch, tag=args.timeframe_name, storage=args.directory_name, consistency=args.consistency)
