var run_code = function () {
  var fd = new FormData();
  var code = editor.getValue();
  console.log(code);
  fd.append('code', code);

  console.log(fd);

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var r = this.responseText;
      console.log(r);
      output.setValue(this.responseText);
    }
  }
  xhttp.open('POST', '/run_code', true);
  xhttp.send(fd);
};
