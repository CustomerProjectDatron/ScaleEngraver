# Scale Engraver

Engrave rulers, dials, gauges and protractors on your part from a handful of parameters. You say
what the scale shows (for example 0 to 100, or 0 to 360 degrees), where it sits and how long its
ticks are, and Scale Engraver generates the toolpath for the ticks, the baseline and the numbers.

## The problem

Scales have dozens or hundreds of ticks, each with its own position, length and number. Drawing
them one by one in CAM, or writing every move by hand, is slow, easy to get wrong, and has to be
redone whenever the length, the unit or the step changes.

## How Scale Engraver solves it

You enter the scale values (first value, last value, a major tick every n, how many minor ticks
in between), the tick lengths and depths, and the size of the numbers. The library places every
tick and number for you. Straight scales can run in any direction, circular scales can cover a
full circle or any part of it, clockwise or counter-clockwise. For every tick the tool moves up,
over, rapidly down to just above the surface, feeds down to the depth and cuts - and nothing is
cut between two ticks.

Start the sample program **ScaleEngraverApp** and answer a few dialogs. To engrave a scale from your own
program, copy one of the commented samples.

## What it can do

- Engrave straight scales (rulers) in any direction, with ticks on either side of the line
- Engrave circular scales: full dials, gauges with a partial sweep, protractors, ticks outside or inside
- Use three tick classes - major, medium and minor - each with its own length and depth
- Engrave the numbers beside the major ticks: font size, decimals, gap, every n-th number only
- Engrave a real inch ruler: inches, halves, quarters, eighths and sixteenths with their own tick lengths, big numbers for the inches and small fractions beside the longer ticks
- Write the numbers of any scale as fractions (1/8, 1/4, 3/8, 1/2, 1 1/2 ...)
- Skip the first or last tick, or only its number, for example where a scale ends on the edge of the part
- Turn the numbers on circular scales to follow the circle, run along the radius, or stay horizontal
- Engrave the scale line (or arc) itself at its own depth
- Start just above the surface: the feed move begins at an approach height you set

## Limits and requirements

- Use a tool whose maximum spindle speed is defined, otherwise the control refuses the speed. Set speed
  and feed to suit your tool and material.
- The work coordinate system must have Z = 0 on the surface of the part. Depths are given as
  positive numbers (how deep).
- The numbers are engraved with the control's single-stroke text engraving; free text and other
  fonts are not part of the package.
- There is no on-screen preview of the scale yet.
- Run the first part on scrap material.

## Contents

- Library `ScaleEngraver` - plans and engraves the scales
- Sample `ScaleEngraverApp` - asks for the scale in a few dialogs and engraves it
- Samples `ScaleEngraverSample`, `SampleInchRuler`, `SampleProtractor`, `SampleGauge`, `SampleEdgeRuler`,
  `SampleDialVariants`, `SamplePlanOnly` - commented examples to copy from
