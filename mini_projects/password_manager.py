

def view():
    with open('passwords.txt','r') as f:
        for line in f.readlines():
            data = line.rstrip();
            user, pwd = data.split('|')
            print('Account Name: ' + user + '  Password: '  + pwd);
            
            
            
    

def add():
    name = input('Account Name:')
    pwd =  input('Password:')
    
    with open('passwords.txt','a') as f:
        f.write(name + '|' + pwd + "\n");
     
    
    


while True:
    mode = input('would you like to add a new password or viw existing ones (add/view)')

    if mode == 'q' :
        quit();
    if mode == 'view':
        view();
    if mode == 'add':
        add();
    



