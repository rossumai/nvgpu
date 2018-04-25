import argparse

import nvgpu

def parse_args():
    parser = argparse.ArgumentParser(description='NVIDIA GPU tools.')
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    parser_predict = subparsers.add_parser('available')
    parser_predict.add_argument('-l', '--limit', default=None, type=int,
        help='Max number of GPUs')

    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == 'available':
        gpus = nvgpu.available_gpus()
        if args.limit:
            gpus = gpus[:args.limit]
        print(','.join(gpus))

if __name__ == '__main__':
    main()
