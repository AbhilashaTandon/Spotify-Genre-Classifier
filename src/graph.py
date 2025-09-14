import re
import json
from itertools import combinations
from collections import Counter

from alive_progress import alive_bar

plists = json.loads(open("data/output.json", mode="r").read())
artists = Counter()
edges = Counter()

with alive_bar(len(plists.items())) as bar:
    for idx, (plist_id, plist) in enumerate(plists.items()):
        for song in plist:
            artist = song["artists"][0]

            if artist is None:
                continue

            artist = re.sub("[^a-zA-Z_0-9 ]", "", artist)

            artists.update([artist])
        bar()

artists = Counter({k: c for k, c in artists.items() if c >= 10})
# filter out rare artists


with alive_bar(len(plists)) as bar:
    # iterate through json and count all artists and pairs of songs that coocur in playlists
    for idx, (plist_id, plist) in enumerate(plists.items()):
        for song1, song2 in combinations(plist, 2):
            artist, artist2 = song1["artists"][0], song2["artists"][0]

            if artist is None or artist2 is None:
                continue

            if artist == artist2:
                continue

            artist = re.sub("[^a-zA-Z_0-9 ]", "", artist)

            artist2 = re.sub("[^a-zA-Z_0-9 ]", "", artist2)

            if artist not in artists:
                continue

            if artist2 not in artists:
                continue

            edges.update([(artist, artist2)])
        bar()

artist_to_idx = dict()
# for quick mapping

# construct string of xml tags with all node data
node_tags = ""
with alive_bar(len(artists)) as bar:
    for idx, (artist, count) in enumerate(artists.items()):
        node_tags += f'<node id="{float(idx)}" label="{artist}"/>\n'
        # could do a better job at escaping {artist}
        artist_to_idx[artist] = float(idx)
        bar()

# construct string of xml tags with all edge data
edge_tags = ""
with alive_bar(len(edges)) as bar:
    for idx, (edge, count) in enumerate(edges.items()):
        if count <= 25:
            continue
        # delete weak edges to make graph simpler

        if edge[0] not in artists:
            continue
        if edge[1] not in artists:
            continue

        source_artist = artist_to_idx[edge[0]]
        target_artist = artist_to_idx[edge[1]]

        edge_tags += f'<edge id="{idx}" source="{source_artist}" target="{target_artist}" weight="{float(count)}"/>\n'

        bar()


# write all data to xml file
with open("output/artist.gexf", mode="w") as output_file:
    output_file.write("""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">
<meta lastmodifieddate="2010-03-03+23:44">
<creator>Gephi 0.7</creator>
</meta>
<graph defaultedgetype="undirected" idtype="string" type="static">
""")

    output_file.write(f'<nodes count="{len(artists)}">\n')
    output_file.write(node_tags)
    output_file.write("</nodes>\n")

    output_file.write(f'<edges count="{len(edges)}">\n')
    output_file.write(edge_tags)
    output_file.write("</edges>\n")

    output_file.write("</graph>\n")
    output_file.write("</gexf>\n")
