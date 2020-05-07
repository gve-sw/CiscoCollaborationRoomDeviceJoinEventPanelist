# Cisco Collaboration Room Device Join Event Panelist

This macro simplifies the joining into Webex Events from a **Cisco Webex RoomKit** room device or any other [Cisco Collaboration Room Endpoint](https://www.cisco.com/c/en/us/products/collaboration-endpoints/collaboration-room-endpoints/index.html) running CE 9.6 and later with the ability to run macros. 

It stores the panelists SIP URI and PIN for a specific Event right inside the macro code to make it a one-step operation to have panelists enter a room with a device running the macro and just press that one button to join. 

There are two ways to try this macro:

## Manual process
- Log onto the admin page of the device and create one action button in the InRoom control editor for the device with the PanelID 'panelist_join_event'. Alternatively, you could import the action buttons from the **panelistJoinEventButton.xml** file provided.
- Load the Javascript code included in the the **CallWebexEventJoinPanelist.js** file into a new Macro in the Macro editor 
- Edit the EVENT_JOIN_URI and EVENT_PIN variables in the script to contain the credentials for the Webex Event you want the button to use to join the event. 
- Enable the macro in the editor and you are ready to go.  

## Deploy and enable via Python script
Use the **SendMacros.py** Python script to connect to a list of devices and create the button and load/enable the macro:
- Make sure you have Python 3.6 or later installed in your environment
- Run ```pip install -r requirements.txt``` to make sure you have all needed Python libraries installed
- Edit the **macros-enable.xml** file to edit the EVENT_JOIN_URI and EVENT_PIN variables in the script to contain the credentials for the Webex Event you want the button to use to join the event
- Edit the **TP_List.csv** file to contain the IP addresses of all devices you would like to load the macro into
- Execute the **SendMacros.py** script:  ```python SendMacros.py``` . 
You will be prompted for credentials to use when connecting to the video devices to be able to load and activate the macro. 
Those credentials must match an account on the devices that has at least Integrator priviledges. 
All devices in the list in **TP_List.csv** must have the same user account with integration priviledges for the macro to be installed. 
- Once the script finishes executing, file named **TP_codec_config_update_report.txt** with be placed in the same directory of the **SendMacros.py** Python script with details on which devices were modified and which were not and why

## Usage

Once the "JoinEvent" button is configured and the macro is active, users can just touch the button while not in an active call and the device will dial the event and automatically enter the PIN to join the session.

More information on how to invoke the Macro editor and customized the User Interface of a Cisco Collaboration Room Endpoint can be found in this [CE Customization User Interface Extensions and Macros, CE9.6](https://www.cisco.com/c/dam/en/us/td/docs/telepresence/endpoint/ce96/sx-mx-dx-room-kit-customization-guide-ce96.pdf) guide. 

(macro distribution Python script was based on sample script originally posted at: https://community.cisco.com/t5/ip-telephony-and-phones/bulk-deploy-macros-on-telepresence-endpoints/td-p/3814373 in a Cisco Communities discussion)