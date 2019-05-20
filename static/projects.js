var files = document.getElementById('file_content')

var show_project = function (projectId) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      files.innerHTML = this.responseText;
    }
  }
  xhttp.open('GET', '/get_files/' + projectId, true);
  xhttp.send();
};
