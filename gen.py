from pwn import *
import yaml
import os
import sys
import shutil
import getopt

base_dir = '/root/Desktop/Parallels Shared Folders/Home/Downloads'
now_dir = os.getcwd()
template_path = '/root/Desktop/Parallels Shared Folders/Home/Kali/pypwn/autopwn.conf'
config = {}

def parse_opt():
    opts, args = getopt.getopt(sys.argv[1:], 'p:u:f:m:r:c:ah')

    for opt, value in opts:
        if '-f' == opt:
            check_file(value)
        elif '-r' == opt:
            config['server']['ip_port'] = value
            # print config
        elif '-c' == opt:
            if value != 'nc' and value != 'ssh':
                help()
            config['server_class'] = value
        elif '-u' == opt:
            config['server']['username'] = value
        elif '-p' == opt:
            config['server']['password'] = value
        elif '-m' == opt:
            if value != 'ctf' and value != 'awd':
                help()
            else:
                config['mode'] = value
        else:
            help()

    if config["mode"] == 0:
        config["mode"] = 'ctf'
    if config["server_class"] == 0:
        config["server_class"] = 'nc'

def help():
    print("help: ")
    print(" -f filename            must specify without -a")
    print(" -m mode                choose between ctf and awd")
    print(" -r ip address          ip address of remote server")
    print(" -c connect method      now you can choose ssh or nc")
    print(" -u username            if you choose ssh")
    print(" -p password            if you choose ssh")
    print(" -a                     update conf")
    exit(1)


def no_parameter():
    print("Fatal: Parameter Not Specified.")
    exit(1)


def check_file(elf_name):
    if os.path.exists(now_dir + '/' + elf_name):
        elf = now_dir + '/' + elf_name
    elif os.path.exists(base_dir + '/' + elf_name):
        elf = base_dir + '/' + elf_name
        shutil.move(elf, now_dir + '/' + elf_name)
    else:
        print("Fatal: No Such File.")
        exit(1)
    config['elf'] = elf_name


if __name__ == '__main__':
    if os.path.exists(now_dir + '/autopwn.conf'):
        conf_path = now_dir + '/autopwn.conf'
    else:
        conf_path = template_path
    
    try:
        config = yaml.load(open(conf_path, 'r'), Loader=yaml.FullLoader)
    except IOError:
        print("Fatal: Template File Not Found.")

    parse_opt()
    os.chmod(config['elf'], 0o775)
    elf = ELF(config["elf"])
    conf_file = now_dir + '/autopwn.conf'
    # print config
    with open(conf_file, 'w') as conf:
        yaml.dump(config, conf)
