from argparse import ArgumentParser
from os.path import exists, join as pjoin
from sys import argv

cfg_array = list()
base_dir = str()

def main():
    global cfg_array
    global base_dir

    aparser = ArgumentParser(description='Nginx config merger')
    aparser.add_argument('-f', help='Path to nginx config', metavar='config_file', required=True)
    aparser.add_argument('-b', help='Nginx configurations base dir', metavar='nginx_base')
    args = aparser.parse_args()

    cfg_file_path = args.f
    base_dir = args.b or '/etc/nginx'

    if not exists(cfg_file_path):
        cfg_file_path = pjoin(base_dir, cfg_file_path)

    if not exists(cfg_file_path):
        msg = list()
        msg.append('Cannot find configuration file {0}'.format(args.f))
        
        if args.f != cfg_file_path:
            msg.append('or {0}'.format(cfg_file_path))

        print(' '.join(msg))
        return

    process_file(cfg_file_path)

    print("\n".join(cfg_array))

def process_file(file_path):
    global cfg_array
    global base_dir

    with open(file_path, 'r') as cfg_file:
        for cfg_line in cfg_file:
            cfg_line = cfg_line.replace("\n", '')
            line_split = cfg_line.split()
            
            if len(line_split) > 1 and 'include' in line_split and '#' not in cfg_line:
                inc_cfg_file = line_split[1].replace(';', '')

                if not exists(inc_cfg_file):
                    inc_cfg_file = pjoin(base_dir, inc_cfg_file)

                if not exists(inc_cfg_file):
                    cfg_array.append('{0} # !!! BROKEN !!!'.format(cfg_line))
                    continue

                process_file(inc_cfg_file)
                continue

            cfg_array.append(cfg_line)

if __name__ == '__main__':
    main()
