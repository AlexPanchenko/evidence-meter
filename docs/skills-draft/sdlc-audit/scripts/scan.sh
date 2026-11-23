#!/usr/bin/env bash
# Read-only scan of one feature's SDLC artifacts. Prints one TSV row per artifact:
# id, phase, artifact, path, state, last_commit, detail
# state: present | missing | stale | n/a ; detail explains it. Dates are git commit dates, not file mtimes.
set -euo pipefail

slug="${1:?usage: scan.sh <slug>}"
root="$(git rev-parse --show-toplevel)"
cd "$root"
dir="docs/features/$slug"
[ -d "$dir" ] || { echo "no feature folder: $dir" >&2; exit 2; }

ts() { git log -1 --format=%ct -- "$@" 2>/dev/null || true; }          # last commit time touching paths
sha() { git log -1 --format=%h -- "$@" 2>/dev/null || true; }
dt() { [ -n "$1" ] && date -r "$1" "+%F %H:%M" || echo "-"; }
day() { [ -n "$1" ] && date -r "$1" +%F || echo "-"; }
dirty() { [ -n "$(git status --porcelain -- "$@" 2>/dev/null)" ] && echo " (uncommitted changes)" || true; }
# Last commit that changed more than frontmatter lines (a status or date sync is not a content change).
cts() {
  local c
  for c in $(git log --format=%h -- "$1" 2>/dev/null); do
    if git show --format= --unified=0 "$c" -- "$1" | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' \
       | grep -qvE '^[+-](---|[a-z_]+:.*)$'; then
      git log -1 --format=%ct "$c"; return
    fi
  done
}
fm() { [ -f "$1" ] && awk -v k="$2" 'NR==1&&$0!="---"{exit} NR>1&&$0=="---"{exit} $0~"^"k":"{sub("^"k":[ ]*","");gsub(/"/,"");print;exit}' "$1" || true; }

# Contexts the feature touches: PRD frontmatter `contexts`, else sad.md, else none (code staleness skipped).
contexts="$(fm "$dir/PRD.md" contexts)"; [ -n "$contexts" ] || contexts="$(fm "$dir/sad.md" contexts)"
ctx_paths=()
for c in $(echo "$contexts" | tr -d '[],' ); do
  [ -d "src/evidence_meter/$c" ] && ctx_paths+=("src/evidence_meter/$c")
done
surfaces="$(fm "$dir/sad.md" target_surfaces)"
size="$(cat "$dir/.size" 2>/dev/null | tr -d '[:space:]' || true)"

