#!/usr/bin/env bash
# Checked scalar counts shared by the README and route guards. Source this library.
# read_scalar_count <scratch-root> <allowed-statuses> <command...> prints one integer.
# read_text_metrics <scratch-root> <file> prints LF-line and byte counts.
read_scalar_count() {
  local count_root="$1" count_allowed="$2" count_tmp count_value count_rc count_ok=0
  shift 2
  mkdir -p "$count_root/target/tmp" || return 2
  count_tmp="$(mktemp -d "$count_root/target/tmp/scalar-count.XXXXXX")" || return 2
  count_value="$("$@" 2> "$count_tmp/error")"
  count_rc=$?
  case " $count_allowed " in *" $count_rc "*) count_ok=1 ;; esac
  if [ "$count_ok" -ne 1 ] || [ -s "$count_tmp/error" ] ||
     ! [[ "$count_value" =~ ^[[:space:]]*[0-9]+[[:space:]]*$ ]]; then
    printf 'UNREADABLE scalar count: %s failed, wrote stderr or returned invalid data (status %s).\n' \
      "$1" "$count_rc" >&2
    rm -rf "$count_tmp"
    return 2
  fi
  rm -rf "$count_tmp"
  printf '%s\n' "${count_value//[[:space:]]/}"
}

read_text_metrics() {
  local metrics_root="$1" metrics_file="$2" metrics_flag metrics_value
  local metrics_values=()
  for metrics_flag in -l -c; do
    if ! metrics_value="$(read_scalar_count "$metrics_root" 0 wc "$metrics_flag" < "$metrics_file")"; then
      printf 'UNREADABLE text measurement: wc %s unavailable.\n' "$metrics_flag" >&2
      return 2
    fi
    metrics_values+=("$metrics_value")
  done
  printf '%s\t%s\n' "${metrics_values[0]}" "${metrics_values[1]}"
}
