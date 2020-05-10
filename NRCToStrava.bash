#!/usr/bin/env bash

# NRCToStrava.bash
# A simple bash script to fetch all activities and metrics from NikePlus.
# See `README.md` for the details.

readonly bearer_token="$1"
if [[ -z "$bearer_token" ]]; then
  echo "Usage: $0 bearer_token"
  exit
fi

if ! type jq >/dev/null 2>&1; then
  echo "Missing jq, please install it." >&2
  exit 1
fi

nike_plus_api() {
  curl -H "Authorization: Bearer ${bearer_token}" "$@"
}

convertNRCToTCX() {
  python ./scripts/nrcToTcx.py "$@"
}

uploadTCXToStrava() {
  python ./scripts/stravaupload.py
}

printf "\n+--------------------------------------------------+"
printf "\n|           Start fetching NRC activities          |"
printf "\n+--------------------------------------------------+"
activity_ids=()
activities_page=0
while true; do
  activities_file="activities-${activities_page}.json"

  if [[ -z "$after_id" ]]; then
    url="https://api.nike.com/sport/v3/me/activities/after_time/0"
  else
    url="https://api.nike.com/sport/v3/me/activities/after_id/${after_id}"
  fi

  printf "\nFetch %s..." "$url"
  nike_plus_api "$url" > "./NRC_activities/$activities_file"

  activity_ids=("${activity_ids[@]}" $(jq -r ".activities[].id" "./NRC_activities/$activities_file"))

  after_id=$(jq -r ".paging.after_id" "./NRC_activities/$activities_file")
  if [[ "$after_id" == "null" ]]; then
    break
  else
    activities_page=$((activities_page + 1));
  fi
done

printf "\n+--------------------------------------------+"
printf "\n|   Download and convert NRC running data    |"
printf "\n+--------------------------------------------+"
for activity_id in ${activity_ids[@]}; do
  activity_file="activity-${activity_id}.json"

  activityId=${activity_id//$'\r'/}
  url="https://api.nike.com/sport/v3/me/activity/${activity_id//$'\r'/}?metrics=ALL"

  printf "\nFetching %s...\n" "$url"
  nike_plus_api "$url" > "./NRC_activities/$activity_file"
  printf "\nConverting %s...\n" "${activity_file//$'\r'/}"
  convertNRCToTCX "$activityId"

done

printf "\n+---------------------------------------------+"
printf "\n|   Uploading NRC converted data to Strava    |"
printf "\n+---------------------------------------------+\n"
uploadTCXToStrava
