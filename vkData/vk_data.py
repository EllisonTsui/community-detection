import requests
import networkx


def get_friends_ids(user_id):
    url = 'https://api.vk.com/method/friends.get?user_id={}'.format(user_id)
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return response.json().get('response', [])


def get_friends_to_friends_map(user_id):
    '''
    Returns dict in which keys are friends of the given user and
    values are list of friends of key-friend
    '''
    map = {}
    user_friend_ids = get_friends_ids(user_id)
    for friend in user_friend_ids:
        print ('Processing id: ', friend)
        map[friend] = get_friends_ids(friend)
    return map


def get_friends_to_friends_links(f_to_f_map):
    '''
    Returns list of tuples with links between friends:
    [
    (friend1, friend2),
    (friend1, friend10),
     ...
    (friend10, friend4)
    ]
    '''
    links = []
    for friend, its_friends in f_to_f_map.items():
        for fr in its_friends:
            if friend != fr and fr in f_to_f_map.keys():
                links.append((friend, fr))
    return links


def get_friends_to_friends_graph(user_id):
    '''
    Returns networkx graph of friends of given user in which
    edge between two friends if and only if they are friends and
    if both are friends of a given user
    '''
    g = networkx.Graph(directed=False)
    f_to_f_map = get_friends_to_friends_map(user_id)
    edges = get_friends_to_friends_links(f_to_f_map)
    for fr1, fr2 in edges:
        g.add_edge(fr1, fr2)
    return g


def get_friends_to_friends_file(user_id, file_path):
    '''
    Returns file with links between friends of a given user in which
    link between two friends if and only if they are friends and
    if both are friends of a given user
    '''
    f_to_f_map = get_friends_to_friends_map(user_id)
    edges = get_friends_to_friends_links(f_to_f_map)
    with open(file_path, 'w') as f:
        for fr1, fr2 in edges:
            f.write("{}\t{}\n".format(fr1, fr2))
