from BUS_LIB.Data_gathering.stop_data import get_bus_data
import argparse


parser = argparse.ArgumentParser(description='Downloads Warsaw bus schedule.')
parser.add_argument('directory_name', type=str,
                    help='Path to a directory where schedule will be stored.')
args = parser.parse_args()

get_bus_data(args.directory_name)
