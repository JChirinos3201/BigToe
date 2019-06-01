var run_code = function (filename) {
  var code = editor.getValue();

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.response;
      console.log(r);

      var rjson = JSON.parse(r);

      console.log(rjson);

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

  console.log('sending:\n\n' + fd.get('code') + '\n\nand\n\n' + fd.get('filename'));

  xhttp.open('POST', 'http://159.65.162.204/run', true);
  xhttp.send(fd);
};

var send_code = function (fileId) {
  var new_code = editor.getValue();
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log('sent!');
    }
  };
  var fd = new FormData();
  fd.append('code', new_code);
  fd.append('fileId', fileId);

  xhttp.open('POST', '/update_code', true);
  xhttp.send(fd);
};

var get_code = function (fileId) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var code = this.responseText;
      editor.setValue(code);
    }
  };
  var fd = new FormData();
  fd.append('fileId', fileId);

  console.log(fileId);

  xhttp.open('POST', '/get_code', true);
  xhttp.send(fd);
}
