import hydra_functions as hf

from hydra_base.lib.objects import Dataset

import click

@click.command()
@click.option('--network-id', '-n', help='Network ID')
@click.option('--recipient-username', '-u', help='The user ID of the receiving user.')
@click.option('--hidden-attribute', '-a', default='cost', help='The name of the attribute to hide.')
def add_user(network_id, recipient_username, hidden_attribute):
    """
        Get the details for a network
    """

    #Connect to hydra
    conn = hf.connect()
    
    #make a lookup of the ID of all attributes to their name so we can look it up
    all_attributes = conn.get_attributes()
    attribute_id_name_map = {}
    for a in all_attributes:
        attribute_id_name_map[a.id] = a.name

    try:
        network = conn.get_network(network_id=network_id, include_data='Y')

        print("Hiding sensitive datasets...")
        hidden_count = 0 # count how many datasets get hidden
        for rs in network.scenarios[0].resourcescenarios:
            if attribute_id_name_map[rs.attr_id].lower() == hidden_attribute.lower():
                # Hide the dataset. 
                conn.hide_dataset(dataset_id=rs.dataset.id) 
                hidden_count = hidden_count + 1
        print("{0} datasets hidden".format(hidden_count))
    except Exception as e:
        print("An error occurred retrieving network {0}".format( network_id ))
        return


    
    #Check if the user exists.
    conn.share_network(network_id=network_id, usernames=[recipient_username], read_only='N', share='N')
    print("Network shared successfully")
    

if __name__ == '__main__':
    add_user()
