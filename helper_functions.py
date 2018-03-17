import os
import errno


def create_folder(dir):
    """Creates the server permissions directory if it doesn't exist"""
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def populate_permissions(dir):
    """Gets permission info for each server"""
    servers = {}
    for server_file in os.listdir(dir):
        with open(os.path.join(dir, server_file)) as f:
            servers[server_file] = [l.rstrip("\n") for l in f.readlines()]
    return servers


def get_channel_and_server(ctx):
    """Returns string representations of channel, server"""
    return str(ctx.message.channel), str(ctx.message.server)


def get_channel_names(ctx):
    """Returns names of all channels in this server"""
    return [str(c) for c in ctx.message.server.channels]


def check_if_allowed_channel(ctx, servers):
    """Checks if countdown bot is allowed to count in this server"""
    chan, serv = get_channel_and_server(ctx)
    if serv in servers:
        if chan in servers[serv]:
            return True
    return False


def readable_channel_list(server_name, servers):
    """Returns a readable list of channels to be printed for list_channels"""
    channel_names = servers[server_name]
    channel_names = list(map(lambda x: "`{}`".format(x), channel_names))
    if len(channel_names) > 1:
        return ", ".join(channel_names[:-1]) + ", and " + channel_names[-1]
    else:
        return str(channel_names[0])


def emoji_countdown_list(count_from, num_emoji):
    """Returns a countdown list in emoji form."""
    output_emoji_list = []
    for num in range(count_from, 0, -1):
        s = ""
        for n in map(int, list(str(num))):
            s += num_emoji[n]
            s += " "
        output_emoji_list.append(s)
    return output_emoji_list
