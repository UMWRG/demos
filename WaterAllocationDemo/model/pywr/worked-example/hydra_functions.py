import hydra_client as hc


def connect(username='root', password=''):
    """
        Create a JSON-based connection to Hydra, and login
        args:
            username: defaults to 'root' (the default hydra user)
            password: defaults to ''     (the default hydra password)
        returns:
                JSONConnection
    """

    conn = hc.JSONConnection()
    conn.login(username, password)

    return conn


