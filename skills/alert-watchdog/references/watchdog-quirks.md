# Watchdog quirks

Author: Sayandip Bagchi.

Platform behaviour met while building and running a watchdog and the intake it watches. Numbers
continue the router's quirk index (`${CLAUDE_PLUGIN_ROOT}/skills/observability/references/designer-quirks.md`).
Evidence for each lives in the tenant's `quirk-evidence.md` and `revisions.md`.

| # | Quirk | What to do |
|---|---|---|
| Q35 | **Read-after-write lag.** In the same run, "List rows present in a table" straight after "Add a row into a table" may not return the row just added. A burst count built from that list misses the current event, so a burst count of N needs N+1 events, and a count of 1 never fires. | Count **older** rows in the window (receipt < the new row's) and add 1 for the current event. Mirror the same semantics in the watchdog. |
| Q36 | `div()` of two integers returns an integer. `ticks` differences divided by ticks-per-day give whole days. | Divide a float: `div(float(…), 864000000000)`. |
| Q37 | The expression editor rejects float literals such as `864000000000.0` ("This expression has a problem"). | Use `float(n)` or divide a float by an integer. |
| Q38 | `createArray()` with no arguments passes the designer and the flow checker, then fails the run ("expects a comma separated list of parameters"). | Use `json('[]')` for an empty array. |
| Q39 | The Excel connector returns a limited page unless Pagination is on; Top Count alone does not page. | Turn Pagination on with a threshold, set Top Count, and order by the receipt column descending. |
| Q40 | Excel values arrive as strings; empty cells arrive as empty strings, and `float('')` fails. | Wrap numbers in `float()` / `int(float())`; guard blanks with `if(empty(x),'0',x)`. |
| Q41 | In the new designer, typing text that starts with `@` into a field stores it as an expression (Filter array advanced mode, Apply to each input, Append value, Condition left value). The fx editor is unreliable: text typed before it opens lands in the field as literal text, and Add can silently do nothing. A Copilot pane or a "ready" banner shifts every coordinate. | Prefer typed `@` text; when the fx editor is needed, open it, wait, focus it, type, Add, then **always** check Code view. Close Copilot and dismiss banners before coordinate clicks. |
| Q42 | Apply to each runs iterations in parallel by default. | Use Append to array variable (safe in parallel); never Set variable inside a loop. An empty input array runs zero iterations, which gates a time slot without a Condition. |
| Q43 | The platform's weekly "N of your flows have failed" email lists every flow with a failure in the past 7 days, including failures already fixed. | Do not read it as a watchdog finding or as a new failure; check the run history dates. |
| Q44 | Excel Online can ignore synthetic clicks and keystrokes entirely, or route them to the wrong cell. | Stop, ask the owner to edit by hand, then read the cells back from the live sheet. Never undo in bulk to recover (Q34). |
| Q45 | Resubmitting an old run from run history may create no new run. | Do not count a resubmit as proof; wait for the next real run. |
