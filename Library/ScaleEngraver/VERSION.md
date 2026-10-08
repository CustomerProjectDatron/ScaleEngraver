# ScaleEngraver v1.2.0

- `EngraveAngleScale` for angle scales on a straight edge (speed square): pivot, start and end point; ticks radial to the pivot
- `skipFirst` / `skipLast` leave out numbers, `skipFirstTicks` / `skipLastTicks` leave out ticks
- Sample `SampleSpeedSquare`: four scales on one plate, then the 45 degree edge milled with tool radius compensation
- Top view of the simulated speed square in the README and the store description; library visible to the user

# ScaleEngraver v1.1.0

One command per scale, heights and feeds like the DATRON milling cycles.

- `EngraveRuler`, `EngraveDial` and `EngraveAngleScale` (speed square) with defaults for ticks, numbers and depth
- One tick length plus a factor for all tick levels; millimetre, centimetre and inch rulers; degree, percent, gauge,
  protractor and clock dials
- Own scales from `valueStart` to `valueEnd`; ticks on multiples of the step
- Position with `X Y Z`, depth measured from `Z`, `feedHeight`, `infeedZ` (also for the numbers),
  `PrePositioning` over `SafeZHeightForWorkpiece`, feeds from `SetFeedTechnology`, spindle handled by `ExecuteMillingCycle`
- `skipFirst` / `skipLast` leave out numbers, `skipFirstTicks` / `skipLastTicks` leave out ticks
- Header images and icons in the command help, commented samples and an operator dialog app

# ScaleEngraver v1.0.0

Initial release: linear and circular scales with major, medium and minor ticks, plan and engrave layers, samples.
