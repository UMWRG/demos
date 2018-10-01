import hydra_functions as hf

import click

@click.command()
@click.option('--name', '-n', default='Example Project', help='The name of the project')
def create_project(name):
    """
        Add a new project.
    """

    #Connect to hydra
    conn = hf.connect()
    
    #Check if the project exists. A user can have access to multiple projects
    #with the same name, so this returns a list.
    projects_with_name = conn.get_project_by_name(project_name=name)

    if len(projects_with_name) == 0:
        project = {'name':name}
        #If the project doesn't exist, create it.
        new_project = conn.add_project(project)
    else:
        #return the first project with this name. THis could be improved
        #to somehow check for the correct project, but lets assume the list is 
        #always 1 in length.
        new_project = projects_with_name[0]

    print("Project {0} created with ID {1}".format(name, new_project.id))

    return new_project

if __name__ == '__main__':
    create_project()
