"use client";
import * as d3 from "d3";
import popularity from "../../public/popularity.json";
// import { promises as fs } from "fs";
import coords from "../../public/raw_data.json";
// import { useState } from "react";
import useWindowSize from "./hooks/useWindowSize";

interface artist {
  name: string;
  x: number;
  y: number;
  popularity: number;
  genre: number;
}
const padding = 0.5;

const colors = [
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
];
const scale = 1;

// function ArtistCircle({ artist, color }: { artist: artist; color: string }) {
//   let radius =
//   if (Number.isNaN(radius)) {
//     radius = 0;
//   }
//   return (
//     <circle
//       cx={artist.x * scale}
//       cy={artist.y * scale}
//       r={radius}
//       opacity=".5"
//       fill={color}
//       id={artist.name}
//     />
//   );
// }

export default function Page() {
  const artists: artist[] = [];
  const genres: Map<string, artist[]> = new Map<string, artist[]>();
  for (let i = 0; i < coords.length; i++) {
    const genre = coords[i];
    const genres_artists: artist[] = [];
    for (let j = 0; j < genre["x"].length; j++) {
      const artist = {
        name: genre["customdata"][j][0],
        x: genre["x"][j],
        y: genre["y"][j],
        popularity: popularity[genre["customdata"][j][0]],
        genre: i,
      };
      genres_artists.push(artist);
    }
    artists.push(...genres_artists);
    genres.set(genre["name"], genres_artists);
  }

  const min_x = Math.min(...artists.map((artist) => artist.x));
  const max_x = Math.max(...artists.map((artist) => artist.x));
  const min_y = Math.min(...artists.map((artist) => artist.y));
  const max_y = Math.max(...artists.map((artist) => artist.y));
  const { height, width } = useWindowSize();
  // const output_height = Math.floor(
  //   (output_width / (max_x - min_x)) * (max_y - min_y)
  // );

  const tooltip = d3
    .select("#labels")
    .append("div")
    .style("position", "absolute")
    .style("visibility", "hidden");

  const points = d3
    .selectAll("svg")
    .selectAll("g")
    .selectAll("circle")
    .data(artists)
    .enter()
    .append("circle")
    .attr("cx", (data) => data.x)
    .attr("cy", (data) => data.y)
    .attr("r", (data) => (Math.sqrt(data.popularity) / 150) * scale)
    .attr("opacity", 0.5)
    .attr("fill", (data) => colors[data.genre]);

  const labels = d3
    .selectAll("svg")
    .selectAll("g")
    .data(artists)
    .enter()
    .append("text")
    .attr("x", (data) => data.x)
    .attr("y", (data) => data.y)
    .attr("id", "#label")
    .attr("font-size", 0.01)
    .text((data) => data.name);

  let zoom = d3.zoom().on("zoom", change_with_zoom);

  function change_with_zoom(e) {
    d3.selectAll("svg").attr("transform", e.transform);
    const points = d3
      .selectAll("svg")
      .selectAll("g")
      .selectAll("circle")
      .data(artists)
      .enter()
      .attr(
        "r",
        (data) => (Math.sqrt(data.popularity) / 150) * scale * e.transform.k
      );
  }

  d3.select("svg").call(zoom);

  return (
    <>
      <svg
        width={width}
        height={height}
        viewBox={`${min_x - padding} ${min_y - padding} ${
          max_x - min_x + 2 * padding
        } ${max_y - min_y + 2 * padding}`}
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect
          fill="#fff"
          x={min_x - padding}
          y={min_y - padding}
          width={max_x - min_x + 2 * padding}
          height={max_y - min_y + 2 * padding}
        />
        <g></g>
      </svg>
      <div id="labels"></div>
    </>
  );
}
