<!-- simpl-skill:begin (managed by 'simpl-skill install' - edits inside this block are overwritten on reinstall; keep your own notes outside it) -->
# SimPL — DATRON next CNC scripting

This project writes SimPL (`.simpl`) for DATRON **next** machines.

SimPL has no standalone compiler, so a control is used as one — and as the source of the
live catalog of commands actually installed. The machine is infrastructure for writing
code; nothing here runs programs.

## The skills

| Task | Skill |
|------|-------|
| **Writing, reading or debugging `.simpl`** — nearly everything | `.agents/skills/simpl/SKILL.md` |
| Shipping it as a `.nextpkg` package | `.agents/skills/next-package/SKILL.md` |
| Reaching the control; read-only machine context while debugging | `.agents/skills/next-machine/SKILL.md` |

Each has its own task router: read the one that matches, then open only the resource it names.
**Starting a project, or unsure what comes next?** Follow the ordered path in
`.agents/skills/simpl/references/project-lifecycle.md` — machine setup, scaffold, dev-install,
library, sample, real run, ship — and do not skip a gate. Its "Which task, which tool" table
maps every step to the MCP tool or command that does it.

## Before writing `.simpl`

Read `.agents/skills/simpl/SKILL.md` first. Its **rules 1–11** are the traps that make
C-looking guesses fail to compile (space-separated arguments, `<>`, a terminator per block,
uninitialized reads, one namespace, …), and its skeleton is the shape of every module. Verify
every command with `lookup_simpl_catalog`, or
`python .agents/skills/simpl/scripts/lookup_cmd.py <Name> --exact` — never guess a name or a
parameter. Prefer canned cycles over hand-rolled toolpaths. Save `.simpl` as UTF-8 with BOM.

## Compile what you write

If the `simpl-compiler` MCP server offers `check_simpl_source`, compile every `.simpl` file
you write or edit: send the complete source, treat `isValid: false` as compiler feedback, fix
the smallest cause, re-check, and stop after five rounds or repeated identical diagnostics.
Otherwise `simpl-mcp check <file>`, or say the code is unvalidated. The endpoint compiles
only — it proves nothing about runtime behaviour, setup or safety.
Loop details: `.agents/skills/simpl/references/compiler-validation.md`.

## The control is read-only, with one fenced exception

`next_machine_status` and `next_read` report what a control is doing; `Runtime/Notifications`
carries what a run reported. Executing a program, moving an axis and writing a variable are
deliberately unreachable — running programs is the operator's job. The only writes are
`next_editor`'s: open a program in the editor, start the editor's simulation, show a screen,
upload a compiled one-off program below `machine:AgentPrograms/`. Say a capability does not
exist rather than reaching for raw HTTP. Credentials missing or `401`: stop and ask the
operator to run `simpl-mcp login` themselves.

The next control runs on **Windows** — run install, packaging and generator tools from a
Windows shell, not WSL.
<!-- simpl-skill:end -->
