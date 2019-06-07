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
      continue;
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
      console.log('sent!');
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

var loop = function () {
  // check if driver
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      if (this.responseText) {
        driver();
      } else {
        spectator();
      }
    }
    sleep(500).then(() => {
      requestId = window.requestAnimationFrame(loop);
    });
  };

  var fd = new FormData();
  fd.append('fileId', fileId);
  xhttp.open('POST', '/is_driver', true);
  xhttp.send(fd);
}

var driver = function () {
  send_code();
}

var spectator = function () {
  get_code(fileId);
}
