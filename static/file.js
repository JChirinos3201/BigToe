var old_code;
var fileId;
var driver = false;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

var set_fileId = function (newFileId) {
  fileId = newFileId
}

var run_code = function (filename) {
  var code = editor.getValue();
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.response;
      var rjson = JSON.parse(r);
      if (rjson.stderr != "") {
        output.setValue(rjson.stderr);
      } else {
        output.setValue(rjson.stdout);
      }
    }
  };
  var fd = new FormData();
  fd.append('code', code);
  fd.append('filename', filename);
  xhttp.open('POST', 'http://159.65.162.204/run', true);
  xhttp.send(fd);
};

var update_code = function () {
  var new_code = editor.getValue();
  var tempPatchObj = diff_match_patch.prototype.patch_make(old_code, new_code);
  var patches;
  if (tempPatchObj.length == 1) {
    patches = tempPatchObj[0].toString();
  } else {
    patches = '';
  }
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      return;
    }
  };
  var fd = new FormData();
  fd.append('patches', patches);
  fd.append('fileId', fileId);
  xhttp.open('POST', '/update_code', true);
  xhttp.send(fd);
};

var send_code = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      //      console.log('sent!');
    }
  };
  var fd = new FormData();
  fd.append('code', editor.getValue());
  fd.append('fileId', fileId);
  xhttp.open('POST', '/update_code', true);
  xhttp.send(fd);
};

var get_code = function () {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var code = this.responseText;
      if (code != editor.getValue()) {
        var pos = editor.getCursorPosition();
        editor.setValue(code);
        old_code = code;
        editor.gotoLine(pos.row + 1, pos.column, false);
        var pos = editor.session.selection.toJSON()
        editor.session.setValue(code)
        editor.session.selection.fromJSON(pos)
      }

    }
  };
  var fd = new FormData();
  fd.append('fileId', fileId);
  xhttp.open('POST', '/get_code', true);
  xhttp.send(fd);
}

var relinquish_control = function () {
  //  console.log('RELINQUISHING CONTROL');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.response == 200) {
      driver = false;
    }
  };
  var fd = new FormData();
  fd.append('fileId', fileId);
  xhttp.open('POST', '/relinquish_control', true);
  xhttp.send(fd);
};

var take_control = function () {
  //  console.log('TAKING CONTROL');
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.response == 200) {
      if (this.responseText) {
        driver = true;
      } else {
        driver = false;
      }
    }
  };
  var fd = new FormData();
  fd.append('fileId', fileId);
  xhttp.open('POST', '/take_control', true);
  xhttp.send(fd);
};

var loop = function () {
  // check if driver
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.responseText;
      //      console.log(r);
      if (r == 'no driver') {
        spectator(false);
      } else if (r == 'driver') {
        driver();
      } else {
        spectator(true);
      }
      requestId = window.requestAnimationFrame(loop);
    }
  };
  var fd = new FormData();
  fd.append('fileId', fileId);
  xhttp.open('POST', '/is_driver', true);
  sleep(100).then(() => {
    xhttp.send(fd);
  });
}

var driver = function () {
  var d = document.getElementById('control-button');
  //  console.log(d.innerHTML);
  if (d.innerHTML != '<button class="btn btn-sm btn-warning" onclick="relinquish_control();"> Relinquish Control</button>') {
    d.innerHTML = '<button class="btn btn-sm btn-warning" onclick="relinquish_control();"> Relinquish Control</button>';
  }
  send_code();
}

var spectator = function (driver_exists) {
  var d = document.getElementById('control-button');
  if (!driver_exists) {
    if (d.innerHTML != '<button class="btn btn-sm btn-warning" onclick="take_control();">Take control</button>') {
      d.innerHTML = '<button class="btn btn-sm btn-warning" onclick="take_control();">Take control</button>';
    }
  } else {
    if (d.innerHTML != '<button class="btn btn-sm btn-warning" disabled>Take control</button>') {
      d.innerHTML = '<button class="btn btn-sm btn-warning" disabled>Take control</button>';
    }
  }
  get_code();
}
get_code();
loop();
