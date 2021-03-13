function showFile(input) {
  let reader = new FileReader();
  let file = input.files[0];
  reader.readAsText(file);
  reader.onload = function() {
    console.log(reader.result);
  };
  reader.onerror = function() {
    console.log(reader.error);
  };
  alert(`File name: ${file.name}`); // например, my.png
}
