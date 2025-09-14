import json
import math

output_width = 4096


def main(input_file, output_file, pop_file):
    popularity = {}
    for line in pop_file.read().splitlines():
        artist, pop = line.split("\t")
        popularity[artist] = int(pop)

    artists = []
    genres = []
    for genre in input_file:
        artists_for_genre = list(zip(genre["customdata"], genre["x"], genre["y"]))
        artists.extend(artists_for_genre)
        genres.append(artists_for_genre)

    minx = min(artist[1] for artist in artists)
    miny = min(artist[2] for artist in artists)
    maxx = max(artist[1] for artist in artists)
    maxy = max(artist[2] for artist in artists)

    padding = 0.5

    output_height = int(output_width / (maxx - minx) * (maxy - miny))

    output_file.write(
        """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n"""
    )

    output_file.write(
        f'<svg width="{output_width}" height="{output_height}" viewBox="{minx - padding} {miny - padding} {maxx - minx + 2 * padding} {maxy - miny + 2 * padding}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    )

    output_file.write(
        f'<rect fill="#fff" x="{minx - padding}" y="{miny - padding}" width="{maxx - minx + 2 * padding}" height="{maxy - miny + 2 * padding}"/>\n'
    )

    # output_file.write(
    #     f'<rect fill="#fff" stroke="#000" stroke-width=".02" x="{minx}" y="{miny}" width="{maxx - minx}" height="{maxy - miny}"/>\n'
    # )

    colors = [
        "#00df33",
        "#ff8009",
        "#180c18",
        "#003da0",
        "#732000",
        "#c124ff",
        "#12260d",
        "#eaca2f",
        "#667900",
        "#ffaeee",
    ]

    output_file.write("""<style>
                         .label{
                            font: sans
                         }
                        </style>
                     """)

    for color, genre in zip(colors, genres):
        for artist in genre:
            artist_name = artist[0][0]
            if artist_name not in popularity:
                print(artist_name)
                continue
            artist_pop = popularity[artist_name]
            output_file.write(
                f'<circle cx="{artist[1]}" cy="{artist[2]}" r="{0.01}" fill="{color}" opacity=".5" />'
            )

    spatial_hash = {}

    for artist in artists:
        coords = (int(artist[1]), int(artist[2]))
        if coords not in spatial_hash:
            spatial_hash[coords] = [artist[0]]
        else:
            spatial_hash[coords].append(artist[0])

    # for artist in artists:
    #     artist_name = artist[0][0]
    #     if artist_name not in popularity:
    #         print(artist_name)
    #         continue
    #     artist_pop = popularity[artist_name]
    #     if artist_pop > 150:
    #         output_file.write(
    #             f'<text x="{artist[1] + 0.01}" y="{artist[2]}" font-size="{math.log(artist_pop) / 160}" class="label">{artist_name}</text>'
    #         )

    # output_file.write("</svg>")


if __name__ == "__main__":
    with open("output/raw_data.json", mode="r") as raw_data:
        with open("output/chart.svg", mode="w") as output:
            with open("output/popularity.txt", mode="r") as pop:
                main(json.load(raw_data), output, pop)
