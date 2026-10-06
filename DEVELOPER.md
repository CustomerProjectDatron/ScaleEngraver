# ScaleEngraver - developer documentation

Not part of the package (the package only contains `Library/`, `Samples/` and `Tests/`, see
`metadata.json`). The end-user documentation is `README.md`, the store page `Installer/store/description.md`.

**Shape:** pure simPL, no C# service. The planning is plain data, so a preview and a web API can be
added later without touching the engraving code.

## Layout

| Path | Content |
|------|---------|
| `Library/ScaleEngraver/ScaleEngraver.simpl` | the library: parameter structures, planning layer, engraving layer |
| `Library/ScaleEngraver/images/` | parameter icons used in the `@doc` texts (`README.md` there lists them) |
| `Samples/ScaleEngraver/` | the dialog app and the commented samples |
| `Tests/ScaleEngraver/ScaleEngraverTest.simpl` | checks of the planning layer (no machine motion) |
| `Installer/store/` | store listing: `description.md`, `cover.png` / `cover.svg` (placeholder cover) |
| `docs/` | README graphics, `gen_graphics.py` and `render.ps1` to regenerate them |
| `.agents/`, `.claude/`, `AGENTS.md`, `CLAUDE.md` | simPL skill, deployed by `simpl-skill install` |

## Architecture

![Parameters, plan, engrave](docs/workflow.png)

* **Planning** (`PlanLinearScale`, `PlanCircularScale`) is a pure function: no machine command. The
  result `ScalePlan` holds `lines` (ticks, baseline), `arcs` (circular baseline) and `labels`
  (text, position, rotation, size, depth). It can be serialised with `System::ValueToJson`, drawn as
  a preview or returned by a service.
* **Engraving** (`EngraveScalePlan`; `EngraveLinearScale` / `EngraveCircularScale` plan and engrave in
  one call) is pure motion: the **calling program** selects the tool and sets `Rpm`, `Feed` and
  `Spindle On/Off`. Plunges and cuts use the current `Feed`.
* **User interface** is separate (`ScaleEngraverApp`). Another front end only has to build the same
  structures and call the library.

### Move sequence

![Move sequence of one tick](docs/move_sequence.png)

For every tick, baseline and arc: up to `retractZ`, rapid over the start, rapid down to `approachZ`,
feed down to the depth, cut horizontally, up again. No connecting move at depth (measured in the
debugger: Z 0.5, -0.2, -0.2, 2 for one tick). Text is engraved with `StandardTextEngrave`, which
brings its own approach. It takes a positive `depth`, and `strokeCuttingZ` counts like the depth
(final cut at `-(strokeCuttingZ + depth)`), so the library passes `strokeCuttingZ = -approachZ` and
`depth = textDepth + approachZ`; `strokeRapidZ` is `retractZ`.

## Parameters (structures)

All lengths in mm, angles in degrees (0 = +X, counter-clockwise). Depths are **positive numbers =
how deep below the surface** (Z = 0 on the surface); the library converts them (`Z = -depth`).
Every structure has a `New...` constructor with defaults for optional values; the `@doc` texts
describe every parameter.

| Structure | Fields |
|-----------|--------|
| `ScaleDivision` | `valueStart`, `valueEnd`, `majorStep`, `minorDivisions`, `mediumEvery`, `skipFirstTick`, `skipLastTick` |
| `TickStyle` (major, medium, minor) | `tickLength`, `tickDepth` |
| `LabelSettings` | `labelHeight`, `labelWidth`, `labelDepth`, `labelOffset`, `decimals`, `labelEvery`, `skipFirstLabel`, `skipLastLabel`, `fractionDenominator` (0 = decimals) |
| `LinearScale` | `originX/Y`, `scaleLength`, `rotationAngle`, `side`, `majorTick`, `minorTick`, `mediumTick`, `labelFormat`, `baselineDepth` |
| `CircularScale` | `centerX/Y`, `radius`, `startAngle`, `endAngle`, `side`, `majorTick`, `minorTick`, `mediumTick`, `labelFormat`, `orientation`, `baselineDepth` |
| `FractionScale` (inch ruler) | `originX/Y`, `scaleLength`, `rotationAngle`, `valueStart`, `valueEnd`, `levels` (halvings), `tickStyles` (one per level), `unitLabel`, `fractionLabel`, `fractionLabelLevel`, `side`, `skipFirstTick`, `skipLastTick`, `baselineDepth` |
| `EngraveHeights` | `retractZ`, `approachZ`, `safeZ` |

## Development

* Link the repo to the control once: `simpl-pkg install --dev` (needs Windows Developer Mode).
* After changing a **signature** of the library (a parameter, a structure) the control must reload
  the user library folder (`POST /api/Execution/RefreshUserDefinedLibraryFolder`, by the operator)
  before dependent modules compile; then `refresh_simpl_catalog`. A changed program body is picked
  up through the links.
* Compile: `simpl-mcp check <file>`. The tests can be run in the isolated simulation.
* Regenerate graphics: `docs\render.ps1` (Python and `resvg`); icons: `Library\ScaleEngraver\images\render.ps1`.

## Status

* Compiled against a control; the planning and engraving programs, the tests and the samples ran in
  the simulation. On the control's simulation screen the ticks and the text engrave at the right
  depth with the move sequence above.
* **Not yet run on a real machine** - first run on scrap material.
* The text placement relies on `StandardTextEngrave`: vertically centred on the programmed point,
  aligned horizontally by the label's alignment, rotation in degrees counter-clockwise.
* `Horizontal` labels on a circle estimate the text width from `labelWidth` x number of characters.

## Next steps (not implemented)

* Web API (C# service, OpenAPI 3, generated simPL client - see
  `.agents/skills/simpl/references/external-services.md`) that takes the parameter structures and
  returns the `ScalePlan` as JSON / SVG for a preview and parametrisation.
* Non-uniform scales (logarithmic), inscriptions on a circle.

## Inch

* `AxisSystem::ImperialMeasuring` / `AxisSystem::MetricMeasuring` switch the whole control; the library only uses plain numbers, so an inch program needs no conversion (see `SampleInchRuler`, verified in the editor simulation: 3230 positions).
* **The library module must not declare a measuring system** (no `@ MeasuringSystem = ... @` in its header). With `Metric` in the library header, calling it from an inch program (or after `ImperialMeasuring`) faulted at the first call in the isolated simulator.
* `FractionScale` (`NewFractionScale`, `PlanFractionScale`, `EngraveFractionScale`) is the inch ruler: the unit is halved `levels` times, level = number of halvings needed to reach a tick (whole units 0, halves 1 ...), one `TickStyle` per level, unit numbers from `unitLabel`, fractions (fractional part only, via `FractionText`) from `fractionLabel` down to `fractionLabelLevel`.
* Fraction labels: `FractionText` rounds to the nearest 1/denominator, reduces with gcd and writes mixed numbers (tested: 1/8, 1/4, 3/8, 1/2, 1 1/2, 2 13/16, 3/10, -3/4).
