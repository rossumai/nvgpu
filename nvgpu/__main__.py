import argparse
import time

import nvgpu
from nvgpu.list_gpus import pretty_list_gpus

def parse_args():
    parser = argparse.ArgumentParser(description='NVIDIA GPU tools.')
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    parser_available = subparsers.add_parser('available')
    parser_available.add_argument('-l', '--limit', default=None, type=int,
        help='Max number of GPUs')
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('-l', '--loop', nargs='?', const=1, type=float,
        help='Probe until Ctrl+C at specified second interval.')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'available':
        gpus = nvgpu.available_gpus()
        if args.limit:
            gpus = gpus[:args.limit]
        print(','.join(gpus))
    elif args.command == 'list':
        if args.loop:
            while True:
                try:
                    pretty_list_gpus()
                    time.sleep(args.loop)
                except KeyboardInterrupt:
                    break
        else:
            pretty_list_gpus()


if __name__ == '__main__':
    main()
