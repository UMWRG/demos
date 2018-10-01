import hydra_functions as hf

import click

@click.command()
@click.option('--network-id', '-n', default='Example Project', help='The name of the project')
def get_network_details(network_id):
    """
        Get the details for a network
    """

    #Connect to hydra
    conn = hf.connect()
    
    #Check if the project exists. A user can have access to multiple projects
    #with the same name, so this returns a list.
    try:
        network = conn.get_network(network_id=network_id)
    except:
        print("An error occurred retrieving network %s", network_id)

    print("Name: {0}".format(network.name))
    print("ID  : {0}".format(network.id))
    print("Scenario ID: {0}".format(network.scenarios[0].id))

if __name__ == '__main__':
    get_network_details()
