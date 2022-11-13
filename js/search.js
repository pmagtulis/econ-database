function myFunction() {
  // Declare variables
  var input, filter, ul, a, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  ul = document.getElementsByClassName("card-body");
  
  cardTitles =[]
  for (i = 0; i < ul.length; i++) {
    cardTitles.push(ul[i].getElementsByClassName("card-title")[0]);
  }
  for (i = 0; i < cardTitles.length; i++) {
    }
}