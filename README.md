# NRCToStrava

Script to export/convert/upload run activities from Nike Run Club to Strava

## Requirements

* **Python 3**: All requirements are set in [requirements.txt](https://github.com/opierre/NRCToStrava/tree/master/requirements.txt)
  
* **Command-line JSON processor**: download and install [jq](https://github.com/stedolan/jq/releases) (*version >= 1.6*)
  
* **Strava**:
    * In order to upload NRC running data to Strava, it is required to make an application as explained 
  [here](https://developers.strava.com/docs/getting-started/#account) and fulfill all necessary fields.
  
## Prerequisites 
 
### NikeRunClub

All Nike+ API is explained in 
[Yoshimasa Niwa's gist](https://gist.github.com/niw/858c1ecaef89858893681e46db63db66). Fetching NRC activities requires
 a bearer token from their website:
 * Go to [Nike Membership page](https://www.nike.com/us/en_us/e/nike-plus-membership) and login
 * Open the developer tools in your browser and filter all "*api.nike.com*" requests
 * You should be able to find such request: "*/engage/invites/v1...*", then click on it
 * In Request Headers there should be an *Authorization* header with a *Bearer* value
 * Copy this value somewhere, it will be asked during **NRCToStrava.bash** execution
 
### Strava 
 
Uploading a run to Strava requires your Client ID, Client Secret and an access token with write permission:
 
* Client Secret and Client ID can be found in *My API Application>Client Secret/Client ID* and should be written in 
[.stravaupload.cfg](https://github.com/opierre/NRCToStrava/tree/master/scripts/.stravaupload.cfg) next to 
*clientsecret* and *clientid* keys. 
 
* In order to generate access token:
    * Get your Client ID at: *My API Application>Client ID* 
    * Open a webbrowser at (*replace [CLIENT_ID] with your client ID*):
     <http://www.strava.com/oauth/authorize?client_id=[CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:write,activity:write>
    * Login, tick each required authorization and click *Authorize*
    * On next page you will get an error but in the URL there is a code: 
    *exchange_token?state=&code=**e2989f17559e073d84ec532db782121519f4f03d**&scope=read,activity:write,profile:write*
    * Copy that code in 
[.stravaupload.cfg](https://github.com/opierre/NRCToStrava/tree/master/scripts/.stravaupload.cfg) next to 
*token* key. 

### Run bash script
  
Run script:
```bash
$ sh NRCToStrava.bash <bearer_token>
```

Paste NRC bearer value and press enter.

## Compatibility

This script has been tested on runs from 2014 to 2019.

## Notes

You can "*Edit distance*" on your run in Strava if the difference between NRC and Strava data is too big.
 
## Credits

* *NRCToStrava.bash* is adapted from [Yoshimasa Niwa's gist](https://gist.github.com/niw/858c1ecaef89858893681e46db63db66)
in order to convert JSON data to TCX and upload to Strava
* *stravaupload.py* is adapted from [Eirik Marthinsen github](https://github.com/marthinsen/stravaupload/blob/master/stravaupload.py) 
in order to work with Python 3 and current Strava API