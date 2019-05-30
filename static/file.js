var run_code = function (filename) {
  var fd = new FormData();
  var code = editor.getValue();
  console.log(code);
  fd.append('code', code);
  fd.append('filename', filename);

  console.log(fd);

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
  }
  console.log('sending:\n\n' + fd.get('code') + '\n\nand\n\n' + fd.get('filename'));
  xhttp.open('POST', 'http://159.65.162.204/run', true);
  xhttp.send(fd);
};