code_ts=""; [ ${#ctx_paths[@]} -gt 0 ] && code_ts="$(ts "${ctx_paths[@]}")"

row() { # id phase name path upstream_paths(;-sep) code_paths(;-sep)
  local id="$1" ph="$2" name="$3" p="$4" up="$5" code="$6" state detail t
  if [ ! -e "$p" ]; then
    printf '%s\t%s\t%s\t%s\tmissing\t-\t%s\n' "$id" "$ph" "$name" "$p" "-"; return
  fi
  t="$(ts "$p")"; local tc; tc="$(cts "$p")"; [ -n "$tc" ] || tc="$t"; state=present; detail="status: $(fm "$p" status)"
  [ "$detail" = "status: " ] && detail=""
  if [ -z "$t" ]; then detail="${detail:+$detail; }never committed"; fi
  local u ut
  IFS=';' read -ra ups <<< "$up"
  for u in ${ups[@]+"${ups[@]}"}; do
    [ -n "$u" ] && [ -e "$u" ] || continue
    ut="$(cts "$u")"
    if [ -n "$tc" ] && [ -n "$ut" ] && [ "$ut" -gt "$tc" ]; then
      state=stale; detail="${detail:+$detail; }content older than upstream $u ($(dt "$tc") < $(dt "$ut"))"
    fi
  done
  if [ "$code" = "CTX" ] && [ -n "$code_ts" ] && [ -n "$t" ] && [ "$code_ts" -gt "$tc" ]; then
    state=stale; detail="${detail:+$detail; }older than code in ${ctx_paths[*]+${ctx_paths[*]}} ($(day "$code_ts"))"
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s%s\n' "$id" "$ph" "$name" "$p" "$state" "$(day "$t")" "$detail" "$(dirty "$p")"
}

row 1 1 CONTEXT        "$dir/CONTEXT.md"            ""                                   ""
row 2 1 idea-brief     "$dir/idea-brief.md"         "$dir/CONTEXT.md"                    ""
row 3 2 PRD            "$dir/PRD.md"                "$dir/idea-brief.md;$dir/CONTEXT.md" ""
row 4 3 sad            "$dir/sad.md"                "$dir/PRD.md"                        CTX
if [ -d "$dir/adr" ]; then row 5 3 adr/ "$dir/adr" "$dir/sad.md" ""
else printf '5\t3\tadr/\t%s\tmissing\t-\trepo-level docs/adr has %s ADR(s)\n' "$dir/adr" "$(ls docs/adr 2>/dev/null | grep -c '\.md$' || true)"; fi
if [ -e "$dir/data-model.md" ]; then row 6 4 data-model "$dir/data-model.md" "$dir/PRD.md;$dir/sad.md" CTX
else printf '6\t4\tdata-model\t%s\tmissing\t-\trepo-level migrations/: %s\n' "$dir/data-model.md" "$(ls migrations 2>/dev/null | grep '\.up\.sql$' | tr '\n' ' ' || echo none)"; fi
if [ -n "$surfaces" ] && ! echo "$surfaces" | grep -Eq 'backend-service|api|web-frontend'; then
  printf '7\t4\topenapi.yaml\t%s\tn/a\t-\tsurfaces %s; expect contracts/cli.md or events.md instead (%s)\n' \
    "$dir/contracts/openapi.yaml" "$surfaces" "$(ls "$dir/contracts" 2>/dev/null | tr '\n' ' ' || echo none)"
else row 7 4 openapi.yaml "$dir/contracts/openapi.yaml" "$dir/PRD.md;$dir/data-model.md;$dir/sad.md" ""; fi
row 8 4 api-sync-report "$dir/contracts/api-sync-report.md" "$dir/contracts/openapi.yaml;$dir/data-model.md" ""
tasks="$dir/tasks/tasks.json"; [ -e "$tasks" ] || { [ -e "$dir/tasks.json" ] && tasks="$dir/tasks.json"; }
row 9 5 tasks/         "$tasks"                     "$dir/PRD.md;$dir/sad.md"            CTX

# Context lines (prefixed with #) the report uses below the table.
echo "# size: ${size:-unknown}"
echo "# contexts: ${contexts:-none declared in PRD or sad frontmatter, code staleness not checked} -> code paths: ${ctx_paths[*]+${ctx_paths[*]}}; last code commit: $(day "$code_ts")"
echo "# surfaces: ${surfaces:-not chosen (no sad.md)}"
shape() { echo "$(grep -c '^## ' "$1" || true) sections, $(wc -w < "$1" | tr -d ' ') words"; }
for v in "$dir"/*.*.md; do
  [ -e "$v" ] || continue
  base="$dir/$(basename "$v" | cut -d. -f1).md"
  echo "# variant: $v ($(sha "$v"); $(shape "$v")) beside $base ($( [ -f "$base" ] && shape "$base" || echo missing))"
done
if [ -f docs/architecture-map.md ]; then
  rc="$(fm docs/architecture-map.md reflects_commit)"
  if [ -n "$rc" ] && git cat-file -e "$rc" 2>/dev/null; then
    n="$(git rev-list --count "$rc"..HEAD -- src migrations)"
    echo "# architecture-map: reflects $rc; $n later commit(s) touch src/ or migrations/"
  fi
fi
if [ -f "$dir/PRD.md" ]; then
  echo "# PRD open questions: $(grep -c '^- \[ \]' "$dir/PRD.md" || true)"
fi
echo "# not visible to this scan: decisions held outside the repository (chat edits-logs, plans, tickets)"
