var pollInterval = null;
var progressEl = document.getElementsByTagName('progress')[0];

function progressHandler(data) {
  progressEl.value = data.position / data.totalSize * 100;
}

function submitForm(ev) {
  ev.preventDefault();
  ev.stopPropagation();
  var formData = new FormData($('form')[0]);
  $.ajax({
    url: 'upload',  //Server script to process data
    type: 'POST',
    xhr: function() {  // Custom XMLHttpRequest
      var myXhr = $.ajaxSettings.xhr();
      if(myXhr.upload){ // Check if upload property exists
        myXhr.upload.addEventListener('progress',progressHandler, false); // For handling the progress of the upload
      }
      return myXhr;
    },
    //Ajax events
    beforeSend: function() {progressEl.style.display = 'inline-block';},
    success: onSuccess,
    error: onError,
    // Form data
    data: formData,
    //Options to tell jQuery not to process data or worry about content-type.
    cache: false,
    contentType: false,
    processData: false
  });
};

function poll(url) {
  pollInterval = setInterval(function() {loadSoundFile(url)}, 3000);
}

function onSuccess(data) {
  console.log('uploadComplete', data);
  poll(data);
}

function onError(data) {
  console.error('oh noww', data);
}

var context = new window.webkitAudioContext();
var source = null;
var audioBuffer = null;

function stopSound() {
  if (source) {
    source.noteOff(0);
  }
}

function playSound() {
  // source is global so we can call .noteOff() later.
  source = context.createBufferSource();
  source.buffer = audioBuffer;
  source.loop = false;
  source.connect(context.destination);
  source.noteOn(0); // Play immediately.
}

function initSound(arrayBuffer) {
  context.decodeAudioData(arrayBuffer, function(buffer) {
    // audioBuffer is global to reuse the decoded audio later.
    audioBuffer = buffer;
    document.getElementsByClassName('player')[0].style.display = 'block'
  }, function(e) {
    console.log('Error decoding file', e);
  }); 
}

// Load file from a URL as an ArrayBuffer.
// Example: loading via xhr2: loadSoundFile('sounds/test.mp3');
function loadSoundFile(url) {
  pollInterval = null;
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'arraybuffer';
  xhr.onload = function(e) {
    initSound(this.response); // this.response is an ArrayBuffer.
  };
  xhr.send();
}

(function(){
  $('.submit').on('click', submitForm);
  $('.start').on('click', playSound);
  $('.stop').on('click', stopSound);
})()
