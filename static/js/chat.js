// Define variables for WebRTC elements and WebSocket connection
let localVideo = document.getElementById('local-video');
let remoteVideo = document.getElementById('remote-video');
let videoCallDiv = document.getElementById('video-call-div');

let localStream = null;
let remoteStream = null;
let peerConnection = null;
let isMuted = false;
let isVideoMuted = false;

// WebSocket setup
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

// Capture WebSocket connection events
chatSocket.onopen = function(e) {
    console.log('WebSocket connection opened successfully');
};

chatSocket.onerror = function(e) {
    console.log('WebSocket connection error:', e);
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('Received data:', data);

    // Handle different types of messages (text, video, voice)
    if (data.type === 'call') {
        if (data.offer) {
            handleOffer(data.offer);
        } else if (data.answer) {
            handleAnswer(data.answer);
        } else if (data.candidate) {
            handleIceCandidate(data.candidate);
        }
    } else if (data.type === 'text') {
        console.log('Text message received:', data.message);
    }
};

// Send call offer/answer/candidate
function sendCallData(data) {
    chatSocket.send(JSON.stringify({
        type: 'call',
        data: data
    }));
}

// Start a call (Voice or Video)
function startCall(type) {
    console.log(`Starting ${type} call`);
    navigator.mediaDevices.getUserMedia({ video: type === 'video', audio: true })
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;

            createPeerConnection();
            localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

            if (type === 'video') {
                videoCallDiv.style.display = 'block';
            }

            peerConnection.createOffer().then(offer => {
                peerConnection.setLocalDescription(offer);
                sendCallData({ 'offer': offer });
            });
        })
        .catch(error => {
            console.log('Error accessing media devices:', error);
        });
}

// Create PeerConnection
function createPeerConnection() {
    peerConnection = new RTCPeerConnection({
        iceServers: [
            { urls: 'stun:stun.l.google.com:19302' }
        ]
    });

    peerConnection.ontrack = function(event) {
        console.log('Received remote stream');
        remoteStream = event.streams[0];
        remoteVideo.srcObject = remoteStream;
    };

    peerConnection.onicecandidate = function(event) {
        if (event.candidate) {
            sendCallData({ 'candidate': event.candidate });
        }
    };
}

// Handle received offer
function handleOffer(offer) {
    console.log('Received offer:', offer);
    createPeerConnection();

    peerConnection.setRemoteDescription(new RTCSessionDescription(offer))
        .then(() => {
            return navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        })
        .then(stream => {
            localStream = stream;
            localVideo.srcObject = stream;
            localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

            return peerConnection.createAnswer();
        })
        .then(answer => {
            peerConnection.setLocalDescription(answer);
            sendCallData({ 'answer': answer });
        })
        .catch(error => {
            console.log('Error handling offer:', error);
        });
}

// Handle received answer
function handleAnswer(answer) {
    console.log('Received answer:', answer);
    peerConnection.setRemoteDescription(new RTCSessionDescription(answer));
}

// Handle received ICE candidate
function handleIceCandidate(candidate) {
    console.log('Received ICE candidate:', candidate);
    peerConnection.addIceCandidate(new RTCIceCandidate(candidate));
}

// Mute/unmute audio
function muteAudio() {
    if (localStream) {
        localStream.getAudioTracks().forEach(track => track.enabled = !track.enabled);
        isMuted = !isMuted;
        console.log(isMuted ? 'Audio muted' : 'Audio unmuted');
    }
}

// Mute/unmute video
function muteVideo() {
    if (localStream) {
        localStream.getVideoTracks().forEach(track => track.enabled = !track.enabled);
        isVideoMuted = !isVideoMuted;
        console.log(isVideoMuted ? 'Video muted' : 'Video unmuted');
    }
}

// Share screen
function sharescreen() {
    navigator.mediaDevices.getDisplayMedia({ video: true }).then(stream => {
        const screenTrack = stream.getVideoTracks()[0];
        const sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
        sender.replaceTrack(screenTrack);

        screenTrack.onended = function() {
            // Revert back to webcam
            sender.replaceTrack(localStream.getVideoTracks()[0]);
        };
    }).catch(error => {
        console.log('Error sharing screen:', error);
    });
}

// End the call
function stopCall(is_send = false) {
    console.log('Stopping call');
    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
        localStream = null;
    }
    videoCallDiv.style.display = 'none';
    if (is_send) {
        sendCallData({ 'end_call': true });
    }
}
