import sys
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.vault import VaultSecret
from ansible.module_utils._text import to_bytes


def runplaybook(inventory,playbook,project,bname,secret):
    loader = DataLoader()
    invlist=[]
    invlist.append(inventory)
    inv=InventoryManager(loader=loader,sources=invlist)

    variable_manager=VariableManager(loader=loader,inventory=inv)
    pblist=[]
    
    pblist.append(playbook)

    if secret != '':
       loader.set_vault_secrets([('default',VaultSecret(_bytes=to_bytes(secret)))])

    
     
    
    passwords={}
    Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
                      'diff'])
    options = Options(connection='smart',
                       remote_user=None,
                       ack_pass=None,
                       sudo_user=None,
                       forks=5,
                       sudo=None,
                       ask_sudo_pass=False,
                       verbosity=5,
                       module_path=None,
                       become=None,
                       become_method=None,
                       become_user=None,
                       check=False,
                       diff=False,
                       listhosts=None,
                       listtasks=None,
                       listtags=None,
                       syntax=None)


    pb = PlaybookExecutor(
        loader = loader,
        playbooks=pblist,
        inventory=inv,
        variable_manager=variable_manager,
        passwords = passwords,
        options=options
)

    f=open('/opt/Projects/'+project+'/logs/'+bname+'out.log','a+')
   # ferr=open('/opt/Projects/'+project+'/logs/'+bname+'err.log','a+')
    sys.stdout = f
   # sys.stderr = ferr
    result = pb.run() 
   # ferr.close()
    f.close()
    return result
