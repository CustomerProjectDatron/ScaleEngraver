# Scale Engraver

Engrave rulers, dials, gauges and protractors on your part from a handful of parameters. You say
what the scale shows (for example 0 to 100, or 0 to 360 degrees), where it sits and how long its
ticks are, and Scale Engraver generates the toolpath for the ticks, the baseline and the numbers.

## The problem

Scales have dozens or hundreds of ticks, each with its own position, length and number. Drawing
them one by one in CAM, or writing every move by hand, is slow, easy to get wrong, and has to be
redone whenever the length, the unit or the step changes.

## How Scale Engraver solves it

You write one line per scale, for example `EngraveRuler X=10 Y=10 Z=0 length=100` or `EngraveDial X=60 Y=60 Z=0 radius=28`.
Position and size are all you must give; the ticks, the numbers, the depth and the heights come from sensible
defaults that you can override one by one. You define one tick length - the longest tick - and every finer level
is a fixed fraction of it, so a whole ruler scales with a single value. Straight scales can run in any direction,
circular scales can cover a full circle or any part of it. For every tick the tool moves up,
over, rapidly down to the feed height just above the surface, feeds down to the depth and cuts - and nothing is
cut between two ticks.

Start the sample program **ScaleEngraverApp** and answer a few dialogs. To engrave a scale from your own
program, copy one of the commented samples.

## What it can do

- Engrave millimetre and centimetre rulers, and real inch rulers (inch, 1/2, 1/4, 1/8, 1/16 with fractions)
- Engrave dials: degrees, percent, gauges with a partial sweep and protractors
- Straight scales in any direction, ticks on either side; circular scales over any part of the circle
- Define one tick length: every finer tick level is a fixed fraction of it (factor 0.7 by default), and the numbers follow
- Defaults for ticks, numbers, depth and heights in millimetres, converted automatically when the control is set to inch
- Numbers on dials that follow the circle, run along the radius, or stay horizontal
- Make your own scale: say from which value to which value, for example 20 to 70, -50 to 50 or a gauge from 20 to 80
- Leave out the first or last tick, for example where a scale ends on the edge of the part
- Change any default one by one: tick length, factor, depth, number size, heights, values, angles
- Works like the DATRON milling cycles: the position has X, Y and Z, the depth is measured from Z, the tool positions with `PrePositioning` over the `SafeZHeightForWorkpiece`, plunges from a feed height and cuts with the feeds of `SetFeedTechnology`; `infeedZ` splits a deep engraving into several cuts

## Limits and requirements

- Use a tool whose maximum spindle speed is defined, otherwise the control refuses the speed. Set speed
  and the feeds (`SetFeedTechnology plunge= finishing=`) to suit your tool and material.
- Z is the height of the surface of the part, depths are given as
  positive numbers (how deep).
- The numbers are engraved with the control's single-stroke text engraving; free text and other
  fonts are not part of the package.
- There is no on-screen preview of the scale yet.
- Run the first part on scrap material.

## Contents

- Library `ScaleEngraver` - the commands `EngraveRuler` and `EngraveDial`
- Sample `ScaleEngraverApp` - asks for the scale in two dialogs and engraves it
- Samples `ScaleEngraverSample`, `SampleInchRuler`, `SampleProtractor`, `SampleGauge`, `SampleCustomScale`, `SampleEdgeRuler`, `SampleDialVariants` - short commented examples to copy from
