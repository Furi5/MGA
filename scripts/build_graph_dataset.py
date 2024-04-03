
# generate hERG dataset
import os
import sys
import argparse
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取上一级目录的绝对路径
parent_dir = os.path.dirname(current_dir)

# 将上一级目录添加到 sys.path 中
sys.path.append(parent_dir)

from utils import build_dataset


def main(args):
        print(args)
        build_dataset.built_data_and_save_for_splited(
                origin_path=args.input_csv,
                save_path=args.output_bin,
                group_path=args.output_csv,
                task_list_selected=None
                )

if __name__ == '__main__':
        parser = argparse.ArgumentParser(description="An example program demonstrating argparse")
        parser.add_argument("--task", "-t",help="Input file path")
        args = parser.parse_args()
        
        args.input_csv = f'./data/tox_data_v1/{args.task}/{args.task}.csv'
        args.output_bin = f'./data/tox_data_v1/{args.task}/{args.task}.bin'
        args.output_csv = f'./data/tox_data_v1/{args.task}/{args.task}_group.csv'
        print(args)
        print(args.input_csv)
        main(args)


