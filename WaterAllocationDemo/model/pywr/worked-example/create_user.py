import hydra_functions as hf
import hydra_base as hb

import click

@click.command()
@click.option('--username', '-u', default='User1', help='The new users username')
@click.option('--password', '-p', default='password', help='The new users password')
def add_user(username, password):
    """
        Get the details for a network
    """

    #Connect to hydra
    conn = hf.connect()
    
    #Check if the user exists.
    try:
        user = conn.get_user_by_name(uname=username)
        print("User {0} already exists with ID {1}".format(username, user.id))
    except:
        user = hb.JSONObject({'username':username, 'password':password})
        newuser = conn.add_user(user=user)
        print("User {0} added with ID {1}".format(username, newuser.id))
    

if __name__ == '__main__':
    add_user()
