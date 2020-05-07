/**
 * @license
 * Copyright (c) 2019 Cisco and/or its affiliates.
 *
 * This software is licensed to you under the terms of the Cisco Sample
 * Code License, Version 1.1 (the "License"). You may obtain a copy of the
 * License at
 *
 *                https://developer.cisco.com/docs/licenses
 *
 * All use of the material herein must be in accordance with the terms of
 * the License. All rights not expressly granted by the License are
 * reserved. Unless required by applicable law or agreed to separately in
 * writing, software distributed under the License is distributed on an "AS
 * IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied.
 */
const xapi = require('xapi');

const EVENT_JOIN_URI='999999999@webex.com';
const EVENT_PIN='000000';

const EVENT_PARTICIPANT_ROLE='Panelist'; // could be Panelist, Host or Guest
const BTN_JOIN_EVENT_PANELIST = 'panelist_join_event'

var theRemoteNumber="";
var isReceivingConfCallEvents = 0;

function sendTouchTones(password) {
    xapi.command('Call DTMFSend', { DTMFString: password });
  }

// to add delays when or if needed.  
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

xapi.event.on('CallDisconnect', (event) => {
    // nothing for now
    console.log("call ended");
    isReceivingConfCallEvents = 0;
    });

    
xapi.event.on('CallSuccessful', () => {
    if (isReceivingConfCallEvents==0) { 
        xapi.status.get('Call')
          .then((call) => {
            console.log("CallSuccesful: The CallbackNumber is:", call[0].CallbackNumber);
            console.log("Comparing theRemoteNumber with EVENT_JOIN_URI...");
            theRemoteNumber=call[0].CallbackNumber;
            if (theRemoteNumber.includes(EVENT_JOIN_URI)) {
                console.log("dialing pin....");
                sendTouchTones(EVENT_PIN+"#");
                // uncomment below if you want the call to start muted
                //setMute(true);
            }
            
        });
    }
    });

// once a call connects, invoke this handler to determine if a conference ID should be prompted for. 
xapi.status.on('Conference Call AuthenticationRequest', (request) => {
  
    console.log("The request is:", request);
    if (request=="PanelistPin") {
        isReceivingConfCallEvents = 1;
        // first assign theRemoteNumber to later check if the same when detected call
        theRemoteNumber="";
        xapi.status.get('Call')
                    .then(call => {
                    console.log('Detected a connected call: ');
                    theRemoteNumber=call[0].CallbackNumber;
                    console.log("in conf call event, theRemoteNumber= ",theRemoteNumber);
                    console.log("Comparing theRemoteNumber with EVENT_JOIN_URI...");
                    if (theRemoteNumber.includes(EVENT_JOIN_URI)) {
                        console.log("sending auth response....");
                        xapi.command('Conference Call AuthenticationResponse', { ParticipantRole:EVENT_PARTICIPANT_ROLE, Pin: EVENT_PIN+"#" });
                        // uncomment below if you want the call to start muted
                        //setMute(true);
                    }
                    });    
    } 
    });

// handle pressing the panel button: call into the Webex Events session
xapi.event.on('UserInterface Extensions Panel Clicked', (event) => {

    if(event.PanelId == BTN_JOIN_EVENT_PANELIST){
        // call webex event    
        console.log("Actual number to dial: ",EVENT_JOIN_URI);
        xapi.command("dial", {Number: EVENT_JOIN_URI});
    }


});
