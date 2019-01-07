#!/usr/bin/python

import boto3, json, pprint, re, os, time, jwt
from urllib.parse import unquote

# lambda variaveis de ambiente
clientid    = os.environ['clientid']
userpoolid  = os.environ['userpoolid']

c           = boto3.client('cognito-idp')


# Retorna o código html
def return_html(txt, title, head):
    # head  = pprint.PrettyPrinter().pformat(head)

    return {
        'statusCode': '200', 
        'body': '<center><h1>'+title+'</h1><a href = "./login">login</a> | <a href = "./register">register</a><br><br>'+str(txt)+'</center><br>'+str(head), 
        'headers': {'Content-Type': 'text/html', 'charset': 'utf-8'}
    } 
    
# Retorna o código html
def return_forbidden():
    # head  = pprint.PrettyPrinter().pformat(head)

    return {
        'statusCode': '503', 
        'body': '<center><h1>Voce nao tem acesso.</h1></center><br>', 
        'headers': {'Content-Type': 'text/html', 'charset': 'utf-8'}
    }     
    
def get_creds(para):
    user    = ''
    pasw    = ''
    
    for y in para.split('&'):
        if re.search('username', y):
            user    = unquote(y[9:])
        elif re.search('password', y):
            pasw    = unquote(y[9:])
         
    return user, pasw
    
def post_login(head, para):
    user, pasw  = get_creds(para)
    
    
    if len(user) > 1 and len(pasw) > 5:
        
        try:
            r = c.initiate_auth(ClientId = os.environ['clientid'],
                AuthFlow = 'USER_PASSWORD_AUTH', 
                AuthParameters = {'USERNAME' : user.strip(), 'PASSWORD' : pasw.strip()}
            )
            
            print(r['AuthenticationResult']['AccessToken'])
            payload = jwt.decode(r['AuthenticationResult']['AccessToken'], verify=False)
            print(payload['cognito:groups'])
            
            x = return_html('<h1>Logado como: '+str(user)+' dos Grupos: '+''.join(payload['cognito:groups'])+'</h1><br><h4>Token: '+r['AuthenticationResult']['AccessToken']+'</h4>', '', '')

        except Exception as e:
            x = return_html(e, '', '')

        return x
        
    return return_html('invalid user or password entered, this is what i received:\nusername: '+user+'\npassword: '+pasw, head)

def post_register(head, para):
    user, pasw  = get_creds(para)
    
    if len(user) > 1 and len(pasw) > 5:
        try:
            print(c.sign_up(Username = user, Password = pasw, ClientId = clientid, UserAttributes = [{'Name': 'email', 'Value': 'devnull@example.com'}]))  #, {'Name' : 'color', 'Value' : str(color)}]))
            print(c.admin_confirm_sign_up(UserPoolId = userpoolid, Username = user))
            return return_html('created user '+user, 'created user '+user, '')
        
        except Exception as e:
            return return_html(e, 'error', head)
            
    else:
        return return_html('invalid user or password entered, this is what i received:\nusername: '+user+'\npassword: '+pasw, he)


def get_cred_page(head, txt, opt):
    body    = '''<br><form method="post">
    username: \t <input type="text" name="username" /><br />
    password: \t <input type="password" name="password" /><br />'''
    body    += opt
    body    += '''<input type="submit" /></form><hr />'''
    
    return return_html(body, txt, head)
    
    
def get_admin_page(head, txt, opt):
    body    = '''<h1>Pagina de Administração</h1>'''

    
    return return_html(body, txt, head)    

# lambda handler
def lambda_handler(event, context):
    head    = str(event)
    meth    = str(event['httpMethod'])
    path    = str(event['path']).strip('/')
    para    = str(event['body'])

    # handle get requests by returning an HTML page
    if meth == 'GET' and path == 'register':
        return get_cred_page(head, 'register here', '')

    elif meth == 'GET' and path == 'login':
        return get_cred_page(head, 'login here', '')
        
    elif meth == 'GET' and path == 'administracao':
        return return_forbidden()   
      
    # hande post requests by submitting the query strings to the api        
    elif meth == 'POST' and path == 'register':
        return post_register(head, para)
        
    elif meth == 'POST' and path == 'login':
        return post_login(head, para)    

    else:
        return return_html('invalid request, try <a href="./login">login</a> instead', 'invalid request', head)
