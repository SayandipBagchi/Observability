# Watchdog build: actions and expressions

Author: Sayandip Bagchi.

Generic build for a Power Automate watchdog over an intake that logs to an Excel table. Names in
angle brackets come from the tenant `config.json`. Action names below are the designer's default
names; if yours differ, change every reference that uses them and re-read in Code view.

Assumed tables (adapt the column names to the tenant's `intake-rules.md`):

- **Rules**: `AlertID`, `Name`, `Active`, `BurstCount`, `BurstWindowMin`, `CooldownMin`,
  `LastBurstSerial`.
- **Log**: `AlertID`, `ReceivedSerial` (Excel serial: UTC days since 1899-12-30, fractional).

---

## Flow layout

```
Recurrence (every 30 min, start time chosen so runs land at :05 and :35 local)
├─ List rows present in a table            Rules
├─ Filter array                            burst rules
├─ List rows present in a table 1          Log  (Select AlertID,ReceivedSerial; order ReceivedSerial desc;
│                                                 Top Count + Pagination threshold sized for 14 days)
├─ Initialize variable                     Issues   (Array, [])
├─ Initialize variable 1                   NowSerial (Float)
├─ Apply to each                           over burst rules                 ── Layer 1
│   ├─ Filter array 1                      log rows for this alert in lookback + window
│   ├─ Filter array 2                      checkpoints
│   └─ Apply to each 1                     over checkpoints
│       ├─ Filter array 3                  rows in the burst window ending at the checkpoint
│       └─ Append to array variable        finding or ''
├─ Filter array 4                          log rows in the last 24 h        ── Layer 3a
├─ Append to array variable 1              finding or ''  (daily slot only)
├─ Filter array 5                          active, non-TEST rules
├─ Apply to each 2                         over active rules, daily slot only ── Layer 3b
│   ├─ Filter array 6                      this alert's rows in 14 days
│   ├─ Filter array 7                      of those, rows in 72 h
│   └─ Append to array variable 2          finding or ''
├─ Filter array 8                          non-empty findings
└─ Condition  length > 0
    └─ True: Send an email (V2) to the owner only
```

Findings are appended as text or as `''` and filtered at the end. This keeps the flow free of
nested Conditions, which the designer makes slow to build and easy to mis-wire.

---

## Expressions

All typed as text starting with `@` into the field (Filter array in advanced mode, the Apply to
each input, the Append value, the Condition's left value), then read back in Code view (Q41).

**NowSerial** (Initialize variable 1, Float, via the expression editor):

```
div(float(sub(ticks(utcNow()),ticks('1899-12-30T00:00:00Z'))),864000000000)
```

Divide a float: integer ÷ integer truncates to whole days (Q36). No float literals (Q37).

**Burst rules** (Filter array, from the Rules rows):

```
@and(equals(item()?['Active'],'Yes'),
     greater(float(if(empty(item()?['BurstCount']),'0',item()?['BurstCount'])),0),
     not(startsWith(string(item()?['Name']),'TEST')))
```

**Filter array 1**: this alert's rows in the lookback plus one burst window:

```
@and(equals(item()?['AlertID'],items('Apply_to_each')?['AlertID']),
     greaterOrEquals(float(item()?['ReceivedSerial']),
       sub(variables('NowSerial'),div(add(40,float(items('Apply_to_each')?['BurstWindowMin'])),1440))))
```

(40 = cadence 30 + settle 10. Change both numbers together.)

**Filter array 2**: checkpoints in (now − 40, now − 10] that are past last-fired + cooldown:

```
@and(greater(float(item()?['ReceivedSerial']),sub(variables('NowSerial'),div(float(40),1440))),
     lessOrEquals(float(item()?['ReceivedSerial']),sub(variables('NowSerial'),div(float(10),1440))),
     greater(float(item()?['ReceivedSerial']),
       add(float(if(empty(items('Apply_to_each')?['LastBurstSerial']),'0',items('Apply_to_each')?['LastBurstSerial'])),
           div(float(if(empty(items('Apply_to_each')?['CooldownMin']),'0',items('Apply_to_each')?['CooldownMin'])),1440))))
```

A checkpoint after last-fired + cooldown whose window meets the count means the intake should have
moved last-fired to at least that checkpoint. Using today's last-fired is safe: it only ever moves
forward, so a checkpoint that passes with today's value also passed at the time.

**Filter array 3**: rows in the window ending at the checkpoint (mirror the intake's edge):

```
@and(lessOrEquals(float(item()?['ReceivedSerial']),float(items('Apply_to_each_1')?['ReceivedSerial'])),
     greaterOrEquals(float(item()?['ReceivedSerial']),
       sub(float(items('Apply_to_each_1')?['ReceivedSerial']),div(float(items('Apply_to_each')?['BurstWindowMin']),1440))))
```

This counts the checkpoint itself. If the intake counts "older rows + 1", the totals agree; if the
intake counts only what List rows returned straight after its own Add a row, it under-counts by one
(Q35) and the watchdog will rightly report misses until the intake is fixed.

**Append to array variable** (Layer 1 finding):

```
@if(greaterOrEquals(length(body('Filter_array_3')),int(float(items('Apply_to_each')?['BurstCount']))),
  concat('MISSED BURST: ',items('Apply_to_each')?['AlertID'],' (',items('Apply_to_each')?['Name'],') had ',
    string(length(body('Filter_array_3'))),' events in ',string(items('Apply_to_each')?['BurstWindowMin']),
    ' min (threshold ',string(items('Apply_to_each')?['BurstCount']),'), window ending ',
    formatDateTime(convertFromUtc(addSeconds('1899-12-30T00:00:00Z',
      int(mul(float(items('Apply_to_each_1')?['ReceivedSerial']),86400))),'<tenant timezone>'),'dd MMM HH:mm'),
    ', but no burst alert was recorded.'),'')
```

**Daily slot test** (used by Layer 3a and as the Apply to each 2 input):

```
startsWith(formatDateTime(convertFromUtc(utcNow(),'<tenant timezone>'),'HH:mm'),'<first 4 characters of dailySlot>')
```

Pick the slot so exactly one run per day matches. **Apply to each 2 input:**
`@if(<slot test>, body('Filter_array_5'), json('[]'))`, never `createArray()` (Q38).

**Filter array 4**: `@greaterOrEquals(float(item()?['ReceivedSerial']),sub(variables('NowSerial'),1))`

**Append 1**: `@if(and(<slot test>, equals(length(body('Filter_array_4')),0)), 'INTAKE SILENT: …', '')`

**Filter array 6 / 7**: rows for `items('Apply_to_each_2')?['AlertID']` with serial ≥ now − 14,
then of those ≥ now − 3. **Append 2**: finding when count(6) ≥ 3 and count(7) = 0.

**Filter array 8**: from `@variables('Issues')`, where `@greater(length(string(item())),0)`.

**Email body** (expression editor):

```
concat('<p><b>Watchdog found possible alert gaps.</b></p><p>', join(body('Filter_array_8'),'</p><p>'),
  '</p><p>Checked at ', formatDateTime(convertFromUtc(utcNow(),'<tenant timezone>'),'dd MMM yyyy HH:mm'),
  '. Investigate in the log and the intake run history.</p>')
```

Subject: `[WATCHDOG] <tenant>: missed alert`. To: `config.json → watchdog.recipients`.

---

## Layer 2 catch (per guarded flow)

After the flow's last main step, add **Send an email (V2)** with *Settings → Run after* set to
FAILED, SKIPPED and TIMEDOUT (not SUCCEEDED), then **Terminate** with status Failed.

- Subject: `[WATCHDOG] <flow name> run failed`
- Body: `concat('<flow name> run failed at ', utcNow(), ' UTC. Run: ', <run link>)` where the run
  link is built from `workflow()?['tags']?['environmentName']`, `workflow()?['name']` and
  `workflow()?['run']?['name']`. Add the failing step's message where one exists:
  `actions('<step>')?['error']?['message']`.
- Never include the trigger body: on an intake it carries the payload and, on some triggers, the
  request URL.

---

## Sizing

Set the log listing's Top Count and Pagination threshold to cover 14 days of rows at the tenant's
peak rate with headroom; order by the receipt column descending so a cap drops the oldest rows,
not the newest (Q39).
