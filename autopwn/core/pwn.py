import re
import os
import yaml
from pwnlib.log import Logger

log = Logger()

def parse_config():
    try:
        with open("autopwn.conf") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            return config
    except EnvironmentError:
        log.error("Fatal: Configure File Not Found")
        exit(1)

def awd(argv, exp=None, get_flag=None, submit=None, targets=None, qes=None):
    config = parse_config()

    assert (exp != None and get_flag != None and submit != None and targets != None and qes != None)
    from autopwn.awd import attacker
    a = attacker.Attacker(config)
    setattr(attacker.Attacker, 'targets', targets)
    setattr(attacker.Attacker, 'submit', submit)
    setattr(attacker.Attacker, 'exp', exp)
    setattr(attacker.Attacker, 'get_flag', get_flag)
    a.run(argv=argv, qes=qes)


def ctf(argv, exp=None, get_flag=None, inter=None, needed=None):
    config = parse_config()
    # parse configuration file

    if exp == None or get_flag == None:
        log.error("Exp or Get_flag function not provided.")
        exit(1)
    
    from autopwn.ctf.attack import Attack
    setattr(Attack, 'exp', exp)
    setattr(Attack, 'get_flag', get_flag)
    attack_obj = Attack(argv=argv, config=config, inter=inter, needed=needed)
    
    if argv[1] == 'patch' and (inter or needed):
        if not attack_obj.ensure_lib():
            log.success("ELF File Modified.")
        else:
            log.failure("ELF File Modifying Failed.")
        exit(0)
    
    tube = attack_obj.process_init()
    
    attack_obj.exp(tube)
    flag = attack_obj.get_flag(tube)
    tube.success(flag)
